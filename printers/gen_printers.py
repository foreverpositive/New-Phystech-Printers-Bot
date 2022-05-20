import json
import csv

csv_file = 'printers/printers.csv'
json_file = 'printers/printers.json'


def json_from_csv():
    printers = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            number, model, location, ip = row
            shortname = 'print' + str(number)
            domain = shortname + '.metalab.ifmo.ru'
            printers[shortname] = {'Domain': domain, 'Model': model,
                                   'Location': location, 'IP': ip}

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(printers, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    json_from_csv()
