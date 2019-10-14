from pprint import pprint
import requests
import json
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
            user_id = if_user_id_is_not_int(client_id)
            return int(user_id)


def if_user_id_is_not_int(client_id):
    """
    Если пользователь введен не по ID, то получаем его ID
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_ids': client_id,
    }
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params
    )
    response_json = response.json()
    user_id = response_json['response'][0]['id']

    print(f"Печатаем результат превращения - {user_id}")
    return int(user_id)


def what_are_user_groups(client_id):
    """
    Запрашиваем группы у пользователя
    """
    params = {
        'access_token': TOKEN,
        'v': 5.101,
        'user_id': client_id,
        'extended': 1,
        'count': 1000
    }
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params
    )
    response_json = response.json()
    usergroups = set()
    if response_json.get('error') and (response_json['error']['error_msg'] == 'This profile is private' or \
                                       response_json['error']['error_msg'] == 'User was deleted or banned'):
        print(f"\nНе можем посмотреть группы у друга {client_id} "
              f"из-за ошибки {response_json['error']['error_msg']}")
        return usergroups
    elif response_json.get('error') and (response_json['error']['error_msg'] == 'Too many requests per second'):
        print(f"\nПридётся подождать 1 секунду, из-за ошибки {response_json['error']['error_msg'] }")
        time.sleep(1)
        response_json = response.json()
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
    response_json = response.json()
    if response_json.get('error') and (response_json['error']['error_msg'] == 'Too many requests per second'):
        print(f"\nПридётся подождать 1 секунду, потому что ошибка {response_json['error']['error_msg']}")
        time.sleep(1)
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


def detail_groups(set_of_groups):
    """
    Детализируем группы
    """
    print(f"Всего групп получилось - {set_of_groups}")
    final_list = []
    for group in set_of_groups:
        params = {
            'access_token': TOKEN,
            'v': 5.101,
            'group_id': group,
            'fields': "name,members_count"
        }
        response = requests.get(
            'https://api.vk.com/method/groups.getById',
            params
        )
        response_json = response.json()
        if response_json.get('error') and (response_json['error']['error_msg'] == 'Too many requests per second'):
            print(f"\nПридётся подождать 3 секунды, потому что ошибка {response_json['error']['error_msg']}")
            time.sleep(3)
            response_json = response.json()
        for grp in response_json['response']:
            final_dict = {}
            final_dict = {'name': grp['name'], 'gid': grp['id'], 'members_count': grp['members_count']}
            final_list.append(final_dict.copy())
    return final_list

def main():
    original_client = who_is()
    print("\nЭтап 1. Определили пользователя. Теперь определим его группы. Press any key to continue:")
    original_group = what_are_user_groups(original_client)
    print("\nЭтап 2. Определили его группы. Теперь будем определять его друзей. Press any key to continue:")
    original_friends = what_are_my_friends(original_client)
    print("\nЭтап 3. Определили его друзей. Теперь будем сверять группы. Press any key to continue:")
    final_set = match_users_groups(original_group, original_friends)
    print("\nЭтап 4. Получаем подробности групп и записываем в файл. Press any key to continue:")
    detail_json = detail_groups(final_set)
    pprint(detail_json)
    with open('groups.json', mode='w') as file:
        json.dump(detail_json, file, ensure_ascii=False, indent=2)


TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
main()





