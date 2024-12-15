import random
import sqlite3
import requests
import urllib.parse
import json
import logging

# DICT_PATH = 'app/resources/dictionary.sqlite'
DICT_PATH = 'D:/member_info/Projects/Dictionary/app/resources/dictionary.sqlite'

# logging.basicConfig(
#     filename='db_provider_log.txt',
#     filemode='w',
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )


def download_main_db():
    headers = {
        'Authorization': 'OAuth y0_AgAAAABenFR4AAzOcwAAAAEZE0UeAAA9Dyor58ZKqbX_XxgwVjLIhlW3vw',
    }

    path = urllib.parse.quote('Dictionary_app/dictionary.sqlite')
    url = f'https://cloud-api.yandex.net/v1/disk/resources/download?path={path}'

    response = requests.get(url=url, headers=headers)

    download_url = response.content.decode('utf-8')
    download_url = json.loads(download_url)['href']
    response_file = requests.get(url=download_url).content

    with open(DICT_PATH, 'wb') as file:
        file.write(response_file)


def upload_main_db():
    headers = {
        'Authorization': 'OAuth y0_AgAAAABenFR4AAzOcwAAAAEZE0UeAAA9Dyor58ZKqbX_XxgwVjLIhlW3vw',
    }

    path = urllib.parse.quote('Dictionary_app/dictionary.sqlite')
    url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={path}&overwrite=true'

    response = requests.get(url=url, headers=headers)

    download_url = response.content.decode('utf-8')
    download_url = json.loads(download_url)['href']

    with open(DICT_PATH, 'rb') as file:
        files = {"file": file}
        print(requests.put(url=download_url, files=files).status_code)


def get_words(mod, kwargs):
    db = sqlite3.connect(DICT_PATH)
    cur = db.cursor()
    size: int = kwargs['size']
    r_data: list[dict] = []  # return data
    buffer: list[tuple]

    len_words_l: int = cur.execute('SELECT COUNT (*) FROM words').fetchone()[0]

    if mod == 'random':
        range_w = random.randint(0, len_words_l - size - 1)
        buffer = cur.execute("SELECT * FROM words LIMIT ? OFFSET ?", (size, range_w)).fetchall()

    elif mod == 'pagination':
        page = -kwargs['page']
        # Почему -1, а не +1? Дело в индексации, последнюю страницу легче взять, прописывая -1,
        # а не искать индекс последнего элемента в l_pages
        l_pages = [[i, i + (size - 1)] for i in range(1, len_words_l + 1, size) if
                   i + (size - 1) <= len_words_l]
        l_pages.insert(0, [0, 0])
        if len_words_l % size != 0:
            l_pages.append([len_words_l - len_words_l % size + 1, len_words_l])
        buffer = cur.execute("SELECT * FROM words LIMIT ? OFFSET ?", (size, l_pages[page][0])).fetchall()

    db.close()

    for item in buffer:
        r_data.append(
            {
                'id': item[0],
                'word': item[1],
                'transcription': item[2],
                'translate': item[3],
                'addition': item[4],
            }
        )

    return r_data


def validate_and_connect(func):  # decorator
    def wrapper(data: dict):
        db = sqlite3.connect(DICT_PATH)
        cur = db.cursor()

        if data['word'] != '' or data['translate'] != '':
            if data['word'] is not None and data['translate'] is not None:
                try:
                    func(data, cur)
                except sqlite3.IntegrityError:
                    logging.info(
                        f'Проблема со словом {' | '.join(list(data.values()))}, возможно оно не уникально')
            else:
                logging.info('Error')
        else:
            logging.info('Error')
        db.commit()
        db.close()
    return wrapper


@validate_and_connect
def inp_word(data, cur=None):
    cur.execute('INSERT INTO words VALUES (NULL, ?, ?, ?, ?)',
                (data['word'], data['transcription'], data['translate'], data['addition']))


@validate_and_connect
def edit_word(data, cur=None):
    cur.execute('UPDATE words SET word=?, transcription=?, translate=?, addition=? WHERE id=?',
                (data['word'], data['transcription'], data['translate'], data['addition'], data['word_id']))


@validate_and_connect
def del_word(data, cur=None):
    cur.execute('DELETE FROM words WHERE id=?', (data['word_id'],))


def get_search(**kwargs):
    db = sqlite3.connect(DICT_PATH)
    cur = db.cursor()
    r_data = []
    buffer = []
    if kwargs['word'] != '' and kwargs['translate'] != '':
        buffer = cur.execute('SELECT id, word, transcription, translate, addition FROM words WHERE word LIKE ? '
                             'AND translate LIKE ?', (f'%{kwargs['word']}%', f'%{kwargs['translate']}%'))
    elif kwargs['word'] != '':
        buffer = cur.execute('SELECT id, word, transcription, translate, addition FROM words WHERE word LIKE ?',
                             (f'%{kwargs['word']}%',))
    elif kwargs['translate'] != '':
        buffer = cur.execute('SELECT id, word, transcription, translate, addition FROM words'
                             ' WHERE translate LIKE ?', (f'%{kwargs['translate']}%',))
    buffer = buffer.fetchall()
    db.close()

    for item in buffer:
        r_data.append(
            {
                'id': item[0],
                'word': item[1],
                'transcription': item[2],
                'translate': item[3],
                'addition': item[4],
            }
        )

    return r_data


if __name__ == '__main__':
    pass
