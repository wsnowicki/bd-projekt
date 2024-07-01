import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

def insert_test_data():
    pg_conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    conn = psycopg2.connect(**pg_conn_params)
    cursor = conn.cursor()
    
    stacje = [
        ('Stacja 1', 'Lokalizacja 1'),
        ('Stacja 2', 'Lokalizacja 2'),
        ('Stacja 3', 'Lokalizacja 3')
    ]
    
    for nazwa, lokalizacja in stacje:
        cursor.execute('INSERT INTO Stacja_Pomiarowa (nazwa, lokalizacja) VALUES (%s, %s)', (nazwa, lokalizacja))
    
    pomiary = [
        (datetime.now(), 'Centrum Miasta', 20.5, 15.2, 30.4, 22.5, 1),
        (datetime.now(), 'Przedmieścia', 40.7, 25.3, 50.5, 18.3, 2),
        (datetime.now(), 'Obszar Wiejski', 10.4, 7.2, 20.1, 16.8, 3)
    ]
    
    for data, lokalizacja, pm10, pm2_5, ozon, temperatura, stacja_id in pomiary:
        cursor.execute('''
        INSERT INTO Pomiar (data, lokalizacja, pm10, pm2_5, ozon, temperatura, stacja_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data, lokalizacja, pm10, pm2_5, ozon, temperatura, stacja_id))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    insert_test_data()

