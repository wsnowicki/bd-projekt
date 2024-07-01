# bd-projekt
Projekt na bazy danych, który zawiera proste wykorzystanie postgresa i sqlite3. Napisany w Pythonie 3.12.

Składa się z 3 części:
- Client (sqlite3),
- Server (postgresql),
- Część analityczna.

# Autorzy
- 272780
- 214963

# Instalacja
1. Sklonuj repo za pomocą polecenia `git clone`,
2. Zainstaluj wszystkie wymagane biblioteki Pythonowe z pliku requirements.txt,
3. Utwórz bazę danych, użytkownika i nadaj mu uprawnienia
```
CREATE DATABASE baza;
CREATE USER example WITH ENCRYPTED PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE baza TO example;
\c baza postgres
# You are now connected to database "baza" as user "postgres".
GRANT ALL ON SCHEMA public TO example;
```
4. Dodaj plik .env z danymi do bazy danych do folderu serwer [przykład do pliku](./.env_example.txt)
5. Uruchom program, importuj cokolwiek xD
