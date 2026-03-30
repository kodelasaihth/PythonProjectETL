from prefect import flow, task, get_run_logger
import subprocess
import os
import snowflake.connector


# 🔹 Task 1: Check if new data exists
@task(retries=2, retry_delay_seconds=30)
def check_new_data():
    logger = get_run_logger()

    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WH"),
        database=os.getenv("SNOWFLAKE_DB"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

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
        else:
            logger.info("No new data. Skipping run.")

    except Exception as e:
        send_alert(str(e))
        raise


if __name__ == "__main__":
    main_flow()