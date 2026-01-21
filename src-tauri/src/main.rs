#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::Mutex;
use once_cell::sync::Lazy;
use tauri::{Manager, AppHandle};

// pra utilização do side-car
use tauri::api::process::{Command, CommandChild, CommandEvent};

static PYTHON_PROCESS: Lazy<Mutex<Option<CommandChild>>> = Lazy::new(|| Mutex::new(None));

#[tauri::command]
fn iniciar_jogo(
    app_handle: AppHandle,
    nome: String,
    classe: String,
) -> Result<(), String> {
    println!(
        "[TAURI] Iniciando Sidecar Python | nome='{}' classe='{}'",
        nome, classe
    );

    let (mut rx, child) = Command::new_sidecar("app")
        .map_err(|e| format!("Falha ao encontrar binário sidecar: {}", e))?
        .args(["--nome", &nome, "--classe", &classe])
        .spawn()
        .map_err(|e| format!("Erro ao iniciar Python sidecar: {}", e))?;

    let app = app_handle.clone();
    tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(line) => {
                    println!("[PYTHON STDOUT] {}", line);
                    app.emit_all("python-output", line).ok();
                }
                CommandEvent::Stderr(line) => {
                    println!("[PYTHON STDERR] {}", line);
                }
                CommandEvent::Terminated(payload) => {
                    println!("[TAURI] Python encerrado. Status: {:?}", payload.code);
                    break;
                }
                _ => {}
            }
        }
    });

    *PYTHON_PROCESS.lock().unwrap() = Some(child);

    println!("[TAURI] Processo Sidecar iniciado com sucesso");
    Ok(())
}

#[tauri::command]
fn send_to_engine(message: String) -> Result<(), String> {
    println!("[TAURI] Enviando para Python: {}", message);

    let mut process_lock = PYTHON_PROCESS.lock().unwrap();
    if let Some(child) = process_lock.as_mut() {
        child.write(format!("{}\n", message).as_bytes())
            .map_err(|e| format!("Erro ao escrever no Python: {}", e))?;
    } else {
        return Err("Processo Python não está rodando".into());
    }

    Ok(())
}

#[tauri::command]
fn encerrar_jogo() -> Result<(), String> {
    println!("[TAURI] Encerrando jogo");

    if let Some(child) = PYTHON_PROCESS.lock().unwrap().take() {
        child.kill().ok();
        println!("[TAURI] Comando de encerramento enviado");
    }

    Ok(())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            iniciar_jogo,
            send_to_engine,
            encerrar_jogo
        ])
        .build(tauri::generate_context!())
        .expect("Erro ao buildar aplicação Tauri")
        .run(|_app_handle, event| {
            match event {
                tauri::RunEvent::ExitRequested { .. }
                | tauri::RunEvent::Exit => {
                    println!("[TAURI] App encerrando, finalizando Python sidecar");

                    if let Some(child) = PYTHON_PROCESS.lock().unwrap().take() {
                        child.kill().ok();
                    }
                }
                _ => {}
            }
        });
}