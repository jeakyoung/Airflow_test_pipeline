import os
from datetime import datetime

from airflow.exceptions import AirflowFailException
from airflow.models import Variable
from airflow.sdk import dag, task


@dag(
    dag_id="mlflow_model_schedule",
    schedule="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["mlops", "mlflow"],
)
def mlflow_model_schedule():
    @task
    def fetch_config() -> dict:
        model_name = Variable.get("mlflow_model_name", default_var="")
        if not model_name:
            raise AirflowFailException(
                "Airflow Variable 'mlflow_model_name' is not set."
            )
        return {
            "model_name": model_name,
            "model_version": Variable.get("mlflow_model_version", default_var="latest"),
            "input_data": Variable.get(
                "mlflow_input_data", default_var={}, deserialize_json=True
            ),
        }

    @task
    def run_model(params: dict) -> dict:
        import mlflow

        tracking_uri = os.environ["MLFLOW_TRACKING_URI"]
        mlflow.set_tracking_uri(tracking_uri)

        model_uri = f"models:/{params['model_name']}/{params['model_version']}"
        model = mlflow.pyfunc.load_model(model_uri)
        predictions = model.predict(params["input_data"])
        predictions = (
            predictions.tolist() if hasattr(predictions, "tolist") else predictions
        )

        return {
            "model_uri": model_uri,
            "predictions": predictions,
        }

    @task
    def log_result(result: dict) -> None:
        import mlflow

        with mlflow.start_run(run_name="airflow-schedule"):
            mlflow.set_tag("source", "airflow")
            mlflow.log_param("model_uri", result["model_uri"])
            mlflow.log_metric("prediction_count", len(result["predictions"]))

        print(f"Model: {result['model_uri']}")
        print(f"Predictions: {result['predictions']}")

    log_result(run_model(fetch_config()))


mlflow_model_schedule()
