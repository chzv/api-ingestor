import psycopg2
from psycopg2.extras import RealDictCursor
from .config import Config


def get_conn(cfg: Config):
    return psycopg2.connect(
        dbname=cfg.postgres_db,
        user=cfg.postgres_user,
        password=cfg.postgres_password,
        host=cfg.postgres_host,
        port=cfg.postgres_port,
        cursor_factory=RealDictCursor,
    )
