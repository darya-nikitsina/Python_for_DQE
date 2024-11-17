import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_root)

from Functions.HT_Functions_DaryaNikitsina import normalize_letter_case

class FileProcessorXML:
    def __init__(self, file_path='InputFile.xml'):
        self.file_path = file_path
        self.invalid_records_file = 'InvalidRecords.xml'

    def read_xml(self):
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} does not exist.")
            return None

        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            return root

        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return None

    def format_xml_string(self, elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)

        # Get the formatted string with minimal spacing
        formatted_string = reparsed.toprettyxml(indent='  ')

        # Remove empty lines and extra whitespace
        clean_lines = []
        for line in formatted_string.splitlines():
            if line.strip():  # Only keep non-empty lines
                clean_lines.append(line)

        return '\n'.join(clean_lines)

    def process_invalid_records(self, invalid_root):
        formated_xml = self.format_xml_string(invalid_root)

        try:
            with open(self.invalid_records_file, 'w', encoding='utf-8') as f:
                f.write(formated_xml)
        except IOError as e:
            print(e)

    def process_xml_file(self):
        from main import News, PrivatAd, WeatherForecast

        root = self.read_xml()
        if root is None:
            return

        to_be_published = []
        invalid_root = ET.Element("InvalidRecords")
        error_occurred = False

        for record in root.findall(".//publication"):
            record_data = {child.tag: child.text for child in record}

            try:
                publication_type = record_data.get("type", "").lower()

                if publication_type == "news":
                    text = normalize_letter_case(record_data.get("text", ""))
                    city = record_data.get("city", "")
                    news = News(text.strip(), city.strip())
                    to_be_published.append(news)

                elif publication_type == "ad":
                    text = normalize_letter_case(record_data.get("text", ""))
                    expiration_date = record_data.get("expiration_date", "")
                    ad = PrivatAd(text.strip(), expiration_date.strip())

                    if ad.check_date(expiration_date):
                        to_be_published.append(ad)
                    else:
                        error_occurred = True
                        invalid_root.append(record)

                elif publication_type == "weather":
                    text = normalize_letter_case(record_data.get("text", ""))
                    city = record_data.get("city", "")
                    temperature = record_data.get("temperature", "0")
                    forecast_date = record_data.get("forecast_date", "")
                    weather = WeatherForecast(text.strip(), city.strip(), int(temperature), forecast_date.strip())

                    if weather.check_date(forecast_date):
                        to_be_published.append(weather)
                    else:
                        error_occurred = True
                        invalid_root.append(record)

                else:
                    print(f"Unsupported publication type: {publication_type}")
                    error_occurred = True
                    invalid_root.append(record)

            except (ValueError, KeyError, TypeError) as e:
                print(f"Error processing record: {record_data}")
                print(f"Error description: {e}")
                invalid_root.append(record)
                continue

        if error_occurred:
            self.process_invalid_records(invalid_root)
            print("File contains invalid records. Check InvalidRecords.xml for details.")
        else:
            for publication in to_be_published:
                publication.publish()
            print("File has been successfully processed.")
            self.remove_file()

    def remove_file(self):
        try:
            os.remove(self.file_path)
            print(f"File {self.file_path} has been successfully removed.")
        except OSError as e:
            print(f"Error while deleting file {self.file_path}: {e}")
