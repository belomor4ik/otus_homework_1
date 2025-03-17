import csv
import sys
import os
from contacts import *
# menu.py

def menu_lvl_0():
    menu = ('Открыть файл', 'Сохранить файл (применить изменения)', 'Выйти из программы (не менять файл)')
    actual_data = backup_file('phone_numbers.csv')
    while True:
        '''Вывести пункты меню на экран'''
        print('\nМеню: ')
        for item in range(len(menu)):
            print(f'{item}:{menu[item]}')
        point = int(input('Выберете пункт меню: '))

        if point == 0:
            '''Выбрать пункт - "Открыть файл". Фактически это - редактирование его содержимого.'''
            current_data = backup_file('phone_numbers.csv')
            actual_data = menu_lvl_1(current_data, actual_data) #Если выбран "Открыть файл", проваливаемся на следующий уровень меню, забирая содержимое телефонной книги
        elif point == 1:
            '''Выбрать пункт - "Сохранить файл". Это запись изменений в файл либо сохранение его в неизменном виде.'''
            try:
                os.remove('phone_numbers.csv')
            except FileExistsError:
                print('Файла не существует!')
            with open('phone_numbers.csv', 'a', encoding='UTF-8', newline='') as file:
                for line in actual_data:
                    file.write(f'{line[0]};{line[1]};{line[2]};{line[3]}\n')
        elif point == 2:
            '''Выйти из программы без сохранения'''
            sys.exit()
        else:
            print('Вы ошиблись. Введите ID пункта, который Вы хотите открыть.')


def menu_lvl_1(current_data, actual_data):
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


def backup_file(path):
    with open(path, 'r', encoding='UTF-8', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        actual_data = []
        for contact in reader:
            actual_data.append(contact)
        return actual_data