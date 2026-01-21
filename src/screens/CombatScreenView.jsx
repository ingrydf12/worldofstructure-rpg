import { useState, useEffect } from "react";
import { useGame } from "../context/gamePyContext";
import { listen } from "@tauri-apps/api/event";
import { invoke } from "@tauri-apps/api";
import "../styles/combatScreenStyleView.css";
import dadoGif from "../assets/dice/dados.gif";
import { useNavigate } from "react-router-dom";

// Assets
import fightOgroImg from "../assets/fight/fight-ogro.gif";
import fightBanditImg from "../assets/fight/fight-bandit.gif";
import imgBalestreiro from "../assets/character/archer.png";
import imgGuerreiro from "../assets/character/warrior.png";
import imgMago from "../assets/character/magician.png";
import imgOrcRei from "../assets/enemies/king_orc.png";
import imgBadArcher from "../assets/enemies/bad_archer.png";

export const CombatScreenView = () => {
  const { player, enemy, setGameState, turnResult, setTurnResult } = useGame();

  const navigate = useNavigate();
  const [selectedAttribute, setSelectedAttribute] = useState(null);

  const playerAttributes = player?.attributes ?? {};

  const fightBgImage =
    enemy?.name === "Bad Archer" ? fightBanditImg : fightOgroImg;

  const playerImg =
    {
      Balestreiro: imgBalestreiro,
      Guerreiro: imgGuerreiro,
      Mago: imgMago,
    }[player?.class_type] || imgGuerreiro;

  const enemyImg =
    {
      "Orc Rei": imgOrcRei,
      "Bad Archer": imgBadArcher,
    }[enemy?.name] || imgOrcRei;

  useEffect(() => {
    let activeListeners = [];

    async function setupListeners() {
      const addListener = async (name, callback) => {
        const unlisten = await listen(name, callback);
        activeListeners.push(unlisten);
      };

      try {
        await addListener("RESULTADO_TURNO", (event) => {
          setTurnResult(event.payload);
        });

        await addListener("COMBAT_STATE", (event) => {
          setGameState(event.payload);
        });

        await addListener("RESULTADO_COMBATE", (event) => {
          if (event.payload === "VITORIA") {
            setTimeout(() => navigate("/narrative-game-screen"), 1500);
          }
        });
      } catch (error) {
        console.error("Erro nos listeners de combate:", error);
      }
    }

    setupListeners();
    return () => activeListeners.forEach((u) => u());
  }, [navigate, setGameState, setTurnResult]);

  const enviarEscolha = async (atributo, acao) => {
    if (!atributo || !acao) return;

    setTurnResult(null);
    setSelectedAttribute(null);

    const comando = `COMBAT_CHOICE::${atributo}::${acao}`;
    try {
      await invoke("send_to_engine", { message: comando });
    } catch (err) {
      console.error("[FRONT] Erro ao enviar comando:", err);
    }
  };

  const tentarNovamente = async () => {
    setTurnResult(null);
    setSelectedAttribute(null);
    await invoke("send_to_engine", { message: "TENTAR_NOVAMENTE" });
  };

  const reiniciarNarrativa = async () => {
    await invoke("send_to_engine", { message: "REINICIAR_JOGO" });
  };

  return (
    <main className="combat-container">
      <header className="combat-calculo-status">
        <section className="combat-status">
          {turnResult ? (
            <div className={`result-container animate-pop`}>
              <p className={turnResult === "SUCESSO" ? "success" : "failure"}>
                {turnResult === "SUCESSO"
                  ? "VANTAGEM! ATAQUE BEM-SUCEDIDO!"
                  : "PERIGO! VOCÊ FOI ATINGIDO!"}
              </p>
            </div>
          ) : selectedAttribute ? (
            <p className="pending">
              Atributo <span className="atribute">{selectedAttribute}</span>{" "}
              selecionado. Escolha uma <b>ação</b> abaixo.
            </p>
          ) : (
            <div className="combat-placeholder">
              <img src={dadoGif} alt="Rolando dado" />
              <p>Aguardando sua estratégia...</p>
            </div>
          )}
        </section>
        <h3 className="combat-instruction">FASE DE DECISÃO</h3>
      </header>

      {/* MARK: - Telinha que marca os personagens*/}
      <section className="combat-screen">
        <div
          className="animated-fight-bg"
          style={{ backgroundImage: `url(${fightBgImage})` }}
        />

        {/* Jogador */}
        <div
          className={`combat-unit player-unit ${turnResult === "FALHA" ? "shake" : ""}`}
        >
          <img
            src={playerImg}
            alt={player?.class_type}
            className="unit-sprite"
          />
          <section className="combat-player-status">
            <h3>{player?.name}</h3>
            <div className="hp-bar-container">
              <div
                className="hp-fill"
                style={{ width: `${(player?.life / 10) * 100}%` }}
              ></div>
              <p>{Math.max(0, player?.life ?? 0)} HP</p>
            </div>
          </section>
        </div>

        {/* Inimigo */}
        <div className="combat-unit enemy-unit">
          <img src={enemyImg} alt={enemy?.name} className="unit-sprite" />
          <section className="combat-enemy-status">
            <h3>{enemy?.name}</h3>
            <div className="hp-bar-container enemy-hp">
              <div
                className="hp-fill"
                style={{ width: `${(enemy?.life / 20) * 100}%` }}
              ></div>
              <p>{Math.max(0, enemy?.life ?? 0)} HP</p>
            </div>
          </section>
        </div>
      </section>

      <section className="combat-box-options">
        <div className="combat-attributes">
          {Object.entries(playerAttributes).map(([attr, val]) => (
            <button
              key={attr}
              onClick={() => setSelectedAttribute(attr)}
              className={`medieval-button ${selectedAttribute === attr ? "selected" : ""}`}
            >
              {attr.toUpperCase()} <span className="attr-val">{val}</span>
            </button>
          ))}
        </div>

        <div className="combat-actions">
          <button
            className="medieval-button"
            disabled={!selectedAttribute}
            onClick={() => enviarEscolha(selectedAttribute, "ATAQUE")}
          >
            Lutar
          </button>
          <button
            className="medieval-button"
            disabled={!selectedAttribute}
            onClick={() => enviarEscolha(selectedAttribute, "DEFESA")}
          >
            Proteger-se
          </button>
        </div>
      </section>

      {status === "DERROTA" && (
        <div className="defeat-overlay">
          <div className="defeat-content">
            <h2>A MORTE TE ENCONTROU...</h2>
            <button className="medieval-button retry" onClick={tentarNovamente}>
              Tentar de Novo
            </button>
            <button
              className="medieval-button quit"
              onClick={reiniciarNarrativa}
            >
              Desistir
            </button>
          </div>
        </div>
      )}
    </main>
  );
};
