import json


def newssave(data):
    with open('static/json/newsList.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def userssave(data):
    with open('static/json/usersList.json', 'w', encoding='utf-8')as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
