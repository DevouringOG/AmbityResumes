import requests
import json

# URL API и ключ для доступа
url = "http://a0814722.xsph.ru/api/resume"
api_key = "Bxq7HZmXVDHVUW1d2X0J"

# Параметры запроса
params = {
    'age_to': 30,
}

# Заголовки запроса с ключом аутентификации
headers = {
    'Api-key': api_key,
}

# Выполнение GET-запроса
response = requests.get(url, headers=headers, params=params)

# Проверка успешности запроса и сохранение данных в файл
if response.status_code == 200:
    with open("json_api.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)
    print("Данные успешно сохранены в файл 'json_api.json'")
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
