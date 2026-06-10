import os
import psycopg2


class Database:
    _conn = None

    @classmethod
    def get_connection(cls):
        if cls._conn is None or cls._conn.closed != 0:
            cls._conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "5433")),
                dbname=os.getenv("DB_NAME", "heroes_db"),
                user=os.getenv("DB_USER", "heroes"),
                password=os.getenv("DB_PASSWORD", "heroes123"),
            )
        return cls._conn

    @classmethod
    def close(cls):
        if cls._conn and cls._conn.closed == 0:
            cls._conn.close()
            cls._conn = None
