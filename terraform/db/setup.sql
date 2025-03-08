-- Create campaigns table with automatic timestamps
CREATE TABLE IF NOT EXISTS campaigns (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  budget_usd DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  active BOOLEAN NOT NULL DEFAULT false,
  cap_daily INTEGER,
  cap_hourly INTEGER,
  country_filters TEXT[],
  language_filters TEXT[],
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by VARCHAR(255) NOT NULL
);

-- Create trigger for automatic updated_at timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON campaigns
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Insert default row with active set to false
INSERT INTO campaigns (name, description, budget_usd, active, cap_daily, cap_hourly, country_filters, language_filters, updated_by)
VALUES ('Default Campaign', 'Initial campaign created by Terraform', 1000.00, false, 1000, 100, ARRAY['US', 'CA'], ARRAY['en'], 'terraform-init')
ON CONFLICT DO NOTHING;