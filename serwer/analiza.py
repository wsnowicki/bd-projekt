import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

def get_pg_conn_params():
    """
    Pobiera parametry połączenia z pliku .env.

    :return: Słownik z parametrami połączenia do bazy danych PostgreSQL.
    """
    return {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

def get_all_measurements() -> pd.DataFrame:
    """
    Pobiera wszystkie pomiary z bazy danych PostgreSQL.

    :return: DataFrame zawierający wszystkie pomiary.
    """
    pg_conn_params = get_pg_conn_params()
    conn = psycopg2.connect(**pg_conn_params)
    query = 'SELECT * FROM Pomiar'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_station_measurements(station_id: int) -> pd.DataFrame:
    """
    Pobiera wszystkie pomiary dla konkretnej stacji pomiarowej.

    :param station_id: ID stacji pomiarowej.
    :return: DataFrame zawierający pomiary dla danej stacji.
    """
    pg_conn_params = get_pg_conn_params()
    conn = psycopg2.connect(**pg_conn_params)
    query = 'SELECT * FROM Pomiar WHERE stacja_id = %s'
    df = pd.read_sql(query, conn, params=(station_id,))
    conn.close()
    return df

def get_summary_statistics() -> pd.DataFrame:
    """
    Pobiera statystyki podsumowujące dla każdej stacji pomiarowej.

    :return: DataFrame zawierający statystyki podsumowujące.
    """
    pg_conn_params = get_pg_conn_params()
    conn = psycopg2.connect(**pg_conn_params)
    query = '''
    SELECT
        stacja_id,
        AVG(pm10) AS avg_pm10,
        AVG(pm2_5) AS avg_pm2_5,
        AVG(ozon) AS avg_ozon,
        AVG(temperatura) AS avg_temperatura
    FROM Pomiar
    GROUP BY stacja_id
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df

