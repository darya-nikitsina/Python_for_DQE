import json
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_root)

from Functions.HT_Functions_DaryaNikitsina import normalize_letter_case


class FileProcessorJSON:
    def __init__(self, file_path='InputFile.json'):
        self.file_path = file_path
        self.invalid_records_file = 'InvalidRecords.json'

    def read_json(self):
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} does not exist.")
            return None

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else [data]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file: {e}")
            return None

    def process_invalid_records(self, record):
        invalid_records = []

        try:
            with open(self.invalid_records_file, 'r', encoding='utf-8') as file:
                invalid_records = json.load(file)
                if not isinstance(invalid_records, list):
                    invalid_records = []
        except (json.JSONDecodeError, BaseException) as exception:
            print('Something happened. Please check the error:')
            print(exception)

        invalid_records.append(record)
        with open(self.invalid_records_file, 'w', encoding='utf-8') as file:
            json.dump(invalid_records, file, ensure_ascii=False, indent=4)

    def process_json_file(self):
        from main import News, PrivatAd, WeatherForecast

        content = self.read_json()
        if not content:
            return

        to_be_published = []
        invalid_records = []
        error_occurred = False

        for record in content:
            try:
                record_type = record.get("type").lower()
                if record_type == "news":
                    text = normalize_letter_case(record.get("text", ""))
                    city = record.get("city", "")
                    publication = News(text, city)
                    to_be_published.append(publication)

                elif record_type == "ad":
                    text = normalize_letter_case(record.get("text", ""))
                    expiration_date = record.get("expiration_date", "")
                    ad = PrivatAd(text, expiration_date)
                    if ad.check_date(expiration_date):
                        to_be_published.append(ad)
                    else:
                        error_occurred = True
                        invalid_records.append(record)

                elif record_type == "weather":
                    text = normalize_letter_case(record.get("text", ""))
                    city = record.get("city", "")
                    temperature = int(record.get("temperature", 0))
                    forecast_date = record.get("forecast_date", "")
                    weather = WeatherForecast(text, city, temperature, forecast_date)
                    if weather.check_date(forecast_date):
                        to_be_published.append(weather)
                    else:
                        error_occurred = True
                        invalid_records.append(record)

                else:
                    print("Unsupported entry type found.")
                    invalid_records.append(record)
                    error_occurred = True

            except (ValueError, TypeError, KeyError) as e:
                print(f"Error processing entry: {e}")
                invalid_records.append(record)
                error_occurred = True

        if error_occurred:
            for invalid_record in invalid_records:
                self.process_invalid_records(invalid_record)
            print("File contains invalid records. Check InvalidRecords.json for details.")
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
