import logging
import os
import time

from .config import get_config
from .fetcher import fetch
from .storage import save


def setup_error_logger(path: str) -> logging.Logger:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    logger = logging.getLogger("errors")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler(path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def main() -> None:
    cfg = get_config()
    err_logger = setup_error_logger(cfg.error_log_path)

    interval_seconds = max(1, cfg.fetch_interval_minutes) * 60

    while True:
        fr = fetch(cfg)
        try:
            save(cfg, fr)
        except Exception as e:
            err_logger.error(f"db_error: {e}")

        if fr.error:
            err_logger.error(
                f"api_error: endpoint={fr.endpoint} status={fr.status_code} duration_ms={fr.duration_ms} error={fr.error}"
            )

        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
