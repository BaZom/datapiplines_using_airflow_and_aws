from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 checks =[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.checks = checks

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        for check_dict in self.checks['check_not_null_coloumn']:
            records = redshift_hook.get_records(check_dict['check_statement'])
            if records[0][0] != check_dict['expected result']:
                raise ValueError(f"Data quality check failed. {check_dict['table']} contained null values for {check_dict['column']}")
            self.log.info(f"Data quality on table {check_dict['table']} check passed with not null {check_dict['column']} records")