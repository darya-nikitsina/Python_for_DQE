import datetime
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_root)

from Functions.HT_Functions_DaryaNikitsina import normalize_letter_case


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


    def process_invalid_row(self, invalid_row=''):
        try:
            with open('InvalidRows.txt', 'a', encoding='utf-8') as file:
                file.write(invalid_row)
                file.write(f'Recording date: {datetime.date.today()}\n\n')
        except BaseException as exception:
            print('Something happened. Please check the error:')
            print(exception)


    def process_file(self):
        from Classes_OOP.main import News, PrivatAd, WeatherForecast
        content = self.read_file()
        if not content:
            return

        # list to store materials to be published in case no errors happened
        to_be_published = []
        invalid_rows = []
        # boolean variable to check errors or exceptions during next for loop
        error_occurred = False

        for line in content:

            try:
                # define input format for previously described publication types
                if "news" in line.lower():
                    _, text, city = line.split('|')
                    news = News(normalize_letter_case(text).strip(), city.strip())
                    to_be_published.append(news)

                elif "advertisement" in line.lower():
                    _, text, expiration_date = line.split('|')
                    s_text = text.strip()
                    s_expiration_date = expiration_date.strip()
                    ad = PrivatAd(normalize_letter_case(s_text), s_expiration_date)

                    if ad.check_date(s_expiration_date) is True:
                        to_be_published.append(ad)
                    else:
                        error_occurred = True
                        invalid_rows.append(line)
                        continue

                elif "weather" in line.lower():
                    _, text, city, temperature, forecast_date = line.split('|')
                    s_text = text.strip()
                    s_city = city.strip()
                    s_temperature = int(temperature.strip())
                    s_forecast_date = forecast_date.strip()
                    weather = WeatherForecast(normalize_letter_case(s_text), s_city, s_temperature, s_forecast_date)

                    if weather.check_date(s_forecast_date) is True:
                        to_be_published.append(weather)
                    else:
                        error_occurred = True
                        invalid_rows.append(line)
                        continue

                else:
                    print(f'Line format is not supported.')
                    invalid_rows.append(line)
                    error_occurred = True
                    continue

            except ValueError as e:
                print(f'Line processing error. Line is in unexpected format.')
                print(f'Error description: {e}')
                invalid_rows.append(line)
                error_occurred = True
                continue

            except Exception as e:
                print(f'An unexpected error occurred while processing the line: {line}')
                print(f'Error description: {e}')
                invalid_rows.append(line)
                error_occurred = True
                continue

        if error_occurred is True:
            for invalid_row in invalid_rows:
                self.process_invalid_row(invalid_row)
            print("The file cannot be published. Please make changes to meet the input requirements.")
            print("Invalid rows are presented in the InvalidRows.txt file.")
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
