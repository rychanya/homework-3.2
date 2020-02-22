import requests

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
API_TOKEN = ''  # insert your token here


def translate_it(text, translation_direction):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': API_KEY,
        'text': text,
        'lang': translation_direction
    }
    print(translation_direction, 'Пытаемся перевести текст ', end='')
    response = requests.post(URL, params=params)
    if response.status_code == 200:
        print('OK')
        return response.json().get('text')
    else:
        print('FAIL')


def detect_lang(text):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    params = {
        'key': API_KEY,
        'text': text
    }
    print('Пытаемся определить язык текста ', end='')
    response = requests.post(URL, params=params)
    if response.status_code == 200:
        print('OK')
        return response.json().get('lang')
    else:
        print('FAIL')


def translate_file(in_file_path, out_file_path, from_lang=None, to_lang='ru'):
    with open(in_file_path, encoding='utf-8') as in_file:
        text = in_file.readlines()
        print(f'Файл {in_file_path} прочитан')
    if from_lang is None:
        from_lang = detect_lang(text)
    with open(out_file_path, 'w', encoding='utf-8') as out_file:
        translated_text = translate_it(text, f'{from_lang}-{to_lang}')
        out_file.writelines(translated_text)
        print(f'Файл с переводом сохранен как {out_file_path}')


class Loader:

    def __init__(self, file_name):
        self._file_name = file_name
        self._upload_link = ''

    def _get_upload_link(self):
        URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'disk:/{self._file_name}',
            'overwrite': True
        }
        headers = {
            'Authorization': API_TOKEN
        }
        response = requests.get(URL, params=params, headers=headers)
        if response.status_code == 200:
            self._upload_link = response.json()['href']
            print('Ссылка для загрузки получена.')
        else:
            print('Не удалось получить ссулку.')

    def upload(self):
        self._get_upload_link()
        if not self._upload_link:
            return
        with open(self._file_name, 'rb') as upload_file:
            response = requests.put(self._upload_link, data=upload_file)
            if response.status_code == 201 or response.status_code == 202:
                print(f'файл {self._file_name} загружен.')
            else:
                print(f'файл {self._file_name} не загружен.')


if __name__ == '__main__':
    files = [
        'DE.txt',
        'ES.txt',
        'FR.txt',
    ]
    for file in files:
        new_path = f'translated-{file}'
        translate_file(file, new_path)
        loader = Loader(new_path)
        loader.upload()
