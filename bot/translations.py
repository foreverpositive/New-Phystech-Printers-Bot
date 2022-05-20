import json
import csv

csv_file = 'bot/phrases.csv'
json_file = 'bot/translations.json'


def json_from_csv():
    phrases = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            phrases[row[0]] = {'en': row[1], 'ru': row[2]}

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(phrases, file, indent=4, ensure_ascii=False)


def load_tr():
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == '__main__':
    json_from_csv()
