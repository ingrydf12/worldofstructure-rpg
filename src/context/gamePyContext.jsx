import { createContext, useContext, useState, useEffect } from "react";
import { listen } from "@tauri-apps/api/event";
import { invoke } from "@tauri-apps/api/tauri";
import { useNavigate } from "react-router-dom";

const GameContext = createContext();

export const useGame = () => useContext(GameContext);

export const GameProvider = ({ children }) => {
  const [player, setPlayer] = useState(null);
  const [narrativa, setNarrativa] = useState([]);
  const [opcoes, setOpcoes] = useState([]);
  const [aguardando, setAguardando] = useState(false);
  const [emCombate, setEmCombate] = useState(false);
  const [enemy, setEnemy] = useState(null);
  const [status, setStatus] = useState("NARRATIVE");
  const [historicoRuns, setHistoricoRuns] = useState([]);
  
  const [gameState, setGameState] = useState({ turn: 0 });
  const [turnResult, setTurnResult] = useState(null);

  const navigate = useNavigate();

  const handleMensagem = (mensagem) => {
    if (!mensagem) return;
    mensagem = mensagem.trim();

    if (mensagem.startsWith("PLAYER_STATE::")) {
      try { setPlayer(JSON.parse(mensagem.replace("PLAYER_STATE::", ""))); } catch (err) { console.error(err); }
      return;
    }

    if (mensagem.startsWith("ENEMY_STATE::")) {
      try {
        setEnemy(JSON.parse(mensagem.replace("ENEMY_STATE::", "")));
        setEmCombate(true);
      } catch (err) { console.error(err); }
      return;
    }

    if (mensagem.startsWith("COMBAT_STATE::")) {
      try {
        const data = JSON.parse(mensagem.replace("COMBAT_STATE::", ""));
        setGameState(data);
        setPlayer(data.player);
        setEnemy(data.enemy);
      } catch (err) { console.error(err); }
      return;
    }

    if (mensagem.startsWith("RESULTADO_TURNO::")) {
      const result = mensagem.replace("RESULTADO_TURNO::", "").replace(/"/g, "");
      setTurnResult(result);
      return;
    }

    if (mensagem.startsWith("GAME_STATE::")) {
      const novoStatus = mensagem.replace("GAME_STATE::", "").replace(/"/g, "");
      setStatus(novoStatus);
      if (novoStatus === "NARRATIVE") {
        setEmCombate(false);
        setEnemy(null);
        setTurnResult(null);
      }
      return;
    }

    if (mensagem.startsWith("RESULTADO_COMBATE::")) {
      const resultado = mensagem.replace("RESULTADO_COMBATE::", "").replace(/"/g, "");
      if (resultado === "VITORIA") {
        setEmCombate(false);
        setEnemy(null);
        setStatus("NARRATIVE");
        navigate("/narrative-game-screen");
      }
      return;
    }

    if (mensagem.startsWith("BRANCH_DATA::")) {
      try {
        const data = JSON.parse(mensagem.replace("BRANCH_DATA::", ""));
        setNarrativa(data.narrativa || []);
        setOpcoes(data.opcoes || []);
        setAguardando(false);
        setEmCombate(false);
      } catch (err) { console.error(err); }
      return;
    }

    if (mensagem === "AGUARDANDO_ESCOLHA") setAguardando(true);
    if (mensagem === "INICIO_DE_COMBATE") {
      setEmCombate(true);
      setAguardando(false);
      setTurnResult(null);
    }
    
    if (mensagem.startsWith("RUNS::")) {
      try {
        const data = JSON.parse(mensagem.split("RUNS::")[1]);
        setHistoricoRuns(data);
      } catch (e) { console.error(e); }
    }
  };

  useEffect(() => {
    let unlisten;
    (async () => {
      unlisten = await listen("python-output", (event) => handleMensagem(event.payload));
    })();
    return () => { if (unlisten) unlisten(); };
  }, []);

  const iniciarJogo = async (nome, classe) => {
    try { await invoke("iniciar_jogo", { nome, classe }); } 
    catch (err) { console.error(err); }
  };

  const enviarEscolha = async (id) => {
    try {
      setTurnResult(null); // Limpa o "Sucesso/Falha" antes de enviar nova ação
      await invoke("send_to_engine", { message: id });
      setAguardando(false);
    } catch (err) { console.error(err); }
  };

  return (
    <GameContext.Provider
      value={{
        player,
        enemy,
        narrativa,
        opcoes,
        aguardando,
        emCombate,
        iniciarJogo,
        enviarEscolha,
        status,
        historicoRuns,
        gameState,
        turnResult,
        setTurnResult
      }}
    >
      {children}
    </GameContext.Provider>
  );
};