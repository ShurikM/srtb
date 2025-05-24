import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import CampaignList from "./components/CampaignList";
import CampaignDetails from "./components/CampaignDetails"; // ← you'll create this

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  if (!loggedIn) {
    return <LoginPage onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CampaignList />} />
        <Route path="/campaigns/:id" element={<CampaignDetails />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
