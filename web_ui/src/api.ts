export async function login(username: string, password: string): Promise<boolean> {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.ok;
}

export async function getCampaigns(): Promise<any[]> {
  const res = await fetch("/api/campaigns/secure", {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Unauthorized");
  return res.json();
}

export async function getCampaignById(id: string): Promise<any> {
  const res = await fetch(`/api/campaigns/${id}`, {
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to fetch campaign");
  return res.json();
}

export async function updateCampaign(id: string, data: any): Promise<any> {
  const res = await fetch(`/api/campaigns/${id}`, {
    method: "PUT",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update campaign");
  return res.json();
}