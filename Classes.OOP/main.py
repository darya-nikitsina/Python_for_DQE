import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_root)

from Functions.HT_Functions_DaryaNikitsina import normalize_letter_case
import datetime
# import time




# Initiate a parent class for all types of publications
class Publication:
    def __init__(self, text):
        self.text = text
        self.publication_date = self.get_publication_date()

    def check_date(self, date_string):                # method to check any date was inserted
        try:
            datetime.datetime.strptime(date_string, '%Y-%m-%d')
            if datetime.date.fromisoformat(date_string) >= datetime.date.today():
                return True
            else:
                print('Date cannot be earlier than today\'s date.')
                return False
        except ValueError:
            print('Date has been added in an inappropriate format.')
            return False

    def get_title(self, title_text=''):
        title = '-' * 20 + title_text
        return title

    def get_publication_date(self):             # method to get date of any type of publication
        publication_date = datetime.date.today()
        return publication_date

    def format_publication(self, title_text=''):               # method to define a standard format for main part of any publication
        return f'{self.text}\nPublished on: {self.publication_date.isoformat()}'

    def publish(self):                          # method for publishing to the .txt file
        try:
            with open('NewsFeed.txt', 'a', encoding='utf-8') as news_file:
                news_file.write(self.format_publication())
                news_file.write('\n')
        except BaseException as exception:
            print('Something happened. Please check the error:')
            print(exception)


# Initiate a child class for News
class News(Publication):
    def __init__(self, text='No news', city='Unspecified'):
        super().__init__(text)
        self.city = city

    def format_publication(self):               # method for customizing the format of a news publication
        parent_format = super().format_publication()
        title = self.get_title('News')
        return f'{title}\nCity: {self.city.upper()}\n{parent_format}\n'


# Initiate a class for Private Advertisement
class PrivatAd(Publication):
    def __init__(self, text='None', expiration_date=str):
        super().__init__(text)
        self.expiration_date = expiration_date
        self.calculate_days_left = self.calculate_days_left()

    def __string_to_date(self):                 # privat method to convert a string value (expiration_date) to a date
        string = self.expiration_date
        date = datetime.datetime.strptime(string, '%Y-%m-%d').date()
        return date

    def calculate_days_left(self):              # method to calculate days left
        published_on = self.get_publication_date()
        expires_on = self.__string_to_date()
        days_left = (expires_on - published_on).days
        return days_left

    def format_publication(self):               # method to format current type of publication
        parent_format = super().format_publication()
        title = self.get_title('Privat Ad')
        expiration = self.expiration_date
        days_left = self.calculate_days_left
        return f'{title}\n{parent_format}\nExpires on: {expiration}\nDays left: {days_left}\n'


# Initiate a class for Weather Forecast as new entity
class WeatherForecast(Publication):
    def __init__(self, text='Weather forecast', city='Unspecified', temperature=0, forecast_date='9999-99-99'):
        super().__init__(text)
        self.city = city
        self.temperature = temperature
        self.forecast_date = forecast_date

    def format_temperature(self):               # method to format temperature with degree Celsius
        return f'{self.temperature}°C'

    def get_weather_advice(self):               # method to provide advice based on temperature
        if self.temperature <= -30 or self.temperature >= 30:
            return 'Extreme temperature! Stay home, stay tuned, stay safe!'
        elif -30 < self.temperature <= -5:
            return 'It is freezing outside. Dress warmly!'
        elif -5 < self.temperature <= 1:
            return 'It is freezing outside. Potential ice. Be careful on the roads!'
        elif 1 < self.temperature <= 10:
            return 'It is chilly. Consider wearing a jacket.'
        elif 10 < self.temperature <= 20:
            return 'The weather is mild, a light jacket will do.'
        elif 20 < self.temperature <= 25:
            return 'It is warm outside. It is a great time for a walk without outerwear.'
        else:
            return 'It is hot outside! Stay hydrated!'

    def format_publication(self):                # method to format the current type of publication
        parent_format = super().format_publication()
        title = self.get_title('Weather Forecast')
        forecast_city = self.city.upper()
        forecast_date = self.forecast_date
        temperature = self.format_temperature()
        weather_advice = self.get_weather_advice()
        return (f'{title}\nCity: {forecast_city}\nForecast for: {forecast_date}\nTemperature: {temperature}\n'
                f'Advice: {weather_advice}\n{parent_format}\n')


# new class that allows to provide records by text file
class FileProcessor:
    def __init__(self, file_path='InputFile.txt'):
        self.file_path = file_path

    def read_file(self):
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} does not exist.")
            return None

        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        return content

    def process_file(self):
        content = self.read_file()
        if not content:
            return

        # list to store materials to be published in case no errors happened
        to_be_published = []
        # boolean variable to check errors or exceptions during next for loop
        error_occurred = False

        for line in content:

            try:
                # define input format for previously described publication types
                if "news" in line.lower():
                    _, text, city = line.split(';')
                    news = News(normalize_letter_case(text).strip(), city.strip())
                    to_be_published.append(news)

                elif "advertisement" in line.lower():
                    _, text, expiration_date = line.split(';')
                    s_text = text.strip()
                    s_expiration_date = expiration_date.strip()
                    ad = PrivatAd(normalize_letter_case(s_text), s_expiration_date)

                    if ad.check_date(s_expiration_date) is True:
                        to_be_published.append(ad)
                    else:
                        error_occurred = True
                        break

                elif "weather" in line.lower():
                    _, text, city, temperature, forecast_date = line.split(';')
                    s_text = text.strip()
                    s_city = city.strip()
                    s_temperature = int(temperature.strip())
                    s_forecast_date = forecast_date.strip()
                    weather = WeatherForecast(normalize_letter_case(s_text), s_city, s_temperature, s_forecast_date)

                    if weather.check_date(s_forecast_date) is True:
                        to_be_published.append(weather)
                    else:
                        error_occurred = True
                        break

                else:
                    print(f'Line format in not supported. The line was skipped:{line}')
                    error_occurred = True
                    break

            except ValueError as e:
                print(f'Line processing error. Line is in unexpected format: {line}')
                print(f'Error description: {e}')
                error_occurred = True
                break

            except Exception as e:
                print(f'An unexpected error occurred while processing the line: {line}')
                print(f'Error description: {e}')
                error_occurred = True
                break

        if error_occurred is True:
            print("The file cannot be published. Please make changes to meet the input requirements.")
        else:
            for publication in to_be_published:
                publication.publish()

            print("File has been successfully processed and published.")
            self.remove_file()


    def remove_file(self):
        try:
            os.remove(self.file_path)
            print(f"File {self.file_path} has been successfully removed.")
        except OSError as e:
            print(f"Error while deleting file {self.file_path}: {e}")


# # Function to run the program from console
# def publish_content():
#     while True:
#         print('\nChoose type of publication:')
#         print('1. News')
#         print('2. Private Advertisement')
#         print('3. Weather Forecast')
#         print('4. Cancel current publication')
#
#         choice = input('Enter the relevant number from 1 to 4: ')
#
#         try:
#             if choice == '1':
#                     text = input('Write the news text: ')
#                     city = input('Write the city name: ')
#                     news = News(text, city)
#                     news.publish()
#                     print('The news has been added to the file!')
#                     time.sleep(3)
#                     continue
#
#             elif choice == '2':
#                 text = input('Write the advertisement text: ')
#
#                 while True:
#                     expiration_date = input('Add the expiration date in format YYYY-MM-DD: ')
#                     if PrivatAd(text).check_date(expiration_date):
#                         break
#                     else:
#                         print('Something went wrong!')
#                         time.sleep(5)
#                         break
#
#                 advertisement = PrivatAd(text, expiration_date)
#                 advertisement.publish()
#                 print('The private advertisement has been added to the file!')
#                 time.sleep(3)
#                 continue
#
#             elif choice == '3':
#                 text = input('Write the text part of the weather forecast: ')
#                 city = input('Write a city name for the weather forecast: ')
#
#                 while True:
#                     try:
#                         temperature = int(input('Add the temperature as positive or negative integer: '))
#                         break
#                     except ValueError:
#                         print('Temperature should be an integer. Please try again.')
#
#                 while True:
#                     forecast_date = input('Write a date for the weather forecast in format YYYY-MM-DD: ')
#                     if PrivatAd(text).check_date(forecast_date):
#                         break
#                     else:
#                         print('Something went wrong!')
#                         time.sleep(5)
#                         break
#
#                 while True:
#                     expiration_date = input('Add the expiration date in format YYYY-MM-DD: ')
#                     if PrivatAd(text).check_date(expiration_date):
#                         break
#                     else:
#                         print('Something went wrong!')
#                         time.sleep(5)
#                         break
#
#                 weather_forecast = WeatherForecast(text, city, temperature, forecast_date)
#                 weather_forecast.publish()
#                 print('The weather forecast has been added to the file!')
#                 time.sleep(3)
#                 continue
#
#             elif choice == '4':
#                 print('Publication has been canceled.')
#                 time.sleep(3)
#                 break
#
#             else:
#                 print('Make sure you have selected the correct option in the previous step.')
#                 time.sleep(3)
#                 continue
#
#         except BaseException as exception:
#             print('Your publication has not been published. Be sure the entered data matches the requested data.')
#             print(exception)
#             time.sleep(5)
#             continue


if __name__ == '__main__':
    file_path = input('Enter the file path or leave empty for default (InputFile.txt): ')
    processor = FileProcessor(file_path if file_path else 'InputFile.txt')
    processor.process_file()
