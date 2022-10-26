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
...bash
|   README.md
|   tree.txt
|
+---dags
|       create_tables.sql
|       create_tables_dag.py
|       create_tables_dag.txt
|       load_from_s3_into_redshift_dag.py
|
+---images
|       staging_tables.png
|       star_schema.png
|
\---plugins
    |   __init__.py
    |
    +---helpers
    |       .DS_Store
    |       sql_queries.py
    |       __init__.py
    |
    \---operators
            .DS_Store
            data_quality.py
            load_dimension.py
            load_fact.py
            stage_redshift.py
            __init__.py        
...

## Project steps
- 
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

## How to run
- 
