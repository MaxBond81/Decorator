from datetime import datetime
import csv
import re


def logger(old_function):
    def new_function(*args, **kwargs):
        data = {"Дата и время вызова функции": datetime.now()}
        result = old_function(*args, **kwargs)
        data["Имя функции"] = old_function.__name__
        data["Аргументы функции"] = f"{args} и {kwargs}"
        data["Результат функции"] = result
        with open("main.log", "w", encoding="utf-8") as new_file:
            for i in data:
                new_file.write(f'{i}: {data[i]}\n')
        return result

    return new_function

# Функция приведения в порядок адресную книгу, используя регулярные выражения
@logger
def normalised_contacts(path):
    pattern_phone = r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*'
    sub_phone = r'+7(\2)\3-\4-\5 \6\7'

    with open(f'{path}', encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # Приводим в порядок ФИО
    contact_list_person = []
    for item in contacts_list:
        name = " ".join(item[:3]).split(" ")
        result = [name[0], name[1], name[2], item[3], item[4], re.sub(pattern_phone, sub_phone, item[5]), item[6]]
        contact_list_person.append(result)

    #Удаляем дубли
    contacts_dict = {}
    for person in contact_list_person:
        key = (person[0], person[1])  # Используем фамилию и имя как ключ
        if key not in contacts_dict:
            contacts_dict[key] = person
        else:
            for i in range(2, len(person)):  # Объединяем недостающие данные
                if contacts_dict[key][i] == '':
                    contacts_dict[key][i] = person[i]

    result_contact_list = list(contacts_dict.values())

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_contact_list)

    return "Файл phonebook.csv записан"


normalised_contacts("D:\\phonebook_raw.csv")