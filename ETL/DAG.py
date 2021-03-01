import os
from ETL.SFTPToS3Operator import SFTPToS3Operator
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator


ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.environ.get("AWS_DEFAULT_REGION")
BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")

dag = DAG(
            dag_id = "wineDataDag",
            start_date = days_ago(1),
            schedule_interval = "@daily"
        )


start_dag = DummyOperator(
            task_id = "StartDag",
            dag = dag
        )

download_file_1 = SFTPToS3Operator(
            task_id = "download_file_1",
            aws_access_key_id = ACCESS_KEY,
            aws_secret_access_key = SECRET_KEY,
            region_name = REGION_NAME,
            bucket_name = BUCKET_NAME,
            pkey = "*private key file path*",
            ip = "3.9.23.108",
            username = "ubuntu",
            file_to_download = "winemag-data-130k-v2.csv",
            save_as = "wine_csv_1.csv",
            dag = dag
        )


download_file_2 = SFTPToS3Operator(
            task_id = "download_file_2",
            aws_access_key_id = ACCESS_KEY,
            aws_secret_access_key = SECRET_KEY,
            region_name = REGION_NAME,
            bucket_name = BUCKET_NAME,
            pkey = "*private key file path*",
            ip = "3.9.23.108",
            username = "ubuntu",
            file_to_download = "winemag-data-130k-v2.json",
            save_as = "wine_json.json",
            dag = dag
        )


download_file_3 = SFTPToS3Operator(
            task_id = "download_file_3",
            aws_access_key_id = ACCESS_KEY,
            aws_secret_access_key = SECRET_KEY,
            region_name = REGION_NAME,
            bucket_name = BUCKET_NAME,
            pkey = "*private key file path*",
            ip = "3.9.23.108",
            username = "ubuntu",
            file_to_download = "winemag-data_first150k.csv",
            save_as = "wine_csv_2.csv",
            dag = dag
        )


transform = BashOperator(
            task_id = "transform",
            bash_command = "python3 /usr/local/airflow/dags/ETL/transform.py",
            dag = dag
        )

load = BashOperator(
            task_id = "load",
            bash_command = "python3 /usr/local/airflow/dags/ETL/load.py"
        )


start_dag >> [download_file_1, download_file_2, download_file_3] >> transform >> load









