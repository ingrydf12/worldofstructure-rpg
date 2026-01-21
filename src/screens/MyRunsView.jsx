import React from "react";
import { useGame } from "../context/gamePyContext";
import { useNavigate } from "react-router-dom";
import TormGenericButton from "../components/TormGenericButton";
import "../styles/myRunsStyleView.css";

import imgBalestreiro from "../assets/character/archer.png";
import imgGuerreiro from "../assets/character/warrior.png";
import imgMago from "../assets/character/magician.png";

const classIcons = {
  Balestreiro: imgBalestreiro,
  Guerreiro: imgGuerreiro,
  Mago: imgMago,
};

const MyRunsView = () => {
  const { historicoRuns } = useGame();
  const navigate = useNavigate();

  return (
    <main className="runs-view-container">
      <header>
        <TormGenericButton
          title="Voltar ao Menu"
          onClick={() => navigate("/")}
        />
      </header>

      <div className="runs-content">
        <h2>Suas runs</h2>

        <section className="runs-list">
          {!historicoRuns || historicoRuns.length === 0 ? (
            <div className="empty-history">
              <p>Parece que você não trilhou uma rota ainda...</p>
              <TormGenericButton
                title="Iniciar Nova Jornada"
                onClick={() => navigate("/")}
              />
            </div>
          ) : (
            historicoRuns.map((run) => (
              <article key={run.run_id} className="run-card">
                <div className="run-card-header">
                  <img
                    src={classIcons[run.class_type] || imgGuerreiro}
                    alt={run.class_type}
                    className="class-icon-mini"
                  />
                  <div className="run-meta">
                    <h3>Aventura - ID {run.run_id}</h3>
                    <span>Classe: {run.class_type}</span>
                  </div>
                </div>

                <div className="run-content">
                  <h4>Caminho Percorrido:</h4>
                  <ul className="event-timeline">
                    {run.events.map((evento, idx) => (
                      <li key={idx} className="event-item">
                        <span className="bullet">›</span> {evento}
                      </li>
                    ))}
                  </ul>
                </div>
              </article>
            ))
          )}
        </section>
      </div>
    </main>
  );
};

export default MyRunsView;
