import sqlite3
from urllib.request import urlopen
import json
from tqdm import tqdm
from urllib.error import HTTPError

con = sqlite3.connect('subtitles.db', check_same_thread=False)
cur = con.cursor()
cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
tables = cur.fetchall()

if not tables or ('subtitles' not in tables[0]):
        cur.execute('''CREATE TABLE subtitles
                       (video_Id integer, duration integer, content text, startOfParagraph integer, startTime integer)''')


def ted_parser(video_id):
    """
    Функция парсит данные(id видео ролика,субтитры ролика,продолжительность и значение существования параграфа) из сайта TED
    """
    try:
        ted_url = urlopen(f'https://www.ted.com/talks/subtitles/id/{video_id}/lang/en')
    except HTTPError as e: return None

    ted_content_json = ted_url.read().decode('utf8')
    ted_content_list = json.loads(ted_content_json)
    data_rows = []
    for data_objects in ted_content_list['captions']:
        data_rows.append([video_id, data_objects['duration'], data_objects['content'], data_objects['startOfParagraph'], data_objects['startTime']])
    cur.executemany("insert into subtitles values (?, ?, ?, ?, ?)", data_rows)


def data_installer():
    """
    Загрузка даных из TED в  subtitles.db
    максимум можно скачать 91793 значений,но это долго
    ограничимся 1000 хотя бы для примера при желании поменяйте занчение на любое
    """
    for link_id in tqdm(range(1000)):
        ted_parser(link_id)

data_installer()






