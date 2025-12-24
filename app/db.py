import psycopg2
from psycopg2.extras import RealDictCursor


def run_query(query: str, params: tuple = ()):
    conn = psycopg2.connect(
        host="localhost",
        database="clinical",
        user="postgres",
        password="postgres"
    )
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()