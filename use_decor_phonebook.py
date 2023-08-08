import csv
import re
import datetime

def logger(old_function):
    """Ф-ция-декоратор создающая files.log с данными декорируемой ф-ции"""

    def new_function(*args, **kwargs):
        now = datetime.datetime.now()
        name = old_function.__name__
        args_str = ', '.join(map(str, args))
        kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        arguments = ', '.join([args_str, kwargs_str]) if args_str and kwargs_str else args_str or kwargs_str

        with open('main_2.log', 'a') as f:
            f.write(f'{now} - {name} - {arguments}\n')

        result = old_function(*args, **kwargs)
        
        with open('main_2.log', 'a') as f:
            f.write(f'Result: {result}\n')

        return result

    return new_function

@logger
def process_contacts(contacts_list: list) -> list:
    """Ф-ция вычленяет и объединяет части Ф.И.О."""
    
    new_contacts = []
    
    for human in contacts_list[1:]:
        fullname = human[0] + human[1] + human[2]
        
        # Убираем лишние пробелы
        prefix_name = "".join(fullname.split())  
        
        # Разбиваем по заглавным буквам
        indexes = []
        for letter in prefix_name:
            if letter.isupper():
                indexes.append(prefix_name.index(letter))
                
        # Записываем обратно в нужные поля        
        if len(indexes) == 3:
            human[0] = prefix_name[:indexes[1]]
            human[1] = prefix_name[indexes[1]:indexes[2]]
            human[2] = prefix_name[indexes[2]:]
        elif len(indexes) == 2:
            human[0] = prefix_name[:indexes[1]]
            human[1] = prefix_name[indexes[1]:]
        
        new_contacts.append(human)
        
    return new_contacts

@logger
def format_phones(humans: list) -> list:
    """Ф-ция форматирует номера телефонов"""
    
    new_humans = []
    
    phone_pattern = r"(\+7|8)\s*\(?(\d{3})\)?\s*-?(\d{3})\-?(\d{2})\-?(\d{2})\s*\(?(доб\.?)?\s*(\d*)\)?"
    substitution = r"+7(\2)\3-\4-\5 \6\7"
    
    for human in humans:
        
        phone = human[5]
        new_phone = re.sub(phone_pattern, substitution, phone)
        human[5] = new_phone
        
        new_humans.append(human)
        
    return new_humans

@logger
def deduplicate(new_list: list)-> list:
    # Объединения дубликатов
    new_list =[]
    temp_list = []
    temp = []
    for elem in contacts_list:
        tmp = elem[0] + elem[1]
        if tmp not in temp:
            temp.append(tmp)
            new_list.append(elem)
        else:
            temp_list.append(elem)
    # Объединяем данные из дубликатов с новым списком
    for temp_elem in temp_list:
        for elem in new_list:
            if temp_elem[0] == elem[0] and temp_elem[1] == elem[1]:
                for i in range(3, 7):
                    if elem[i] == '' and len(temp_elem[i]) != 0:
                        elem[i] = temp_elem[i]
    
    return new_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    new_contacts_list = format_phones(process_contacts(contacts_list))
        
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(deduplicate(new_contacts_list))