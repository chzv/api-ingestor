import json
from typing import Optional

from psycopg2.extras import Json
from .config import Config
from .db import get_conn
from .fetcher import FetchResult


def save(cfg: Config, fr: FetchResult) -> int:
    with get_conn(cfg) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO requests (endpoint, params, status_code, duration_ms, error)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    fr.endpoint,
                    Json(fr.params),
                    fr.status_code,
                    fr.duration_ms,
                    fr.error,
                ),
            )
            request_id = int(cur.fetchone()["id"])

            if fr.error is None and fr.json_data is not None:
                cur.execute(
                    """
                    INSERT INTO responses (request_id, temperature_2m, wind_speed_10m, raw_json)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        request_id,
                        fr.temperature_2m,
                        fr.wind_speed_10m,
                        Json(fr.json_data),
                    ),
                )

            return request_id
