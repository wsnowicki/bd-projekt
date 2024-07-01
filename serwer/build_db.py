import psycopg2
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

def build_db():
    pg_conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    conn = psycopg2.connect(**pg_conn_params)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stacja_Pomiarowa (
        id SERIAL PRIMARY KEY,
        nazwa VARCHAR(100),
        lokalizacja VARCHAR(255)
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pomiar (
        id SERIAL PRIMARY KEY,
        data TIMESTAMP,
        lokalizacja VARCHAR(255),
        pm10 REAL,
        pm2_5 REAL,
        ozon REAL,
        temperatura REAL,
        stacja_id INTEGER REFERENCES Stacja_Pomiarowa(id)
    );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    build_db()

