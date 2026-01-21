import React from "react";
import UnderwaterImg from "../assets/bg/UndergroundJungleNewBetter.gif";

import magoImg from "../assets/character/magician.png";
import balestreiroImg from "../assets/character/archer.png";

import TormGenericButton from "../components/TormGenericButton";
import "../styles/creditsStyleView.css";
import { useNavigate } from "react-router-dom";

const CreditsView = () => {
  const navigate = useNavigate();
  return (
    <main className="credits-container">
      <div
        className="animated-narrative-bg"
        style={{ backgroundImage: `url(${UnderwaterImg})` }}
      />

      <header>
        <TormGenericButton
          title="Voltar ao Menu"
          onClick={() => navigate("/")}
        />
      </header>

      <div className="credits-content">
        <div className="credit-person">
          <img src={balestreiroImg}></img>
          <h2>Ingryd</h2>
          <p>Programação</p>
        </div>
        <div className="credit-person">
          <img src={magoImg}></img>
          <h2>John</h2>
          <p>Pixel Artist and Game Designer</p>
        </div>
      </div>
    </main>
  );
};

export default CreditsView;
