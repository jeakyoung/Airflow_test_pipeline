from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="test_pipeline",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["test"],
)
def test_pipeline():
    @task
    def extract():
        return {"a": 1, "b": 2, "c": 3}

    @task
    def transform(data: dict):
        return {k: v * 10 for k, v in data.items()}

    @task
    def load(data: dict):
        print(f"Loaded: {data}")

    load(transform(extract()))


test_pipeline()
