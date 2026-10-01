import os

from airflow.exceptions import AirflowFailException
from airflow.sdk import Param, dag, task


@dag(
    dag_id="mlflow_model_trigger",
    schedule=None,
    start_date=None,
    catchup=False,
    tags=["mlops", "mlflow"],
    params={
        "model_name": Param("", type="string"),
        "model_version": Param("latest", type="string"),
        "input_data": Param({}, type=["object", "null"]),
    },
)
def mlflow_model_trigger():
    @task
    def resolve_params(**context) -> dict:
        params = context["params"]
        if not params.get("model_name"):
            raise AirflowFailException(
                "model_name is required. Trigger with conf={'model_name': ..., "
                "'model_version': ..., 'input_data': ...}"
            )
        return params

    @task
    def run_model(params: dict) -> dict:
        import mlflow

        tracking_uri = os.environ["MLFLOW_TRACKING_URI"]
        mlflow.set_tracking_uri(tracking_uri)

        model_name = params["model_name"]
        model_version = params["model_version"]
        input_data = params["input_data"] or {}

        model_uri = f"models:/{model_name}/{model_version}"
        model = mlflow.pyfunc.load_model(model_uri)
        predictions = model.predict(input_data)
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

        with mlflow.start_run(run_name="airflow-trigger"):
            mlflow.set_tag("source", "airflow")
            mlflow.log_param("model_uri", result["model_uri"])
            mlflow.log_metric("prediction_count", len(result["predictions"]))

        print(f"Model: {result['model_uri']}")
        print(f"Predictions: {result['predictions']}")

    log_result(run_model(resolve_params()))


mlflow_model_trigger()
