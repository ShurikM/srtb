-- Create campaigns table with updated schema
CREATE TABLE IF NOT EXISTS campaigns (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  domain VARCHAR(255) NOT NULL,
  price NUMERIC(10, 4) NOT NULL,
  crid VARCHAR(255) NOT NULL,
  adm TEXT NOT NULL,
  click_url TEXT,
  budget NUMERIC(12, 2),
  bid_floor NUMERIC(10, 4),
  impression_limit INTEGER,
  targeting_rules JSONB,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON campaigns;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON campaigns
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Insert one example campaign
INSERT INTO campaigns (
  name, domain, price, crid, adm, click_url, budget, bid_floor,
  impression_limit, targeting_rules, start_time, end_time, is_active
)
VALUES (
  'Default Campaign',
  'example.com',
  0.50,
  'creative-123',
  '<!-- Sample Creative -->',
  'https://example.com/click',
  1000.00,
  0.10,
  100000,
  '{"geo": ["US", "CA"], "lang": ["en"]}',
  NOW(),
  NOW() + INTERVAL '30 days',
  true
)
ON CONFLICT DO NOTHING;
