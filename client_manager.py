import psycopg2


class Call_centre:
    def __init__(self, password, db_name, username='postgres'):
        self.default_params = {
            'password': password,
            'database': db_name,
            'user': username,
            'host': 'localhost'
        }
        self.connect_object = psycopg2.connect(**self.default_params)
        print("Подключение к базе данных произошло успешно")

    def create_tables(self, create_file='sql_request//create_requests.sql'):
        conn = self.connect_object
        sql_request_existance = """SELECT EXISTS (
                                    SELECT *
                                    FROM INFORMATION_SCHEMA.TABLES 
                                    WHERE TABLE_CATALOG = %s
                                    AND TABLE_NAME = %s
                                ) AS table_exists;"""

        with conn.cursor() as cur:
            # если все таблицы есть, то смысла создавать таблицы - нет
            flag_all_tables_exist = True

            for table in ('clients', 'client_phones', 'phone_numbers'):
                cur.execute(
                    sql_request_existance, 
                    (self.default_params['database'], table)
                )
                flag_all_tables_exist *= cur.fetchone()[0]

            if flag_all_tables_exist:
                print("Таблицы \'clients\', \'phone_numbers\' и \'client_phones\'\
 уже существуют")
                return
            
            try:
                with open(create_file, 'r') as create_requests_file:
                    sql_content = create_requests_file.read().replace('\n', '')
            except FileNotFoundError:
                print('Возникла ошибка с чтением файла со скриптами.')
                return
            
            sql_commands = sql_content.split(';')

            for sql_command in sql_commands:
                if sql_command:  # если не пустая строка
                    cur.execute(sql_command)
            
            conn.commit()

        print("Таблицы были успешно созданы.")

    def drop_all_tables(self, drop_file='sql_request//drop_requests.sql'):
        conn = self.connect_object
        with conn.cursor() as cur:
            try:
                with open(drop_file, 'r') as drop_requests_file:
                    sql_content = drop_requests_file.read().replace('\n', '')
            except FileNotFoundError:
                print('Возникла ошибка с чтением файла со скриптами')
                return
            
            sql_commands = sql_content.split(';')
            for sql_command in sql_commands:
                if sql_command:
                    sql_command += ';'
                    cur.execute(sql_command)
            
            conn.commit()
                    
        print("В базе данных больше нет таких таблиц.")

    def add_client(self, name, surname, email):
        # валидируем значения
        if not self._validate_email(email):
            print("Некорректное значение email. Клиент не был добавлен в базу данных")
            return
        if not self._validate_name(name):
            print("Некорректное имя. Клиент не был добавлен в базу данных")
            return
        if not self._validate_surname(surname):
            print("Некорректная фамилия. Клиент не был добавлен в базу данных")
            return
        
        conn = self.connect_object

        sql_find_by_email = """SELECT EXISTS (
                                SELECT * 
                                FROM clients 
                                WHERE email=%s
                            );"""
        sql_insert_request = """INSERT INTO clients(name, surname, email)
                                    VALUES (%s, %s, %s);"""
        
        with conn.cursor() as cur:
            cur.execute(sql_find_by_email, (email,))
            if not cur.fetchone()[0]:
                print(f"Клиент {name} {surname} с адресом электронной почты \
{email} был успешно зарегистрирован")
                cur.execute(sql_insert_request, (name, surname, email))
            else:
                print("Клиент с таким адресом электронной почты уже зарегистрирован")
            conn.commit()

    def delete_client_by_fields(self, email=None, id=None):
        mode = ''
        if email is None and id is None:
            print("Клиента невозможно найти без идентификатора или адреса электронной почты")
        if email is not None:
            mode += 'e'  # удаление по id
        if id is not None:
            mode += 'i'  # удаление по email
        if (not isinstance(id, int)) and id is not None:
            print("Идентификатор должен быть целым числом")
            return
        
        conn = self.connect_object
        sql_request_delete_by_id = """DELETE FROM clients 
                                      WHERE id=%s;"""
        sql_request_delete_by_email = """DELETE FROM clients 
                                        WHERE email=%s;"""
        sql_request_delete_by_both = """DELETE FROM clients 
                                        WHERE email=%s 
                                        AND id=%s;"""

        sql_request_select_by_id = """SELECT name, surname 
                                      FROM clients 
                                      WHERE id=%s;"""
        sql_request_select_by_email = """SELECT name, surname 
                                        FROM clients 
                                        WHERE email=%s;"""
        sql_request_select_by_both = """SELECT name, surname 
                                        FROM clients 
                                        WHERE email=%s 
                                        AND id=%s;"""

        with conn.cursor() as cur:
            match mode:
                case 'i':
                    cur.execute(sql_request_select_by_id, (id, ))
                    fio = cur.fetchone()
                    if fio is not None:
                        cur.execute(sql_request_delete_by_id, (id, ))
                        print(f"Клиент {fio[0]} {fio[1]} с идентификатором\
 {id} был успешно удален")
                    else:
                        print("Такого клиента нет в базе данных")
                case 'e':
                    cur.execute(sql_request_select_by_email, (email, ))
                    fio = cur.fetchone()

                    if fio is not None:
                        cur.execute(sql_request_delete_by_email, (email, ))
                        print(f"Клиент {fio[0]} {fio[1]} с адресом электронной\
 почты {email} был успешно удален")
                    else:
                        print("Такого клиента нет в базе данных")
                case 'ei':
                    cur.execute(sql_request_select_by_both, (email, id))
                    fio = cur.fetchone()

                    if fio is not None:
                        cur.execute(sql_request_delete_by_both, (email, id))
                        print(f"Клиент {fio[0]} {fio[1]} с адресом электронной\
 почты {email} и идентификатором {id} был успешно удален")
                    else:
                        print("Такого клиента нет в базе данных")

            conn.commit()
    
    def add_phone(self, id, phone):
        if not self._validate_phone(phone):
            print("Номер некорректен")
            return

        conn = self.connect_object
        sql_request_select_by_id = """SELECT name, surname 
                                        FROM clients 
                                        WHERE id=%s;"""
        sql_request_insert_phone = """INSERT INTO phone_numbers(number) 
                                            VALUES (%s);"""
        sql_request_select_by_phone = """SELECT id 
                                        FROM phone_numbers 
                                        WHERE number=%s;"""
        sql_request_insert_client_phone = """INSERT INTO client_phones 
                                                VALUES (%s, %s);"""

        with conn.cursor() as cur:
            cur.execute(sql_request_select_by_id, (id, ))
            client_fio = cur.fetchone()
            if client_fio is None:
                print("Такого клиента нет в базе данных")
                return

            cur.execute(sql_request_select_by_phone, (phone, ))
            if cur.fetchone() is not None:
                print("Такой телефон уже зарегистрирован и привязан к другому клиенту")
                return
            
            # если существует такой клиент, то создаем телефон и связываем с ним
            cur.execute(sql_request_insert_phone, (phone, ))
            conn.commit()

            cur.execute(sql_request_select_by_phone, (phone, ))
            phone_id = cur.fetchone()[0]

            cur.execute(sql_request_insert_client_phone, (id, phone_id))
            print(f"Телефон {phone} был успешно связан с клиентом \
{client_fio[0]} {client_fio[1]}")
            conn.commit()
        
    def edit_client_info(self, id, email=None, name=None, surname=None):
        mode = ''
        if not isinstance(id, int):
            print("Идентификатор должен быть целым числом")
            return
        if email is not None:
            if not self._validate_email(email):
                print("Такой email некорректен")
                return
            mode += 'e'
        if name is not None:
            if not self._validate_name(name):
                print("Такое имя некорректно")
                return
            mode += 'n'
        if surname is not None:
            if not self._validate_surname(surname):
                print("Такая фамилия некорректна")
            mode += 's'
        if not mode:
            print("Обновлять нечего")
            return
    
        conn = self.connect_object
        sql_request_select_by_id = """SELECT name, surname, email 
                                        FROM clients 
                                        WHERE id=%s;"""
        sql_request_select_by_email = """SELECT id 
                                        FROM clients 
                                        WHERE email=%s;"""

        sql_request_update_name = """UPDATE clients 
                                    SET name=%s 
                                    WHERE id=%s;"""
        sql_request_update_surname =  """UPDATE clients 
                                    SET surname=%s 
                                    WHERE id=%s;"""
        sql_request_update_email = """UPDATE clients 
                                    SET email=%s 
                                    WHERE id=%s;"""
        sql_request_update_name_surname = """UPDATE clients 
                                    SET name=%s, surname=%s 
                                    WHERE id=%s;"""
        sql_request_update_email_name = """UPDATE clients 
                                    SET email=%s, name=%s 
                                    WHERE id=%s;"""
        sql_request_update_email_surname = """UPDATE clients 
                                    SET email=%s, surname=%s 
                                    WHERE id=%s;"""
        sql_request_update_all = """UPDATE clients 
                                    SET name=%s, surname=%s, email=%s 
                                    WHERE id=%s;"""

        with conn.cursor() as cur:
            cur.execute(sql_request_select_by_id, (id, ))
            fio_email = cur.fetchone()
            if fio_email is None:
                print("Такого клиента нет в базе данных")
                return
            
            match mode:
                case 'e':
                    cur.execute(sql_request_select_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(f"Обновить адрес электронной почты невозможно. \
Адрес {email} уже зарегистрирован")
                        return
                    cur.execute(sql_request_update_email, (email, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
email: {fio_email[2]} -> {email}")
                case 'n':
                    cur.execute(sql_request_update_name, (name, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
Имя: {fio_email[0]} -> {name}")
                case 's':
                    cur.execute(sql_request_update_surname, (surname, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
Фамилия: {fio_email[1]} -> {surname}")
                case 'en':
                    cur.execute(sql_request_select_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(f"Обновить адрес электронной почты невозможно. \
Адрес {email} уже зарегистрирован")
                        return
                    cur.execute(sql_request_update_email_name, (email, name, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
email: {fio_email[2]} -> {email}, имя: {fio_email[0]} -> {name}")
                case 'es':
                    cur.execute(sql_request_select_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(f"Обновить адрес электронной почты невозможно. \
Адрес {email} уже зарегистрирован")
                        return
                    cur.execute(sql_request_update_email_surname, (email, surname, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
email: {fio_email[2]} -> {email}, фамилия: {fio_email[1]} -> {surname}")
                case 'ns':
                    cur.execute(sql_request_update_name_surname, (name, surname, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
Имя: {fio_email[0]} -> {name}, фамилия: {fio_email[1]} -> {surname}")
                case 'ens':
                    cur.execute(sql_request_select_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(f"Обновить адрес электронной почты невозможно. \
Адрес {email} уже зарегистрирован")
                        return
                    cur.execute(sql_request_update_all, (name, surname, email, id))
                    print(f"Изменение данных о клиенте с идентификатором {id}. \
Имя: {fio_email[0]} -> {name}, фамилия: {fio_email[1]} -> {surname}, \
email: {fio_email[2]} -> {email}")
            conn.commit()

    def delete_phone(self, phone):
        conn = self.connect_object
        sql_request_select_by_phone = """SELECT ph.id, name, surname 
                        FROM clients AS cl
                            JOIN client_phones AS cp ON cp.client_id = cl.id
                            JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                        WHERE ph.number=%s;"""
        sql_request_delete_by_id = """DELETE FROM phone_numbers 
                                    WHERE id=%s;"""
        with conn.cursor() as cur:
            cur.execute(sql_request_select_by_phone, (phone, ))
            id_fio = cur.fetchone()
            if id_fio is None:
                print("Такого телефона нет в базе данных")
                return
            phone_id, name, surname = id_fio
            cur.execute(sql_request_delete_by_id, (phone_id, ))
            print(f"Номер телефона {phone}, привязанный к пользователю \
{name} {surname}, был успешно удален")
            conn.commit()
    
    def find_client_by_fields(self, name=None, surname=None, email=None, phone=None):
        mode = ''
        if name is not None:
            mode += 'n'
        if surname is not None:
            mode += 's'
        if email is not None:
            mode += 'e'
        if phone is not None:
            mode += 'p'
        if not mode:
            print("Недостаточно информации для поиска клиента")
        
        conn = self.connect_object
        sql_request_select_by_name = """SELECT name, surname, email, ph.number 
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE name = %s;"""
        sql_request_select_by_surname = """SELECT name, surname, email, ph.number 
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE surname = %s;"""
        sql_request_select_by_name_surname = """SELECT name, surname, email, ph.number 
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE name = %s
                                AND surname = %s;"""
        sql_request_select_by_email = """SELECT name, surname, email, ph.number 
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE email = %s;"""
        sql_request_select_by_phone = """SELECT name, surname, email, ph.number 
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE ph.number = %s;"""

        with conn.cursor() as cur:
            list_clients = []
            match mode:
                case 'n':
                    cur.execute(sql_request_select_by_name, (name, ))
                    fio_email_phone_list = cur.fetchall()
                    if not fio_email_phone_list:  # если пустой
                        print(f"Ни один клиент с именем {name} не был найден")
                        return
                    
                    self._print_clients_info(list_clients, fio_email_phone_list)
 
                case 's':
                    cur.execute(sql_request_select_by_surname, (surname, ))
                    fio_email_phone_list = cur.fetchall()
                    if not fio_email_phone_list:  # если пустой
                        print(f"Ни один клиент с фамилией {surname} не был найден")
                        return
                    
                    self._print_clients_info(list_clients, fio_email_phone_list)

                case 'ns':
                    cur.execute(sql_request_select_by_name_surname, (name, surname))
                    fio_email_phone_list = cur.fetchall()
                    if not fio_email_phone_list:  # если пустой
                        print(f"Ни один клиент с именем {name} и \
фамилией {surname} не был найден")
                        return
                    
                    self._print_clients_info(list_clients, fio_email_phone_list)

                case _:
                    if 'e' in mode:
                        cur.execute(sql_request_select_by_email, (email, ))
                        fio_email_phone = cur.fetchone()
                        if not fio_email_phone: 
                            print(f"Ни один клиент с адресом эл.почты \
{email} не был найден")
                            return
                        cl_name, cl_surname, cl_email, cl_phone = fio_email_phone
                        print(f"Найден клиент {cl_name} {cl_surname}. \
Адрес эл.почты: {cl_email}, телефон: {cl_phone}")
                    elif 'p' in mode:
                        cur.execute(sql_request_select_by_phone, (phone, ))
                        fio_email_phone = cur.fetchone()
                        if not fio_email_phone: 
                            print(f"Ни один клиент с телефоном {phone} не был найден")
                            return
                        cl_name, cl_surname, cl_email, cl_phone = fio_email_phone
                        print(f"Найден клиент {cl_name} {cl_surname}. \
Адрес эл.почты: {cl_email}, телефон: {cl_phone}")

    def close_connection(self):
        print("Закрытие подключения к базе данных")
        self.connect_object.close()

    # статические методы валидации полей
    @staticmethod
    def _validate_email(email):
        latin_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        allowed_chars = latin_alphabet + '@._' + '0123456789'

        if '@' not in email:
            return False
        if email.count('@') > 1:
            return False
        
        if '..' in email:
            return False
        if '.' not in email:
            return False
        
        for letter in email:
            if letter not in allowed_chars:
                return False
        if not email.split('@')[0]:
            return False
        if not email.split('@')[1]:
            return False
        if (email[0] == '.' or email[-1] == '.' 
        or email.split('@')[0][-1] == '.' 
        or email.split('@')[1][0] == '.'):
            return False
        if email.split('@')[-1].count('.') > 1:
            return False
        if ((not email.split('@')[-1].split('.')[0]) 
        or (not email.split('@')[-1].split('.')[1])):
            return False
        
        return True
    
    @staticmethod
    def _validate_name(name):

        cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        allowed_chars = cyrillic_alphabet + cyrillic_alphabet.upper() + '- '

        if name[0].upper() != name[0]:
            return False
        for letter in name:
            if letter not in allowed_chars:
                return False
        
        return True

    @staticmethod
    def _validate_surname(surname):

        cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        allowed_chars = cyrillic_alphabet + cyrillic_alphabet.upper() + '- '
        
        if surname[0].upper() != surname[0]:
            return False
        for letter in surname:
            if letter not in allowed_chars:
                return False
        
        return True
    
    @staticmethod
    def _validate_phone(phone):
        
        if phone[0] != '+':
            return False
        for digit in phone[1:]:
            if digit not in '0123456789':
                return False
        if phone[1] == '7' and len(phone) != 12:
            return False
        
        return True
    
    @staticmethod
    def _print_clients_info(list_clients, fio_email_phone_list):
        for cl_name, cl_surname, cl_email, cl_phone in fio_email_phone_list:
            if not list_clients:
                list_clients.append({
                    'name': cl_name,
                    'surname': cl_surname,
                    'email': cl_email,
                    'phones': [cl_phone]
                })
                continue

            for client in list_clients:
                if (cl_name == client['name'] 
                    and cl_surname == client['surname'] 
                    and cl_email == client['email']):
                    client['phones'].append(cl_phone)
                    break
            else:
                list_clients.append({
                    'name': cl_name,
                    'surname': cl_surname,
                    'email': cl_email,
                    'phones': [cl_phone]
                })
        if len(list_clients) > 1:
            cnt = 1
            print("Найдены следующие соответствия:")
            for client in list_clients:
                print(f"{cnt}. {client['name']} {client['surname']}.\
 Адрес электронной почты: {client['email']}, телефон(ы): \
{', '.join(client['phones']) if client['phones'][0] is not None else None}")
                cnt += 1
        else:
            client = list_clients[0]
            print(f"Найден клиент {client['name']} {client['surname']}.\
 Адрес электронной почты: {client['email']}, телефон(ы): \
{', '.join(client['phones']) if client['phones'][0] is not None else None}")
    