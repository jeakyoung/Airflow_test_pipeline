from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="test_schedule_3min",
    schedule="*/3 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["test", "schedule"],
)
def test_schedule_3min():
    @task
    def print_run_time(**context):
        print(f"Triggered at: {datetime.now()}")
        print(f"Logical date: {context['logical_date']}")
        print(f"Run id: {context['run_id']}")

    print_run_time()


test_schedule_3min()
