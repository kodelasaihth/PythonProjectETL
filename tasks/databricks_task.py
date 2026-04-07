from prefect import task, get_run_logger
import requests
import os
import time


@task(retries=2, retry_delay_seconds=60)
def run_databricks_job():
    logger = get_run_logger()

    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")
    job_id = os.getenv("DATABRICKS_JOB_ID")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    logger.info("Triggering Databricks job...")

    response = requests.post(
        f"{host}/api/2.1/jobs/run-now",
        headers=headers,
        json={"job_id": int(job_id)}
    )

    if response.status_code != 200:
        raise Exception(f"Failed to trigger job: {response.text}")

    run_id = response.json()["run_id"]
    logger.info(f"Databricks job triggered. Run ID: {run_id}")

    # -----------------------------
    # Poll job status
    # -----------------------------
    while True:
        status_resp = requests.get(
            f"{host}/api/2.1/jobs/runs/get",
            headers=headers,
            params={"run_id": run_id}
        )

        state = status_resp.json()["state"]["life_cycle_state"]
        result = status_resp.json()["state"].get("result_state")

        logger.info(f"Job Status: {state}")

        if state == "TERMINATED":
            if result == "SUCCESS":
                logger.info("Databricks job completed successfully!")
                return True
            else:
                raise Exception(f"Job failed with result: {result}")

        time.sleep(20)