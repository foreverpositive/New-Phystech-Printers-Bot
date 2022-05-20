import os
import json
import requests


def is_member(telegram_id):
    token = os.environ['API_TOKEN']
    # with open('printers/access-token', 'r', encoding='utf-8') as token_file:
    #     token = token_file.read()

    url = 'https://physics.itmo.ru/ru/rest/export/json/users-telegram-id-roles'
    params = {'_format': 'json', 'telegram_id_value': telegram_id}
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, params=params, headers=headers)
    resp = json.loads(response.text)

    if resp != [] and resp[0]['roles_target_id'] == 'member':
        return True

    return False
