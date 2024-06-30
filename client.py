import sqlite3
import random
from datetime import datetime, timedelta
import csv

class Client:
    def __init__(self, db_path: str):
        """
        Inicjalizuje klienta z podaną ścieżką do bazy danych.

        :param db_path: Ścieżka do pliku bazy danych SQLite.
        """
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        """
        Otwiera połączenie z bazą danych przy użyciu kontekstu.
        """
        self.conn = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Zamyka połączenie z bazą danych po zakończeniu kontekstu.
        """
        if self.conn:
            self.conn.close()

    def init_db(self) -> None:
        """
        Inicjalizuje bazę danych, tworząc tabele 'Stacja_Pomiarowa' i 'Pomiar', jeśli jeszcze nie istnieją.
        """
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Stacja_Pomiarowa (
                            id INTEGER PRIMARY KEY,
                            nazwa TEXT,
                            lokalizacja TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Pomiar (
                            id INTEGER PRIMARY KEY,
                            data TEXT,
                            lokalizacja TEXT,
                            pm10 REAL,
                            pm2.5 REAL,
                            ozon REAL,
                            temperatura REAL,
                            stacja_id INTEGER,
                            FOREIGN KEY (stacja_id) REFERENCES Stacja_Pomiarowa(id))''')
        self.conn.commit()

    def add_measurement(self, data: str, lokalizacja: str, pm10: float, pm25: float, ozon: float, temperatura: float, stacja_id: int) -> None:
        """
        Dodaje nowy pomiar do bazy danych.

        :param data: Data i czas pomiaru w formacie ISO.
        :param lokalizacja: Lokalizacja pomiaru.
        :param pm10: Poziom PM10.
        :param pm25: Poziom PM2.5.
        :param ozon: Poziom ozonu.
        :param temperatura: Temperatura.
        :param stacja_id: ID stacji pomiarowej.
        """
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO Pomiar (data, lokalizacja, pm10, pm2.5, ozon, temperatura, stacja_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (data, lokalizacja, pm10, pm25, ozon, temperatura, stacja_id))
        self.conn.commit()

    def export_to_csv(self, csv_file: str) -> None:
        """
        Eksportuje wszystkie pomiary z bazy danych do pliku CSV.

        :param csv_file: Nazwa pliku CSV do którego zostaną zapisane dane.
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Pomiar')
        rows = cursor.fetchall()
        
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'data', 'lokalizacja', 'pm10', 'pm2.5', 'ozon', 'temperatura', 'stacja_id'])
            writer.writerows(rows)

    def generate_random_data(self, ilosc: int) -> None:
        """
        Generuje losowe dane pomiarowe i wstawia je do bazy danych.

        :param ilosc: Liczba wierszy do wygenerowania i wstawienia do bazy danych.
        """
        cursor = self.conn.cursor()

        stacje = [
            (1, 'Stacja 1', 'Lokalizacja 1'),
            (2, 'Stacja 2', 'Lokalizacja 2'),
            (3, 'Stacja 3', 'Lokalizacja 3')
        ]

        cursor.executemany('INSERT OR IGNORE INTO Stacja_Pomiarowa (id, nazwa, lokalizacja) VALUES (?, ?, ?)', stacje)

        for _ in range(ilosc):
            data = datetime.now() - timedelta(days=random.randint(0, 30))
            data_str = data.isoformat()
            lokalizacja = random.choice(['Centrum Miasta', 'Przedmieścia', 'Obszar Wiejski'])
            pm10 = round(random.uniform(5.0, 100.0), 2)
            pm25 = round(random.uniform(5.0, 100.0), 2)
            ozon = round(random.uniform(10.0, 200.0), 2)
            temperatura = round(random.uniform(-10.0, 35.0), 2)
            stacja_id = random.choice([1, 2, 3])

            self.add_measurement(data_str, lokalizacja, pm10, pm25, ozon, temperatura, stacja_id)

        self.conn.commit()

# Przykład użycia klasy Client:
if __name__ == '__main__':
    with Client(DATABASE) as db:
        db.init_db()
        db.generate_random_data(100)  # Generuje i wstawia 100 losowych wierszy do bazy danych
        db.export_to_csv('measurements.csv')
