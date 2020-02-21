import requests

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'


def translate_it(text, translation_direction):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': API_KEY,
        'text': text,
        'lang': translation_direction
    }
    response = requests.post(URL, params=params)
    try:
        response.raise_for_status()
        texts = response.json().get('text')
        return ''.join(texts)
    except requests.exceptions.HTTPError as error:
        print(error)


def get_langs(lang):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
    params = {
        'key': API_KEY,
        'ui': lang
    }
    response = requests.post(URL, params=params)
    try:
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


def translate_file(in_file_path, out_file_path, from_lang='en', to_lang='ru'):
    translation_direction = make_translation_direction(from_lang=from_lang, to_lang=to_lang)
    with open(in_file_path) as in_file:
        with open(out_file_path, 'w') as out_file:
            for line in in_file:
                out_file.write(translate_it(line, translation_direction))


if __name__ == '__main__':
    files = [
        {
            'file': 'DE.txt',
            'language': 'de'
        },
        {
            'file': 'ES.txt',
            'language': 'es'
        },
        {
            'file': 'FR.txt',
            'language': 'fr'
        },
    ]
    for file in files:
        translate_file(
            file['file'], 
            'translated-' + file['file'], 
            file['language'])
