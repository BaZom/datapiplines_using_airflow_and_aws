from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (PostgresOperator, PythonOperator)
from airflow.hooks.postgres_hook import PostgresHook
import logging



from helpers import SqlQueries

table_exist_sql = """
    SELECT EXISTS (
       SELECT * FROM pg_tables
       WHERE  schemaname = 'public'
       AND    tablename   = '{}'
       );
"""

def check_table_exists(*args, **kwargs):
    tables = kwargs["params"]["tables"]
    redshift_hook = PostgresHook("redshift")

    for table in tables:
        records = redshift_hook.get_records(table_exist_sql.format(table))
        if records[0][0] != True:
                raise ValueError(f"{table} does not exist")
        logging.info(f"{table} exists")


default_args = {
    'owner': 'Basem Abughallya',
    'start_date': datetime.now()
}

dag = DAG('create_tables_dag',
          default_args=default_args,
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_task = PostgresOperator(
    task_id="create_tables_on_redshift",
    dag=dag,
    postgres_conn_id="redshift",
    sql='create_tables.sql'
    
)

run_quality_checks = PythonOperator(
    task_id='check_table_created_and_empty',
    dag=dag,
    python_callable=check_table_exists,
    provide_context=True,
    params={
        'tables': ['artists','users','songs','songplays','staging_events','staging_songs','time'],
    }
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables_task >> run_quality_checks >> end_operator