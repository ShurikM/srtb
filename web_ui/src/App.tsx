import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import CampaignList from "./components/CampaignList";
import CampaignDetails from "./components/CampaignDetails";
import EditCampaignForm from "./components/EditCampaignForm";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <BrowserRouter>
      <Routes>
        {!loggedIn ? (
          <Route path="*" element={<LoginPage onLogin={() => setLoggedIn(true)} />} />
        ) : (
          <>
            <Route path="/" element={<CampaignList />} />
            <Route path="/campaigns/:id" element={<CampaignDetails />} />
            <Route path="/campaigns/:id/edit" element={<EditCampaignForm />} />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
