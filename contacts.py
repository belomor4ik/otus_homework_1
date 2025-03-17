import re
# contacts.py


def show_contacts(actual_data):
    """  Вывести всех пользователей """
    if actual_data:
        print(f'Список пользователей:\n ------------------')
        try:
            for contact in actual_data:
                print(f'ID: {contact[0]}\nИмя: {contact[1]}\nТелефон: {contact[2]}\nКомментарий: {contact[3]}\n ------------------')
        except TypeError:
            print(
                f'ID: {actual_data[0]}\nИмя: {actual_data[1]}\nТелефон: {actual_data[2]}\nКомментарий: {actual_data[3]}\n ------------------')
    return True


def add_contact(actual_data):
    while True:
        name = input('Введите имя: ')
        if name.isalpha():
            break
        else:
            print('Имя должно состоять из букв. Введите его еще раз.')
    while True:
        phone = input('Введите телефон: ')
        if phone.isnumeric():
            break
        else:
            print('Телефон должен содержать цифры.')
    comment = input('Введите комментарий: ')
    new_id = get_unic_id(actual_data)
    actual_data.append([new_id, name, phone, comment])
    print(f'-------------------\nID: {new_id}\nИмя: {name}\nТелефон: {phone}\nКомментарий: {comment}\n-------------------')
    return actual_data


def find_contact(actual_data):
    """  Функция возвращает список строк с совпадениями пользователей """
    text = input('Введите текст для поиска по справочнику: ')
    coincidences = []
    for contact in actual_data:
        if (re.search(text.lower(), contact[1].lower()) or re.search(text.lower(), contact[2].lower()) or re.search(text.lower(), contact[3].lower())):
                coincidences.append(contact)
    else:
        if len(coincidences) != 0:
            print(f'Найдены следующие пользователи:\n ------------------')
            for contact in coincidences:
                print(f'ID: {contact[0]}\nИмя: {contact[1]}\nТелефон: {contact[2]}\nКомментарий: {contact[3]}\n ------------------')
                return coincidences # Вернуть совпавшие контакты
        else:
            print (f'Совпадений не найдено.')
            return False


def change_contact(actual_data):
    """ Изменить пользователя """
    if actual_data:
        id = input('Введите ID пользователя, которого собираетесь изменить: ')
        if is_id(id):
            modified_contacts = []
            for contact in actual_data:
                if contact[0] != id:
                    modified_contacts.append(contact)
                else:
                    contact[1] = input('Введите новое имя: ')
                    contact[2] = input('Введите новый номер: ')
                    contact[3] = input('Введите новый комментарий: ')
                    modified_contacts.append(contact)
            return modified_contacts
        else:
            print('Нет пользователя с таким ID.')
            return actual_data
    else:
        print('В телефонной книге нет записей.')

def delete_contact(actual_data):
    """ Удалить пользователя """
    if actual_data:
        id = input('Введите ID пользователя, которого собираетесь удалить: ')
        if is_id(id, actual_data):
            modified_contacts = []
            for contact in actual_data:
                if contact[0] != id:
                    modified_contacts.append(contact)
                else:
                    print(f'Пользователь с ID {id} удален')
            return modified_contacts
        else:
            print('Нет пользователя с таким ID.')
            return actual_data
    else:
        print('В телефонной книге нет записей.')


def is_id(id, actual_data):
    """Проверка наличия ID"""
    for row in actual_data:
        if id == row[0]:
            return True
    else:
        return False


def get_unic_id(actual_data):
    """Функция возвращает уникальный ID для заведенного пользователя"""
    try:
        unic_id = False
        while unic_id != True:
            unic_id_contact = random.randint(1, len(actual_data)*30)
            unic_id = is_id_unic(unic_id_contact, actual_data) # Проверяем сгенерированный ID на уникальность
    except:
        unic_id_contact = 1
    return unic_id_contact


def is_id_unic(id_contact, actual_data):
    """Функция проверяет ID пользователя на уникальность"""
    for contact in actual_data:
        if id_contact == int(contact[0]):
            unic_id = False
            break
    else:
        unic_id = True
    return unic_id

