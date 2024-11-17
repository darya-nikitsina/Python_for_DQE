import sqlite3

class DatabaseProcessor:
    def __init__(self, db_name='NewsFeedDatabase.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS News (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                city TEXT,
                publication_date DATE,
                UNIQUE(text, city, publication_date)
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PrivatAd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                expiration_date DATE,
                days_left INTEGER,
                publication_date DATE,
                UNIQUE(text, expiration_date, publication_date)
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS WeatherForecast (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                city TEXT,
                temperature INTEGER,
                forecast_date DATE,
                publication_date DATE,
                UNIQUE(text, city, forecast_date)
            );
        ''')
        self.connection.commit()

    def check_duplicate(self, table_name, **kwargs):
        conditions = ' AND '.join([f"{key} = ?" for key in kwargs])
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {conditions};"

        self.cursor.execute(query, tuple(kwargs.values()))
        result = self.cursor.fetchone()
        return result[0] > 0

    def add_record(self, table_name, **kwargs):
        if self.check_duplicate(table_name, **kwargs):
            print(f"Duplicate found in table '{table_name}'. Record is not added to the database.")
            return False

        else:
            columns = ', '.join(kwargs.keys())
            placeholders = ', '.join(['?'] * len(kwargs))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
            try:
                self.cursor.execute(query, tuple(kwargs.values()))
                self.connection.commit()
                print(f"Record has been successfully added to the {table_name} in the {self.db_name}.")
                return True
            except sqlite3.IntegrityError as e:
                print(f"Error adding record: {e}")
                return False

    def close_connection(self):
        self.connection.close()
