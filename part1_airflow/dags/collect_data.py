from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

TELEGRAM_BOT_TOKEN = '8935661523:AAEVBhktS9ABBuKskaK4aRTxEIvMbQqB7Us'
TELEGRAM_CHAT_ID = '8935661523'

default_args = {
    'owner': 'mle-user',
    'depends_on_past': False,
    'start_date': datetime(2026, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        pass

with DAG(
    dag_id='collect_real_estate_data',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['project', 'stage1'],
) as dag:

    @task
    def create_table():
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        sql = """
            DROP TABLE IF EXISTS merged_flats;
            CREATE TABLE merged_flats (
                flat_id INTEGER,
                building_id INTEGER,
                floor INTEGER,
                kitchen_area FLOAT,
                living_area FLOAT,
                rooms INTEGER,
                is_apartment BOOLEAN,
                studio BOOLEAN,
                total_area FLOAT,
                price FLOAT,
                build_year INTEGER,
                building_type_int INTEGER,
                latitude FLOAT,
                longitude FLOAT,
                ceiling_height FLOAT,
                flats_count INTEGER,
                floors_total INTEGER,
                has_elevator BOOLEAN
            );
        """
        pg_hook.run(sql)
        return "Table created"

    @task
    def extract():
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        flats_count = pg_hook.get_first("SELECT COUNT(*) FROM flats;")[0]
        buildings_count = pg_hook.get_first("SELECT COUNT(*) FROM buildings;")[0]
        return {"flats": flats_count, "buildings": buildings_count}

    @task
    def transform(counts):
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        sql = """
            INSERT INTO merged_flats
            SELECT
                f.id AS flat_id,
                f.building_id,
                f.floor,
                f.kitchen_area,
                f.living_area,
                f.rooms,
                f.is_apartment,
                f.studio,
                f.total_area,
                f.price,
                b.build_year,
                b.building_type_int,
                b.latitude,
                b.longitude,
                b.ceiling_height,
                b.flats_count,
                b.floors_total,
                b.has_elevator
            FROM flats f
            LEFT JOIN buildings b ON f.building_id = b.id;
        """
        pg_hook.run(sql)
        return "Transform done"

    @task
    def load():
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        count = pg_hook.get_first("SELECT COUNT(*) FROM merged_flats;")[0]
        return f"Loaded {count} rows"

    @task
    def notify_success():
        send_telegram_message("DAG collect_real_estate_data completed successfully!")

    @task(trigger_rule='one_failed')
    def notify_failure():
        send_telegram_message("DAG collect_real_estate_data failed!")

    t1 = create_table()
    t2 = extract()
    t3 = transform(t2)
    t4 = load()
    t5 = notify_success()
    t6 = notify_failure()

    t1 >> t2 >> t3 >> t4 >> t5
    [t1, t2, t3, t4] >> t6