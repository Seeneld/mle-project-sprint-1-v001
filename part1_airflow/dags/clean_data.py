from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'mle-user',
    'depends_on_past': False,
    'start_date': datetime(2026, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='clean_real_estate_data',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['project', 'stage2'],
) as dag:

    @task
    def create_clean_table():
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        sql = """
            DROP TABLE IF EXISTS cleaned_flats;
            CREATE TABLE cleaned_flats AS
            SELECT * FROM merged_flats WHERE 1=0;
        """
        pg_hook.run(sql)
        return "Table cleaned_flats created"

    @task
    def clean_and_load():
        import pandas as pd
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from cleaning_functions import clean_data
        
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        engine = pg_hook.get_sqlalchemy_engine()
        
        df = pd.read_sql("SELECT * FROM merged_flats", engine)
        df_clean = clean_data(df)
        
        df_clean.to_sql('cleaned_flats', engine, if_exists='replace', index=False)
        return f"Loaded {len(df_clean)} cleaned rows"

    t1 = create_clean_table()
    t2 = clean_and_load()

    t1 >> t2