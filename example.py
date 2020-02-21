import requests

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
API_TOKEN = '' #insert your token here

def translate_it(text, translation_direction):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': API_KEY,
        'text': text,
        'lang': translation_direction
    }
    try:
        response = requests.post(URL, params=params)
        response.raise_for_status()
        return response.json().get('text')
    except requests.exceptions.HTTPError as error:
        print(error)


def detect_lang(text):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    params = {
        'key': API_KEY,
        'text': text
    }
    try:
        response = requests.post(URL, params=params)
        response.raise_for_status()
        return response.json().get('lang')
    except requests.exceptions.HTTPError as error:
        print(error)

def get_langs(lang):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
    params = {
        'key': API_KEY,
        'ui': lang
    }
    try:
        response = requests.post(URL, params=params)
        response.raise_for_status()
        return set(response.json()['langs'].keys())
    except requests.exceptions.HTTPError as error:
        print(error)


def make_translation_direction(from_lang='en', to_lang='ru'):
    langs = get_langs(from_lang)
    if from_lang in langs and to_lang in langs:
        return f'{from_lang}-{to_lang}'
    else:
        print('Invalide language. Try translate from en to ru.')
        return('en-ru')


def translate_file(in_file_path, out_file_path, from_lang=None, to_lang='ru'):
    with open(in_file_path, encoding='utf-8') as in_file:
        text = in_file.readlines()
    if from_lang is None:
        from_lang = detect_lang(text)
    translation_direction = make_translation_direction(from_lang=from_lang, to_lang=to_lang)
    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        out_file.writelines(translate_it(text, translation_direction))

def create_dir(dir_name):
    URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {
        'path': f'disk:/{dir_name}',
    }
    headers = {
        'Authorization': API_TOKEN
    }
    response = requests.put(URL, params=params, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 409:
            print('Dir aleredy exists')
            return
        print(error)

def get_upload_link(file_name):
    URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params = {
        'path': f'disk:/foo/{file_name}',
        'overwrite': True
    }
    headers = {
        'Authorization': API_TOKEN
    }
    response = requests.get(URL, params=params, headers=headers)
    try:
        response.raise_for_status()
        return response.json()['href']
    except requests.exceptions.HTTPError as error:
        print(error)

def upload_to_disk(url, data):
    response = requests.put(url, data=data)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)

if __name__ == '__main__':
    files = [
        'DE.txt',
        'ES.txt',
        'FR.txt',
    ]
    create_dir('foo')
   
    for file in files:
        new_path = f'translated-{file}'
        translate_file(file, new_path)
        url = get_upload_link(new_path)
        with open(new_path, 'rb') as uplod_file:
            upload_to_disk(url, uplod_file)

