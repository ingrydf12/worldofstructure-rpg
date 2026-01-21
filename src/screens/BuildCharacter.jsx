import React, { useState } from "react";
import "../styles/buildCharacterStyleView.css";
import { useNavigate } from "react-router-dom";
import { useGame } from "../context/gamePyContext";

import guerreiroImg from "../assets/character/warrior.png";
import magoImg from "../assets/character/magician.png";
import balestreiroImg from "../assets/character/archer.png";

const CLASSES = [
  { id: "Guerreiro", label: "Guerreiro", image: guerreiroImg },
  { id: "Mago", label: "Mago", image: magoImg },
  { id: "Balestreiro", label: "Balestreira", image: balestreiroImg },
];

const BuildCharacter = () => {
  const navigate = useNavigate();
  const { iniciarJogo } = useGame();

  const [step, setStep] = useState(1);
  const [nome, setNome] = useState("");
  const [classe, setClasse] = useState(null);

  const avancarParaClasse = () => {
    if (!nome.trim()) return;
    setStep(2);
  };

  const escolherClasse = async (classeEscolhida) => {
    setClasse(classeEscolhida);
    await iniciarJogo(nome, classeEscolhida);
    navigate("/narrative-game-screen");
  };

  return (
    <main className="build-character">
      <div className="build-character-input-container">
        {step === 1 && (
          <section className="step-name">
            <h1>Crie seu herói</h1>
            <p>Digite o nome do seu personagem</p>

            <div className="input-area">
              <input
                type="text"
                placeholder="Nome do Herói"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
              />
              <button className="custom-button" onClick={avancarParaClasse}>Continuar</button>
            </div>
          </section>
        )}

        {step === 2 && (
          <section className="step-class">
            <h1>Escolha sua classe</h1>
            <p>
              Seu destino começa aqui, <b>{nome}</b>
            </p>

            <div className="class-grid">
              {CLASSES.map((c) => (
                <div key={c.id} className="class-card">
                  <img src={c.image} alt={c.label} />
                  <button className="custom-button" onClick={() => escolherClasse(c.id)}>
                    {c.label}
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
};

export default BuildCharacter;