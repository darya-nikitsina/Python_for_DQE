# install geopy through terminal: pip install geopy
from geopy.distance import geodesic
from Cities_DB_Processor import CitiesDBProcessor

db_processor = CitiesDBProcessor()

def calculate_distance(city_name_1, city_name_2):
    city_coordinates_1 = db_processor.get_city_coordinates_db(city_name_1)
    city_coordinates_2 = db_processor.get_city_coordinates_db(city_name_2)

    city_coordinates_1 = list(map(float, city_coordinates_1))
    city_coordinates_2 = list(map(float, city_coordinates_2))

    distance = geodesic(city_coordinates_1, city_coordinates_2).kilometers
    return distance

def main():
    try:
        print("Hi! Here you can find a straight-line distance between 2 cities!")
        city1 = input("Please input the first city name: ").strip()
        city2 = input("Please input the second city name: ").strip()

        distance = calculate_distance(city1, city2)
        print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} kilometers.")

    except BaseException as e:
        print(f"Oops! Something went wrong. Please see exception {e}")

if __name__ == "__main__":
    main()
