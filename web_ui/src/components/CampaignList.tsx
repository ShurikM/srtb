import { useEffect, useState } from "react";
import { getCampaigns } from "../api";
import CampaignCard from "./CampaignCard";

export default function CampaignList() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getCampaigns()
      .then(setCampaigns)
      .catch(() => setError("Failed to load campaigns"));
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h2 className="text-2xl font-bold mb-6">Campaigns</h2>
      {error && <p className="text-red-600">{error}</p>}
      <div className="grid gap-4 md:grid-cols-2">
        {campaigns.map((c) => (
          <CampaignCard key={c.id || c.crid} campaign={c} />
        ))}
      </div>
    </div>
  );
}
