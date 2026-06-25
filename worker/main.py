import os
import time

import psycopg
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://marmitia:secret@localhost:5432/marmitia"
)

cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def preparer_db():
    """Attend que la db réponde, puis crée la table de battements."""
    while True:
        try:
            with psycopg.connect(DATABASE_URL) as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS battement ("
                    "id SERIAL PRIMARY KEY, vu_le TIMESTAMPTZ DEFAULT now())"
                )
            return
        except psycopg.OperationalError:
            print("db pas prête, nouvelle tentative dans 2s...", flush=True)
            time.sleep(2)


def main():
    preparer_db()
    cache.ping()  # prouve qu'on joint aussi Redis
    print("worker prêt (squelette) — un battement toutes les 10s", flush=True)
    while True:
        with psycopg.connect(DATABASE_URL) as conn:
            conn.execute("INSERT INTO battement DEFAULT VALUES")
        print("battement", flush=True)
        time.sleep(10)


if __name__ == "__main__":
    main()