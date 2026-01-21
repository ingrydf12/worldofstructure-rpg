import "./App.css";
import TormGenericButton from "./components/TormGenericButton";
import { IoPlayOutline } from "react-icons/io5";
import { AiFillBug } from "react-icons/ai";
import { BsHeadsetVr } from "react-icons/bs";
import forestImg from "./assets/bg/durotar_wpp.png";

function App() {
  return (
    <main className="container">
      <div className="animated-home-bg">
        <img src={forestImg} alt="Floresta sombria" className="animated-bg" />
      </div>

      <h1><b>World of TormStructure</b></h1>
      <h2>RPG baseado em Tormenta para Estrutura de Dados - SMD</h2>

      <div className="vertical-buttons-menu">
        <TormGenericButton
          title="Iniciar jogo"
          btnIcon={<IoPlayOutline />}
          path="/build-character"
        />        
        <TormGenericButton title="Suas runs" btnIcon={<BsHeadsetVr />} path="/runs"/>
        <TormGenericButton title="Créditos" btnIcon={<AiFillBug />} path="/credits" />
      </div>
    </main>
  );
}

export default App;
