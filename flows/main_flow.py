from prefect import flow, task, get_run_logger
import subprocess
from tasks.snowflake_tasks import run_stored_procedure
from tasks.databricks_task import run_databricks_job
from utils.connection import get_snowflake_connection


# ----------------------------- # Task: Run Stored Procedure # -----------------------------
@task(retries=2, retry_delay_seconds=30)
def run_stored_procedure():
    logger = get_run_logger()
    logger.info("Executing Snowflake stored procedure...")
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("CALL process_data()")
        result = cursor.fetchone()
        logger.info(f"Stored Procedure Result: {result}")
    finally:
        cursor.close()
        conn.close()

# 🔹 Task 1: Check if new data exists
@task(retries=2, retry_delay_seconds=30)
def check_new_data():
    logger = get_run_logger()
    conn = get_snowflake_connection()
    cur = conn.cursor()

    # Example: check last 5 minutes data
    cur.execute("""
        SELECT COUNT(*)
        FROM userdata
        -- WHERE created_at >= DATEADD(minute, -5, CURRENT_TIMESTAMP)
    """)

    count = cur.fetchone()[0]
    logger.info(f"New rows found: {count}")

    return count > 0


# 🔹 Task 2: Run dbt models
@task(retries=2, retry_delay_seconds=60)
def run_dbt():
    logger = get_run_logger()

    logger.info("Running dbt models...")

    subprocess.run(
        ["dbt", "run"],
        cwd="./dbt",
        check=True
    )

    subprocess.run(
        ["dbt", "test"],
        cwd="./dbt",
        check=True
    )

    logger.info("dbt run completed")


# 🔹 Task 3: Send alert (basic)
@task
def send_alert(message):
    logger = get_run_logger()
    logger.error(f"ALERT: {message}")


# 🔹 Main Flow
@flow(name="snowflake-etl-pipeline")
def main_flow():
    logger = get_run_logger()

    try:
        has_data = check_new_data()

        if has_data:
            logger.info("New data detected. Running pipeline...")
            run_dbt()
            run_stored_procedure()
        else:
            logger.info("No new data. Skipping run.")

    except Exception as e:
        send_alert(str(e))
        raise


if __name__ == "__main__":
    main_flow()