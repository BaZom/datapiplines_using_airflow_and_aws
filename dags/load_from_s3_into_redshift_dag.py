from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator
from airflow.operators import PostgresOperator


from helpers import SqlQueries

default_args = {
    'owner': 'Basem Abughallya',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'start_date': datetime(2022, 5, 12)
}

dag = DAG('udac_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='* * 0 0 *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_task = PostgresOperator(
    task_id="create_tables_on_redshift",
    dag=dag,
    postgres_conn_id="redshift",
    sql='create_tables.sql'
    
)
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table="staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_path="s3://udacity-dend/log_data/2018/11/"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table="staging_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_path="s3://udacity-dend/song_data/A/A/A/",
)


load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='songplays',
    sql_stmt=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='users',
    sql_stmt=SqlQueries.user_table_insert,
    append_only=False
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='songs',
    sql_stmt=SqlQueries.song_table_insert,
    append_only=False
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='artists',
    sql_stmt=SqlQueries.artist_table_insert,
    append_only=False
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table='time',
    sql_stmt=SqlQueries.time_table_insert,
    append_only=False
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    checks={
        "check_not_null_coloumn":
        [
            {
                "check_statement": "SELECT count(*) FROM udacity.public.artists where artistid is null",
                "table": "artists",
                "column": "artistid",
                "expected result": 0
            },
            {
                "check_statement": "SELECT count(*) FROM udacity.public.songplays where userid is null or sessionid is null",
                "table": "songplays",
                "column": "userid and sessionid",
                "expected result": 0
            },
            {
                "check_statement": "SELECT count(*) FROM udacity.public.songs where songid is null",
                "table": "songs",
                "column": "songid",
                "expected result": 0
            },
            {
                "check_statement": "SELECT count(*) FROM udacity.public.users where userid is null",
                "table": "userid",
                "column": "artistid",
                "expected result": 0
            }
        ]
    }
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables_task >> [stage_events_to_redshift , stage_songs_to_redshift] >> load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks >> end_operator