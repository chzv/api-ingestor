CREATE TABLE IF NOT EXISTS requests (
  id BIGSERIAL PRIMARY KEY,
  requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  endpoint TEXT NOT NULL,
  params JSONB NOT NULL DEFAULT '{}'::jsonb,
  status_code INTEGER,
  duration_ms INTEGER,
  error TEXT
);

CREATE TABLE IF NOT EXISTS responses (
  id BIGSERIAL PRIMARY KEY,
  request_id BIGINT NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
  received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  temperature_2m DOUBLE PRECISION,
  wind_speed_10m DOUBLE PRECISION,
  raw_json JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_requests_requested_at ON requests (requested_at DESC);
CREATE INDEX IF NOT EXISTS idx_responses_request_id ON responses (request_id);