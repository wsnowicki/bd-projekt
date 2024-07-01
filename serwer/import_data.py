import psycopg2
import csv
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

def import_data(csv_path):
    """
    Importuje dane z plików CSV do bazy danych PostgreSQL.

    :param csv_path: Ścieżka do katalogu z plikami CSV.
    """
    pg_conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    # Import CSV data to PostgreSQL
    pg_conn = psycopg2.connect(**pg_conn_params)
    cursor = pg_conn.cursor()
    
    with open(csv_path + 'stacja_pomiarowa.csv', 'r') as file:
        next(file)
        cursor.copy_expert("COPY Stacja_Pomiarowa FROM STDIN WITH CSV HEADER", file)
    
    with open(csv_path + 'pomiar.csv', 'r') as file:
        next(file)
        cursor.copy_expert("COPY Pomiar FROM STDIN WITH CSV HEADER", file)
    
    pg_conn.commit()
    cursor.close()
    pg_conn.close()

if __name__ == '__main__':
    csv_path = 'path/to/csv/'
    import_data(csv_path)

