from pprint import pprint
import requests
import time
from urllib.parse import urlencode
#### Получить userid
#### Получить список его групп
#### Получить список его друзей
#### Взять список групп у каждого друга и сравнить со списком заданного пользователя
#### Записать полученный список групп в файл


def who_is():
    """
    Задаем пользователя для работы
    """
    client_id = input("Введите имя пользователя или его ID: ")
    try:
        int(client_id)
        print(f"Будет использован пользователь {client_id}")
        return int(client_id)
    except ValueError:
        if client_id == "":
            print("Будет использован пользователь по умолчанию, 171691064/eshmargunov")
            return 171691064
        else:
            print(f"Будет использован пользователь {client_id}")
            return client_id


def what_are_user_groups(client_id):
    """
    Запрашиваем группы у пользователя
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_id': client_id,
        'extended': 1,
        'fields': "name,gid,members_count",
        'count': 1000
    }
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params
    )
    # print('?'.join(('https://api.vk.com/method/groups.get', urlencode(params))))
    response_json = response.json()
    usergroups = set()
    print(f"\nИщем группы у пользователя {client_id}: ")
    try:
        for group in response_json['response']['items']:
            print(".", end="")
            usergroups.add(group['id'])
        return usergroups
    except:
        return usergroups


def what_are_my_friends(client_id):
    """
    Получаем список пользователей
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_id': client_id
    }
    response = requests.get(
        'https://api.vk.com/method/friends.get',
        params
    )
    # print('?'.join(('https://api.vk.com/method/friends.get', urlencode(params))))
    response_json = response.json()
    friends = list()
    print(f"\nИщем друзей у пользователя {client_id}: ")
    for friend in response_json['response']['items']:
        print(".", end = "")
        friends.append(friend)
    return friends


def match_users_groups(original_group, original_friends):
    """
    Передаем список оригинальных групп и список друзей
    Итерацией получаем список групп каждого друга и сравниваем множества с исходным
    Возвращаем его
    """
    final_groups = original_group
    for friend in original_friends:
        usergroups = what_are_user_groups(friend)
        diff_groups = final_groups.difference(usergroups)
        final_groups = diff_groups
    return final_groups


TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
original_client = who_is()
input("\nЭтап 1. Определили пользователя. Теперь определим его группы. Press any key to continue:")
original_group = what_are_user_groups(original_client)
input("\nЭтап 2. Определили его группы. Теперь будем определять его друзей. Press any key to continue:")
original_friends = what_are_my_friends(original_client)
input("\nЭтап 3. Определили его друзей. Теперь будем сверять группы. Press any key to continue:")
final_set = match_users_groups(original_group, original_friends)
pprint(final_set)




