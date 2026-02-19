import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from .config import Config


@dataclass
class FetchResult:
    endpoint: str
    params: Dict[str, Any]
    status_code: Optional[int]
    duration_ms: int
    error: Optional[str]
    json_data: Optional[Dict[str, Any]]
    temperature_2m: Optional[float]
    wind_speed_10m: Optional[float]


def fetch(cfg: Config) -> FetchResult:
    params = {
        "latitude": cfg.latitude,
        "longitude": cfg.longitude,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": cfg.timezone,
    }

    start = time.perf_counter()
    status_code = None
    error = None
    json_data = None
    temperature_2m = None
    wind_speed_10m = None

    try:
        resp = requests.get(cfg.api_base_url, params=params, timeout=cfg.http_timeout_seconds)
        status_code = resp.status_code
        resp.raise_for_status()
        json_data = resp.json() if resp.content else {}

        current = (json_data or {}).get("current") or {}
        temperature_2m = _to_float(current.get("temperature_2m"))
        wind_speed_10m = _to_float(current.get("wind_speed_10m"))

    except requests.exceptions.Timeout as e:
        error = f"timeout: {e}"
    except requests.exceptions.ConnectionError as e:
        error = f"connection_error: {e}"
    except requests.exceptions.HTTPError as e:
        error = f"http_error: {e}"
    except ValueError as e:
        error = f"json_decode_error: {e}"
    except Exception as e:
        error = f"unexpected_error: {e}"

    duration_ms = int((time.perf_counter() - start) * 1000)

    return FetchResult(
        endpoint=cfg.api_base_url,
        params=params,
        status_code=status_code,
        duration_ms=duration_ms,
        error=error,
        json_data=json_data,
        temperature_2m=temperature_2m,
        wind_speed_10m=wind_speed_10m,
    )


def _to_float(v) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None
