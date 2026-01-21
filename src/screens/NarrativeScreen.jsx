import { useGame } from "../context/gamePyContext";
import TormGenericButton from "../components/TormGenericButton";
import { useEffect, useState } from "react"; // Adicione useState
import { useNavigate } from "react-router-dom";
import "../styles/narrativeScreenStyleView.css";
import UnderwaterImg from "../assets/bg/UndergroundJungleNewBetter.gif";

const NarrativeScreen = () => {
  const { narrativa, opcoes, aguardando, enviarEscolha, emCombate, status } = useGame();
  const navigate = useNavigate();

  useEffect(() => {
    if (emCombate) {
      navigate("/combat");
    } 
    else if (status === "NARRATIVE" && window.location.pathname === "/combat") {
      navigate("/narrative-game-screen");
    }
  }, [emCombate, status, navigate]);

  if (!narrativa || narrativa.length === 0) {
    return (
      <main className="narrative-screen-main">
         <div className="loading-container"> 
            <p>Carregando próxima parte da jornada...</p>
         </div>
      </main>
    );
  }

  const isGameOver = status === "FIM_DA_NARRATIVA" || (opcoes.length === 0 && !emCombate);

  return (
    <main className="narrative-screen-main">
      <div
        className="animated-narrative-bg"
        style={{ backgroundImage: `url(${UnderwaterImg})` }}
      />

      <section className="narrative-text">
        {narrativa.map((linha, index) => (
          <p key={index}>{linha}</p>
        ))}
      </section>

      <section className="narrative-options">
        {isGameOver ? (
          <TormGenericButton
            title="Ver Histórico de Runs"
            onClick={() => navigate("/runs")}
            className="btn-finalizar"
          />
        ) : (
          !emCombate && opcoes.filter(Boolean).map((opcao) => (
            <TormGenericButton
              key={opcao.id}
              title={opcao.texto}
              onClick={() => enviarEscolha(opcao.id)}
              disabled={!aguardando}
            />
          ))
        )}
      </section>
    </main>
  );
};

export default NarrativeScreen;