from datetime import datetime, timedelta

from airflow import DAG

from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.models import Variable


# Definição padrão de argumentos das tasks
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="integracao_btc",
    description="DAG que executa um container com imagem do Docker Hub",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/5 * * * *",  # roda a cada 5 minutos
    catchup=False,
    default_args=default_args,
    tags=["docker", "kubernetes"],
) as dag:


    # Recupera a credencial da variável do Airflow

    db_dsn = Variable.get("DB_DSN")

    executar_container = KubernetesPodOperator(
        task_id="executar_integracao_btc",
        name="executar-integracao-btc",
        namespace="airflow",  # ajuste se seu namespace for outro
        image="andreaquino/integracao_btc:latest",  # imagem correta
        image_pull_policy="Always",
        get_logs=True,
        is_delete_operator_pod=True,  # remove o pod após terminar
        env_vars={
            "DB_DSN": db_dsn,
        },  # passa apenas DB_DSN como variável de ambiente
    )

    executar_container
