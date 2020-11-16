import requests
import time
import pandas as pd
import sqlalchemy
import json
import os
from sqlalchemy import engine as sql
from IPython import display


def getPage(works_name, area, page=0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    params = {
        'text': 'NAME:{}'.format(works_name),
        'area': area,
        'page': page,
        'per_page': 100
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


class Vacancy:
    def __init__(self, works_name, area):
        self.works_name = works_name
        self.area = area

    def get_vacancies_list(self):
        for page in range(0, 20):

            jsObj = json.loads(getPage(self.works_name, self.area, page))
            nextFileName = './docs/pagination/{}.json'.format(len(os.listdir('./docs/pagination')))
            with open(nextFileName, 'w', encoding='utf8') as f:
                f.write(json.dumps(jsObj, ensure_ascii=False))
                jsonText = f.read()

            jsonObj = json.loads(jsonText)

            for v in jsonObj['items']:
                req = requests.get(v['url'])
                data = req.content.decode()
                req.close()
                fileName = './docs/vacancies/{}.json'.format(v['id'])
                with open(fileName, 'w', encoding='utf8') as f:
                    f.write(data)

        print('All vacancies sa')


test = Vacancy('Программист', 4)
test.get_vacancies_list()
