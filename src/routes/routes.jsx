import { Routes, Route } from "react-router-dom";

import BuildCharacter from "../screens/BuildCharacter";
import NarrativeScreen from "../screens/NarrativeScreen";
import MyRunsView from "../screens/MyRunsView";
import CreditsView from "../screens/CreditsView";
import { CombatScreenView } from "../screens/CombatScreenView";
import AppLayout from "../layout/useLayout";
import App from "../App";

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<App />} />
        <Route path="/build-character" element={<BuildCharacter />} />
        <Route path="/narrative-game-screen" element={<NarrativeScreen />} />
        <Route path="/combat" element={<CombatScreenView />} />
        <Route path="/runs" element={<MyRunsView />} />
        <Route path="/credits" element={<CreditsView />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
