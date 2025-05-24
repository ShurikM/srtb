import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function CampaignDetails() {
  const { id } = useParams();
  const [campaign, setCampaign] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
  fetch(`/api/campaigns/${id}`, {
    credentials: "include",
  })
    .then((res) => {
      console.log("📡 Response status:", res.status);
      if (!res.ok) throw new Error("Campaign not found");
      return res.json();
    })
    .then((data) => {
      console.log("✅ Campaign data:", data);
      setCampaign(data);
    })
    .catch((err) => {
      console.error("❌ Error loading campaign:", err);
      setError("Failed to load campaign details");
    });
}, [id]);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!campaign) return <p>Loading...</p>;

  return (
    <div className="p-6 space-y-2 bg-white rounded shadow max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">{campaign.crid}</h2>
      <p><strong>Price:</strong> ${campaign.price}</p>
      <p><strong>Budget:</strong> ${campaign.budget}</p>
      <p><strong>Daily Cap:</strong> {campaign.daily_cap}</p>
      <p><strong>Hourly Cap:</strong> {campaign.hourly_cap}</p>
      <p><strong>Status:</strong> {campaign.is_active ? "Active" : "Inactive"}</p>
      <p><strong>Click URL:</strong> <a href={campaign.click_url} className="text-blue-600 underline" target="_blank" rel="noreferrer">{campaign.click_url}</a></p>
      <div>
        <strong>Targeting Rules:</strong>
        <ul className="list-disc ml-6">
          {Object.entries(campaign.targeting_rules).map(([k, v]) => (
            <li key={k}>{k}: {v}</li>
          ))}
        </ul>
      </div>
      <p><strong>Last Impression:</strong> {campaign.last_impression_at ? new Date(campaign.last_impression_at).toLocaleString() : "None"}</p>
    </div>
  );
}
