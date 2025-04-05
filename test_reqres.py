import requests
import json
from jsonschema import validate
import schemas #наш файл с переменными схем ответов
'''
#---------------------это код, скопированный из постмана

url = "https://reqres.in/api/users"

payload = json.dumps({
  "name": "morpheus",
  "job": "leader"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

#---------------------как лучше писать
response = requests.post(url, headers=headers, data=payload)
#или так:
response = requests.post("https://reqres.in/api/users", headers=headers, data=json.dumps({
  "name": "morpheus",
  "job": "leader"
}))
'''

'''
#оборачиваем в тест
def test():
    response = requests.post("https://reqres.in/api/users", data=json.dumps({
        "name": "morpheus",
        "job": "leader"
    }))

    assert response.status_code == 201

    #-----посмотреть у респонса, что есть
    #response.status_code
    #response.content
    #response.text
    #response.json() #это преобразователь контента в dict, если валидный json вернулся строкой, то создаст словарь питона и можно будет обращаться по ключам response.json()['data']

'''

#------------Проверка схемы ответа
'''
def test_response():
    response = requests.post("https://reqres.in/api/users", data=json.dumps({
        "name": "morpheus",
        "job": "leader"
    }))
    body = response.json() #тело ответа

    assert response.status_code == 201
    with open("post_users.json") as file: #подгрузили наш файл со схемой ответа
        validate(body, schema=json.loads(file.read())) # и метод validate сравнил body с нашей схемой
        #file.read возвращает на строку и мы конвертируем в json с помощью json.loads
'''
#------------пример схемы ответа в переменной
'''
post_users = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "createdAt": {
      "type": "string"
    }
  },
  "required": [
    "id",
    "createdAt"
  ]
}

def test_response1():
    response = requests.post("https://reqres.in/api/users", data=json.dumps({
        "name": "morpheus1",
        "job": "leader"
    }))
    body = response.json() #тело ответа

    assert response.status_code == 201
    validate(body, schema=schemas.post_users) #переменная в файле
'''
#----------------пример проверки бизнес логики, т.е. проверять в ответе то, что отправили

def test_response2():
    job = "morpheus"
    name = "leader"
    response = requests.post("https://reqres.in/api/users", data={
        "name": name,
        "job": job
    })
    body = response.json() #тело ответа

    assert body["name"] == name #распакуем словарь, достаем из него name
    assert body["job"] == job
    #assert body["name"][] #если нужно достать глубже, чем нейм

#---------------Пример передачи Params--------------------

def test_get():
    response = requests.get("https://reqres.in/api/users", params= {"page" : 2})
    #это вместо https://reqres.in/api/users?page=2

#------Если пришел список, Как проверить, что у разных объектов разные названия. Например, запросили юзеров и у них разные id

def test_get_users_returns_unique_users_by_id():
    """Проверяем, что по запросу GET /users вернулись уникальные id пользовталей в data"""
    response = requests.get(
        "https://reqres.in/api/users",
        params={"page": 2},
        verify=False #если есть проблемы с верификацией
    )
    ids = [element["id"] for element in response.json()["data"]] # достаем все ключи id, записываем в список ids
    #len(set(ids)) #а дальше этот список сжимаем и проверяем его len
    set_ids = set(ids[1:]) #убираем 1 элемент из списка и далее сравниваем

    assert len(ids) == len(set_ids)