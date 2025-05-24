import { useEffect, useState } from "react";
import { getCampaigns } from "../api";
import { useNavigate } from "react-router-dom";

export default function CampaignList() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    getCampaigns()
      .then(setCampaigns)
      .catch(() => setError("Failed to load campaigns"));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Campaigns</h2>
      {error && <p className="text-red-600">{error}</p>}
      <ul className="space-y-2">
        {campaigns.map((c) => (
          <li key={c.id || c.crid} className="p-2 border rounded flex justify-between items-center">
            <div>
              <strong>{c.name || c.crid}</strong> – ${c.price}
            </div>
            <button
              onClick={() => navigate(`/campaigns/${c.id || c.crid}/edit`)}
              className="bg-blue-600 text-white px-3 py-1 rounded"
            >
              Edit
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
