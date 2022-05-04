import json
import requests


with open('printers/access-token', 'r', encoding='utf-8') as token_file:
    TOKEN = token_file.read()


def is_member(telegram_id):
    url = 'https://physics.itmo.ru/ru/rest/export/json/users-telegram-id-roles'
    params = {'_format': 'json', 'telegram_id_value': telegram_id}
    headers = {'Authorization': f'Bearer {TOKEN}'}

    response = requests.get(url, params=params, headers=headers)
    resp = json.loads(response.text)

    if resp != [] and resp[0]['roles_target_id'] == 'member':
        return True

    return False
