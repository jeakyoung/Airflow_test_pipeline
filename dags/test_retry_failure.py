from datetime import datetime, timedelta

from airflow.sdk import dag, task


def alert_on_failure(context):
    ti = context["ti"]
    print(
        f"ALERT: {ti.task_id} failed permanently after {ti.try_number - 1} retries "
        f"(run_id={ti.run_id})"
    )


@dag(
    dag_id="test_retry_failure",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["test"],
)
def test_retry_failure():
    @task(
        retries=2,
        retry_delay=timedelta(seconds=10),
        on_failure_callback=alert_on_failure,
    )
    def always_fails():
        raise RuntimeError("Intentional failure for retry testing")

    always_fails()


test_retry_failure()
