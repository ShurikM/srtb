interface Campaign {
  id: string;
  crid: string;
  adm: string;
  price: number;
  click_url: string;
  targeting_rules: Record<string, string>;
  budget: number;
  is_active: boolean;
  daily_cap: number;
  hourly_cap: number;
  impression_timestamps: string[];
  last_impression_at: string | null;
}

export default function CampaignCard({ campaign }: { campaign: Campaign }) {
  return (
    <div className="border rounded shadow p-4 space-y-2 bg-white">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-bold text-blue-700">{campaign.crid}</h3>
        <span className={`text-sm font-semibold px-2 py-1 rounded ${campaign.is_active ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
          {campaign.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>

      <p>Price: <strong>${campaign.price.toFixed(2)}</strong></p>
      <p>Budget: ${campaign.budget.toLocaleString()}</p>
      <p>Daily Cap: {campaign.daily_cap}</p>
      <p>Hourly Cap: {campaign.hourly_cap}</p>

      <div>
        <strong>Targeting Rules:</strong>
        <ul className="list-disc ml-6 text-sm text-gray-700">
          {Object.entries(campaign.targeting_rules).map(([key, value]) => (
            <li key={key}>{key}: {value}</li>
          ))}
        </ul>
      </div>

      <p className="text-sm text-gray-600">
        Last Impression:{' '}
        {campaign.last_impression_at
          ? new Date(campaign.last_impression_at).toLocaleString()
          : 'None yet'}
      </p>

      <a
        href={campaign.click_url}
        className="text-blue-500 underline"
        target="_blank"
        rel="noopener noreferrer"
      >
        Visit Ad
      </a>
    </div>
  );
}
