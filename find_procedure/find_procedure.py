# Задание
# мне нужно отыскать файл среди десятков других
# я знаю некоторые части этого файла (на память или из другого источника)
# я ищу только среди .sql файлов
# 1. программа ожидает строку, которую будет искать (input())
# после того, как строка введена, программа ищет её во всех файлах
# выводит список найденных файлов построчно
# выводит количество найденных файлов
# 2. снова ожидает ввод
# поиск происходит только среди найденных на этапе 1
# 3. снова ожидает ввод
# ...
# Выход из программы программировать не нужно.
# Достаточно принудительно остановить, для этого можете нажать Ctrl + C

# Пример на настоящих данных

# python3 find_procedure.py
# Введите строку: INSERT
# ... большой список файлов ...
# Всего: 301
# Введите строку: APPLICATION_SETUP
# ... большой список файлов ...
# Всего: 26
# Введите строку: A400M
# ... большой список файлов ...
# Всего: 17
# Введите строку: 0.0
# Migrations/000_PSE_Application_setup.sql
# Migrations/100_1-32_PSE_Application_setup.sql
# Всего: 2
# Введите строку: 2.0
# Migrations/000_PSE_Application_setup.sql
# Всего: 1

# не забываем организовывать собственный код в функции

import os
import copy
import locale
import chardet
import re

migrations = 'Migrations'
current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # ваша логика
    def all_list(): # полный список файлов
        migrations_dir = os.path.join(current_dir, migrations)
        os.chdir(migrations_dir)
        file_list = os.listdir(path=".")
        return file_list
    
    def sql_list(all_list): # функция для отбора sql-файлов
        sql_file_list = list() # пустой список sql-файлов
        for i in all_list:
            if i.endswith('.sql'):
                sql_file_list.append(i)
        return sql_file_list
    
    def search_string(sql_list):
        search_file = list() # пустой список файлов для формирования сужающегося списка
        file_list = sql_list
        while True: #бесконечный цикл
            search = input('Введите строку (регистр не важен): ') # ввод строки для поиска
            search_file.clear()
            search = search.lower()
            for i in file_list: #открываем поочередно каждый файл, раскодируем, ищем в нем введенную строку
                with open(os.path.join(current_dir, migrations, i), 'rb') as f:
                    data = f.read()
                    result = chardet.detect(data)
                    data = data.lower()
                with open(i) as f:
                    for line in f:
                        #signal = 0 # сигнал для дострочного выхода из цикла 
                        try:
                            line = line.encode(locale.getpreferredencoding())
                            line = line.decode(result['encoding'])
                        except Exception:
                            print('Ошибка. Строка пропущена')
                        line = line.lower()
                        if re.findall(search, line) != []:
                            search_file.append(i)
                            print(i)
                            break
            print('Всего: {}'.format(len(search_file)))
            file_list = copy.deepcopy(search_file) 
    
    search_string(sql_list(all_list()))
            
    pass