# datapiplines_using_airflow_and_aws
Datapipelines project submission for Udacity Data Engineer for AI Applications Nanodegree

## Introduction
This project aims create an airflow pipline for extracting songs metadata and user activity data from JSON  files residing in an AWS S3 bucket and save them in a database star schema in AWS redshift. 

## Project Dataset
The following two datasets used in this project are two subsets of real data from the [Million Song Dataset](http://millionsongdataset.com/) and of generated data by this [event simulator](https://github.com/Interana/eventsim).

AWS S3 links for each:
-   Song data: `s3://udacity-dend/song_data`
-   Log data: `s3://udacity-dend/log_data`

Log data json path: `s3://udacity-dend/log_json_path.json`

## Project files
   - __dags__
     - [create\_tables.sql](dags/create_tables.sql) contains sql queries to create the star schema and the staging tables 
     - [create\_tables\_dag.py](dags/create_tables_dag.py) dag for creating the star schema and the staging tables on redshift
     - [load\_from\_s3\_into\_redshift\_dag.py](dags/load_from_s3_into_redshift_dag.py) dag for loading data from s3 into redshift and doing quality checks
   - __images__
     - [create\_tables\_dag\_graph.JPG](images/create_tables_dag_graph.JPG) airflow dag graph for creating tables
     - [etl\_graph.JPG](images/etl_graph.JPG) airflow etl graph
     - [staging\_tables.png](images/staging_tables.png) staging tables
     - [star\_schema.png](images/star_schema.png) star schema tables
   - __plugins__
     - [\_\_init\_\_.py](plugins/__init__.py)
     - __helpers__
       - [\_\_init\_\_.py](plugins/helpers/__init__.py)
       - [sql\_queries.py](plugins/helpers/sql_queries.py) sql queries for inserting data into fact and dimension tables
     - __operators__
       - [\_\_init\_\_.py](plugins/operators/__init__.py)
       - [data\_quality.py](plugins/operators/data_quality.py) customized operator for quality checks
       - [load\_dimension.py](plugins/operators/load_dimension.py) customized operator for loading data into dimension tables
       - [load\_fact.py](plugins/operators/load_fact.py) customized operator for loading data into fact table
       - [stage\_redshift.py](plugins/operators/stage_redshift.py) customized operator for loading data into staging tables
   - [README.md](README.md)

## Staging tables

![enter image description here](https://github.com/BaZom/Data-warehouse-with-AWS-S3-and-Redshift/blob/4361dc1f49353701d142e70bcecdf2d2b8fe0633/staging_tables.png)

## Star schema tables
![enter image description here](https://github.com/BaZom/Data-warehouse-with-AWS-S3-and-Redshift/blob/848476c6f991f098374eba1e0247dcb8d3350468/star_schema.png)

## Schema Design
- The data is loaded in a star schema with a fact table having foreign keys to four dimensional tables
- user_id from table songplays is used as a redshift distribution key.
- The primary key of each dimensional table is used as a sorting key for that table.
## Dags
### create tables dag
![create tables dag](https://github.com/BaZom/datapiplines_using_airflow_and_aws/blob/main/images/create_tables_dag_graph.JPG)

### etl dag
![etl dag](https://github.com/BaZom/datapiplines_using_airflow_and_aws/blob/main/images/etl_graph.JPG)

## Project steps
-  creating dag for creating tables
- implementing the etl dag with the needed customized operators
## How to run
__Create an IAM User in AWS__
   - Needed Permissions: AdministratorAccess, AmazonS3FullAccess and AmazonRedshiftDataFullAccess 
__Create a redshift cluster in AWS__
   - Ensure that you are creating this cluster in the us-west-2 region. This is important as the s3-bucket that we are going to use for this project is in us-west-2.

__Setting up Connections__
   - Connect Airflow and AWS: connection ID is "aws_credentials"
   - Connect Airflow to the AWS Redshift Cluster: connection ID is "redshift"

__Run [create\_tables\_dag.py](dags/create_tables_dag.py)__
__Run [load\_from\_s3\_into\_redshift\_dag.py](dags/load_from_s3_into_redshift_dag.py)__
