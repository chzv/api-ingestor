import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    fetch_interval_minutes: int
    http_timeout_seconds: int

    api_base_url: str
    latitude: float
    longitude: float
    timezone: str

    error_log_path: str


def get_config() -> Config:
    return Config(
        postgres_db=os.getenv("POSTGRES_DB", "app"),
        postgres_user=os.getenv("POSTGRES_USER", "app"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", "app"),
        postgres_host=os.getenv("POSTGRES_HOST", "db"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        fetch_interval_minutes=int(os.getenv("FETCH_INTERVAL_MINUTES", "5")),
        http_timeout_seconds=int(os.getenv("HTTP_TIMEOUT_SECONDS", "10")),
        api_base_url=os.getenv("API_BASE_URL", "https://api.open-meteo.com/v1/forecast"),
        latitude=float(os.getenv("LATITUDE", "55.7558")),
        longitude=float(os.getenv("LONGITUDE", "37.6176")),
        timezone=os.getenv("TIMEZONE", "UTC"),
        error_log_path=os.getenv("ERROR_LOG_PATH", "/app/logs/errors.log"),
    )
