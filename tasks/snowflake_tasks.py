from prefect import task
import snowflake.connector
from utils.connection import get_snowflake_connection

@task
def run_stored_procedure():
    conn = get_snowflake_connection()

    cursor = conn.cursor()

    try:
        cursor.execute("CALL process_data(%s)", ('2026-01-01',))
        result = cursor.fetchone()
        print("Stored Procedure Result:", result)

    finally:
        cursor.close()
        conn.close()