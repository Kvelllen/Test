import psycopg2

# Project packages
from config import DATABASE_CONFIG


def get_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

def execute_query(sql_script, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script, params)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []

def execute_non_query(sql_script, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script, params)
                conn.commit()
    except Exception as e:
        print(f"Error executing non-query: {e}")