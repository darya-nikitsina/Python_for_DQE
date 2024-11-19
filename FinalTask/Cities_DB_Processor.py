import sqlite3

class CitiesDBProcessor:
    def __init__(self):
        self.db_name = "cities.db"
        self.__create_db()

    def execute_query(self, query, params=(), fetchone=False, fetchall=False):
        """
            Args:
                query (str): SQL query to run
                params (tuple): Parameters for SQL query
                fetchone (bool): to return first result (one result)
                fetchall (bool): to return all results

            Returns:
                tuple or list
        """
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                elif fetchall:
                    return cursor.fetchall()
                connection.commit()

        except BaseException as e:
            print('Something went wrong. Please see exception: ')
            print(e)

    def __create_db(self):
        try:
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS cities(
                    name TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
            ''')

        except BaseException as e:
            print('Something went wrong. Please see exception: ')
            print(e)

    def insert_to_db(self, city_name, city_longitude, city_latitude):
        try:
            self.__create_db()

            self.execute_query(
                # OR IGNORE - if the value already exists in the table
                "INSERT OR IGNORE INTO cities (name, latitude, longitude) VALUES (?, ?, ?)",
                (city_name, city_longitude, city_latitude)
            )
        except BaseException as e:
            print('Something went wrong. Please see exception: ')
            print(e)

    def get_city_coordinates_user(self, city_name):
        try:
            city_coordinates = []
            latitude = float(input(f"Please write the {city_name} latitude: "))
            longitude = float(input(f"Please write the {city_name} longitude: "))
            self.insert_to_db(city_name, latitude, longitude)
            city_coordinates.append(latitude)
            city_coordinates.append(longitude)
            return city_coordinates
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    def get_city_coordinates_db(self, city_name):
        try:
            city_coordinates = self.execute_query('''
                    SELECT latitude, longitude
                    FROM cities
                    WHERE UPPER(name) = UPPER(?)
                ''', (city_name,), True, False)

            if city_coordinates:
                return city_coordinates
            else:
                print(f"No records found for {city_name}.")
                return self.get_city_coordinates_user(city_name)

        except BaseException as e:
            print('Something went wrong. Please see exception: ')
            print(e)
