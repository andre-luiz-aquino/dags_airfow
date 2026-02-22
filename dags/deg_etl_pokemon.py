from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator


# Definição padrão de argumentos das tasks
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="rodar_imagem_dockerhub_pokemon",
    description="DAG que executa um container com imagem do Docker Hub",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # ou por ex. '0 9 * * *' para rodar todo dia às 09h
    catchup=False,
    default_args=default_args,
    tags=["docker", "kubernetes"],
) as dag:

    executar_container = KubernetesPodOperator(
        task_id="executar_imagem_dockerhub",
        name="executar-imagem-dockerhub",
        namespace="airflow",  # ajuste se seu namespace for outro
        image="andreaquino/ingestao_pokemon:latest",  # <-- coloque aqui sua imagem
        image_pull_policy="Always",
        get_logs=True,
        is_delete_operator_pod=True,  # remove o pod após terminar
        # Se precisar passar comandos/args para o container:
        # cmds=["python", "main.py"],
        # arguments=["--param1", "valor"],
        # Se precisar de variáveis de ambiente:
        # env_vars={"AMBIENTE": "producao"},
    )

    executar_container
