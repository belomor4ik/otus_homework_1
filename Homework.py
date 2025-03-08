from pathlib import Path
import csv
import random
import re
from pyexpat import ParserCreate
import os.path
import sys


def menu_lvl_0():
    menu = ('Открыть файл', 'Сохранить файл (применить изменения)', 'Выйти из программы (не менять файл)')
    actual_data = backup_file('phone_numbers.csv')
    while True:
        '''Вывести пункты меню на экран'''
        print('\nМеню: ')
        for item in range(len(menu)):
            print(f'{item}:{menu[item]}')
        point= int(input('Выберете пункт меню: '))

        if point == 0:
            '''Выбрать пункт - "Открыть файл". Фактически это - редактирование его содержимого.'''
            current_data = backup_file('phone_numbers.csv')
            actual_data = menu_lvl_1(current_data) #Если выбран "Открыть файл", проваливаемся на следующий уровень меню, забирая содержимое телефонной книги
        elif point == 1:
            '''Выбрать пункт - "Сохранить файл". Это запись изменений в файл либо сохранение его в неизменном виде.'''
            try:
                os.remove('phone_numbers.csv')
            except FileExistsError:
                print('Файла не существует!')
            with open('phone_numbers.csv', 'a', encoding='UTF-8', newline='') as file:
                for line in actual_data:
                    file.write(f'{line[0]};{line[1]};{line[2]};{line[3]}')
        elif point == 2:
            '''Выйти из программы без сохранения'''
            sys.exit()
        else:
            print('Вы ошиблись. Введите ID пункта, который Вы хотите открыть.')


def menu_lvl_1(current_data):
    print('-------------------')
    menu = ('Показать все контакты', 'Добавить контакт', 'Найти контакт', 'Изменить контакт', 'Удалить контакт', 'Закончить редактирование')
    actual_data = current_data
    while True:
        print('Меню: ')
        for item in range(len(menu)):
            print(f'{item}:{menu[item]}')
        point = int(input('\nВыберете пункт меню: '))
        if point == 0:
            show_contacts(actual_data)
        elif point == 1:
            actual_data = add_contact(actual_data)
        elif point == 2:
            find_contact(actual_data)
        elif point == 3:
            actual_data = change_contact(actual_data)
        elif point == 4:
            actual_data = delete_contact(actual_data)
        elif point == 5:
            return actual_data


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
    id = get_unic_id(actual_data)
    actual_data.append([id, name, phone, comment])
    print(f'-------------------\nID: {id}\nИмя: {name}\nТелефон: {phone}\nКомментарий: {comment}\n-------------------')
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


def backup_file(path):
    with open(path, 'r', encoding='UTF-8', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        actual_data = []
        for contact in reader:
            actual_data.append(contact)
        return actual_data


if __name__ == "__main__":
    menu_lvl_0()
