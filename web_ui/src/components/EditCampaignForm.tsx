import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getCampaignById, updateCampaign } from "../api";

export default function EditCampaignForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getCampaignById(id!)
      .then(setForm)
      .catch(() => setError("Failed to load campaign"));
  }, [id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, type, value, checked } = e.target;
    const parsedValue =
      type === "number" ? parseFloat(value) :
      type === "checkbox" ? checked : value;

    setForm({ ...form, [name]: parsedValue });
  };

  const handleNestedChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      targeting_rules: {
        ...form.targeting_rules,
        [name]: value,
      },
    });
  };

  const handleSubmit = async () => {
    try {
      await updateCampaign(id!, form);
      navigate("/");
    } catch {
      setError("Failed to save changes");
    }
  };

  if (error) return <p className="text-red-600">{error}</p>;
  if (!form) return <p>Loading...</p>;

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold">Edit Campaign</h2>

      {Object.entries(form).map(([key, value]) => {
        if (key === "targeting_rules" && typeof value === "object" && value !== null) {
          return (
            <div key={key} className="flex flex-col gap-2">
              <label className="text-sm font-semibold">Targeting Rules</label>

              <div>
                <label className="text-sm text-gray-600">Geo:</label>
                <select
                  name="geo"
                  value={value.geo || ""}
                  onChange={handleNestedChange}
                  className="border rounded p-2 w-full"
                >
                  <option value="">Select country</option>
                  <option value="US">US</option>
                  <option value="UK">UK</option>
                  <option value="DE">Germany</option>
                  <option value="IL">Israel</option>
                </select>
              </div>

              <div>
                <label className="text-sm text-gray-600">Device:</label>
                <select
                  name="device"
                  value={value.device || ""}
                  onChange={handleNestedChange}
                  className="border rounded p-2 w-full"
                >
                  <option value="">Select device</option>
                  <option value="mobile">Mobile</option>
                  <option value="desktop">Desktop</option>
                  <option value="tablet">Tablet</option>
                </select>
              </div>
            </div>
          );
        }

        const type =
          key === "click_url" ? "url" :
          key.includes("time") ? "datetime-local" :
          typeof value === "boolean" ? "checkbox" :
          typeof value === "number" ? "number" :
          "text";

        return (
          <div key={key} className="flex flex-col">
            <label className="text-sm text-gray-600 capitalize">{key}</label>
            <input
              className="border p-2 rounded"
              name={key}
              type={type}
              value={type === "checkbox" ? undefined : value}
              checked={type === "checkbox" ? value : undefined}
              onChange={handleChange}
            />
          </div>
        );
      })}

      <button
        onClick={handleSubmit}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Save
      </button>
    </div>
  );
}
