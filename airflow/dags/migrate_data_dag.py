from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook
from pendulum import datetime
from datetime import timedelta
from airflow import DAG


def migrate_vehicles_table():
    '''
    A function to migrate data from postgres to MySQL database
    '''
    src = PostgresHook(postgres_conn_id="pg_server")
    target = MySqlHook(mysql_conn_id="mysql_conn")
    src_conn = src.get_conn()
    cursor = src_conn.cursor()

    cursor.execute("SELECT * FROM vehicles")
    sources = cursor.fetchall()
    target.insert_rows(table="vehicles", rows=sources,
                       replace=True, replace_index="id")


def migrate_trajectories_table():
    '''
    A function to migrate data from postgres to MySQL database
    '''
    src = PostgresHook(postgres_conn_id="pg_server")
    target = MySqlHook(mysql_conn_id="mysql_conn")
    src_conn = src.get_conn()
    cursor = src_conn.cursor()

    cursor.execute("SELECT * FROM trajectories")
    sources = cursor.fetchall()
    target.insert_rows(table="trajectories", rows=sources,
                       replace=True, replace_index="id")


default_args = {
    'owner': 'tewodros',
    'depends_on_past': False,
    'email': ['teddylnk1@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'start_date': datetime(2022, 7, 22),
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    "Migrate_data_from_PostgreSQL_to_MySQL",
    description="A data migration DAG from Postgres to MySQL database.",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
) as dag:

    create_table_vehicle = MySqlOperator(
        task_id="create_table",
        mysql_conn_id="mysql_conn",
        sql='./scripts/vehicle_data_schema.sql'
    )
    migrate_data_vehicles = PythonOperator(task_id="migrate_data",
                                  python_callable=migrate_vehicles_table)
    create_table_trajectories = MySqlOperator(
        task_id="create_table",
        mysql_conn_id="mysql_conn",
        sql='./scripts/trajectories_data_schema.sql'
    )
    migrate_data_trajectories = PythonOperator(task_id="migrate_data",
        python_callable=migrate_trajectories_table)


create_table_vehicle >> migrate_data_vehicles >> create_table_trajectories >> migrate_data_trajectories
