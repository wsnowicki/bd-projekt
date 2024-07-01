import psycopg2
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

def clear_db():
    pg_conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    conn = psycopg2.connect(**pg_conn_params)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS Pomiar;')
    cursor.execute('DROP TABLE IF EXISTS Stacja_Pomiarowa;')
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    clear_db()

