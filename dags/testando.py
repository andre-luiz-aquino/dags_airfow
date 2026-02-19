from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="testtee",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["docker"],
) as dag:

    run_container = KubernetesPodOperator(
        task_id="run_dockerhub_image",
        name="run-dockerhub-image",
        namespace="airflow",
        image="seuusuario/sua-imagem:latest",
        image_pull_policy="Always",
        get_logs=True,
        is_delete_operator_pod=True,
    )

    run_container
