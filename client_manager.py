"""Модуль с классом для работы с бд"""

import psycopg2
from templates import Messages, SQL


class CallCentre:
    """Класс для инкапсуляции работы с базой данных"""
    def __init__(self, password: str, db_name: str, username='postgres'):
        self.default_params = {
            'password': password,
            'database': db_name,
            'user': username,
            'host': 'localhost'
        }
        self.connect_object = psycopg2.connect(**self.default_params)
        print(Messages.connect_success)

    def create_tables(self, create_file='sql_request/create_requests.sql') -> None:
        """
        Метод для создания таблиц в базе данных. Если таблицы созданы,
        выводится соответвующее сообщение.
        :param create_file: [str] - путь к файлу с sql- create-запросами
        :result: - в результате работы функции в базе создаются таблицы
        """
        conn = self.connect_object

        with conn.cursor() as cur:
            # если все таблицы есть, то смысла создавать таблицы - нет
            flag_all_tables_exist = True

            for table in ('clients', 'client_phones', 'phone_numbers'):
                cur.execute(
                    SQL.request_existance,
                    (self.default_params['database'], table)
                )
                flag_all_tables_exist *= cur.fetchone()[0]

            if flag_all_tables_exist:
                print(Messages.tables_exist)
                return

            try:
                with open(create_file, 'r', encoding='utf-8') as create_requests_file:
                    sql_content = create_requests_file.read().replace('\n', '')
            except FileNotFoundError:
                print(Messages.error_script_file_does_not_exist)
                return

            sql_commands = sql_content.split(';')

            for sql_command in sql_commands:
                if sql_command:  # если не пустая строка
                    cur.execute(sql_command)

            conn.commit()

        print(Messages.create_tables_success)

    def drop_all_tables(self, drop_file='sql_request/drop_requests.sql') -> None:
        """
        Метод для удаления таблиц из базы данных.
        :param drop_file: [str] - путь к файлу с sql- drop-запросами
        :result: - в результате работы функции из базы удаляются таблицы
        """
        conn = self.connect_object
        with conn.cursor() as cur:
            try:
                with open(drop_file, 'r', encoding='utf-8') as drop_requests_file:
                    sql_content = drop_requests_file.read().replace('\n', '')
            except FileNotFoundError:
                print(Messages.error_script_file_does_not_exist)
                return

            sql_commands = sql_content.split(';')
            for sql_command in sql_commands:
                if sql_command:
                    sql_command += ';'
                    cur.execute(sql_command)

            conn.commit()

        print(Messages.delete_tables_success)

    def add_client(self, name: str, surname: str, email: str) -> None:
        """
        Метод для добавления клиента в базу данных.
        :param name: [str] - имя клиента
        :param surname: [str] - фамилия клиента
        :param email: [str] - электронная почта клиента
        :result: [None] - функция добавляет клиента в базу
        """
        # валидируем значения
        if not self._validate_email(email):
            print(Messages.error_incorrect_email)
            return
        if not self._validate_name(name):
            print(Messages.error_incorrect_name)
            return
        if not self._validate_surname(surname):
            print(Messages.error_incorrect_surname)
            return

        conn = self.connect_object

        with conn.cursor() as cur:
            cur.execute(SQL.find_by_email, (email,))
            if not cur.fetchone()[0]:
                cur.execute(SQL.insert_request, (name, surname, email))
                print(f"Клиент {name} {surname} с адресом электронной почты \
{email} был успешно зарегистрирован")
            else:
                print(Messages.error_client_already_exists)
            conn.commit()

    def delete_client_by_fields(self, email=None, client_id=None):
        """
        Метод для удаления клиента из базы данных.
        :param email: [str] - электронная почта клиента
        :param client_id: [int] - идентификатор клиента в базе данных
        :result: [None] - функция удаляет клиента из базы
        """
        mode = ''
        if email is None and client_id is None:
            print(Messages.error_empty_search_fields)
            return
        if email is not None:
            mode += 'e'
        if client_id is not None:
            mode += 'i'
        if (not isinstance(client_id, int)) and client_id is not None:
            print(Messages.error_id_is_not_int)
            return

        conn = self.connect_object

        with conn.cursor() as cur:
            match mode:
                case 'i':
                    cur.execute(SQL.select_by_id, (client_id, ))
                    fio = cur.fetchone()
                    if fio is not None:
                        cur.execute(SQL.delete_by_id, (client_id, ))
                        print(f"Клиент {fio[0]} {fio[1]} с идентификатором\
 {client_id} был успешно удален")
                    else:
                        print(Messages.error_client_does_not_exist)
                case 'e':
                    cur.execute(SQL.select_by_email, (email, ))
                    fio = cur.fetchone()

                    if fio is not None:
                        cur.execute(SQL.delete_by_email, (email, ))
                        print(f"Клиент {fio[0]} {fio[1]} с адресом электронной\
 почты {email} был успешно удален")
                    else:
                        print(Messages.error_client_does_not_exist)
                case 'ei':
                    cur.execute(SQL.select_by_both, (email, client_id))
                    fio = cur.fetchone()

                    if fio is not None:
                        cur.execute(SQL.delete_by_both, (email, client_id))
                        print(f"Клиент {fio[0]} {fio[1]} с адресом электронной\
 почты {email} и идентификатором {client_id} был успешно удален")
                    else:
                        print(Messages.error_client_does_not_exist)

            conn.commit()

    def add_phone(self, client_id: int, phone: str) -> None:
        """
        Метод для добавления телефона в базу данных по айди
        :param client_id: [int] - идентификатор клиента в базе
        :param phone: [str] - телефон
        :result: [None] - функция добавляет телефон клиента в базу и 
                        соединяет его с ним
        """
        if not self._validate_phone(phone):
            print(Messages.error_incorrect_phone)
            return

        conn = self.connect_object

        with conn.cursor() as cur:
            cur.execute(SQL.select_by_id, (client_id, ))
            client_fio = cur.fetchone()
            if client_fio is None:
                print(Messages.error_client_does_not_exist)
                return

            cur.execute(SQL.select_by_phone, (phone, ))
            if cur.fetchone() is not None:
                print(Messages.error_phone_reserved)
                return

            # если существует такой клиент, то создаем телефон и связываем с ним
            cur.execute(SQL.insert_phone, (phone, ))
            conn.commit()

            cur.execute(SQL.select_by_phone, (phone, ))
            phone_id = cur.fetchone()[0]

            cur.execute(SQL.insert_client_phone, (client_id, phone_id))
            print(f"Телефон {phone} был успешно связан с клиентом \
{client_fio[0]} {client_fio[1]}")
            conn.commit()

    def edit_client_info(self, client_id: int, email=None, name=None, surname=None) -> None:
        """
        Метод, изменяющий информацию о клиенте
        :param client_id: [int] - идентификатор клиента
        :param email: [str | None] - электронная почта
        :param name: [str | None] - имя клиента
        :param surname: [str | None] - фамилия клиента
        :result: [None] - функция меняет информацию о клиенте в базе данных 
        """
        mode = ''
        if not isinstance(client_id, int):
            print(Messages.error_id_is_not_int)
            return
        if email is not None:
            if not self._validate_email(email):
                print(Messages.error_incorrect_email)
                return
            mode += 'e'
        if name is not None:
            if not self._validate_name(name):
                print(Messages.error_incorrect_name)
                return
            mode += 'n'
        if surname is not None:
            if not self._validate_surname(surname):
                print(Messages.error_incorrect_surname)
            mode += 's'
        if not mode:
            print(Messages.error_nothing_to_update)
            return

        conn = self.connect_object

        with conn.cursor() as cur:
            cur.execute(SQL.select_all_by_id, (client_id, ))
            fio_email = cur.fetchone()
            if fio_email is None:
                print(Messages.error_client_does_not_exist)
                return

            match mode:
                case 'e':
                    cur.execute(SQL.select_id_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(Messages.error_email_already_exists)
                        return
                    cur.execute(SQL.update_email, (email, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
email: {fio_email[2]} -> {email}")
                case 'n':
                    cur.execute(SQL.update_name, (name, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
Имя: {fio_email[0]} -> {name}")
                case 's':
                    cur.execute(SQL.update_surname, (surname, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
Фамилия: {fio_email[1]} -> {surname}")
                case 'en':
                    cur.execute(SQL.select_id_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(Messages.error_email_already_exists)
                        return
                    cur.execute(SQL.update_email_name, (email, name, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
email: {fio_email[2]} -> {email}, имя: {fio_email[0]} -> {name}")
                case 'es':
                    cur.execute(SQL.select_id_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(Messages.error_email_already_exists)
                        return
                    cur.execute(SQL.update_email_surname, (email, surname, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
email: {fio_email[2]} -> {email}, фамилия: {fio_email[1]} -> {surname}")
                case 'ns':
                    cur.execute(SQL.update_name_surname, (name, surname, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
Имя: {fio_email[0]} -> {name}, фамилия: {fio_email[1]} -> {surname}")
                case 'ens':
                    cur.execute(SQL.select_by_email, (email, ))
                    if cur.fetchone() is not None:
                        print(Messages.error_email_already_exists)
                        return
                    cur.execute(SQL.update_all, (name, surname, email, client_id))
                    print(f"Изменение данных о клиенте с идентификатором {client_id}. \
Имя: {fio_email[0]} -> {name}, фамилия: {fio_email[1]} -> {surname}, \
email: {fio_email[2]} -> {email}")
            conn.commit()

    def delete_phone(self, phone: str) -> None:
        """
        Метод для удаления телефона из базы
        :param phone: [str] - телефон
        :result: [None] - функция удаляет телефон из базы данных
        """
        conn = self.connect_object
        with conn.cursor() as cur:
            cur.execute(SQL.select_all_by_phone, (phone, ))
            id_fio = cur.fetchone()
            if id_fio is None:
                print(Messages.error_phone_does_not_exists)
                return
            phone_id, name, surname = id_fio
            cur.execute(SQL.delete_by_id, (phone_id, ))
            print(f"Номер телефона {phone}, привязанный к пользователю \
{name} {surname}, был успешно удален")
            conn.commit()

    def find_client_by_fields(
            self,
            name=None,
            surname=None,
            email=None,
            phone=None) -> None:
        """
        Метод для поиска клиента по указанным полям полям
        :param name: [str | None] - имя клиента
        :param surname: [str | None] - фамилия клиента
        :param email: [str | None] - электронная почта клиента
        :param phone: [str | None] - телефон
        :result: [None] - функция ищет клиента и выводит сообщение о результате.
        """
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
            print(Messages.error_empty_client_fields)

        conn = self.connect_object

        with conn.cursor() as cur:
            list_clients = []
            match mode:
                case 'n':
                    cur.execute(SQL.search_by_name, (name, ))
                    fio_email_phone_list = cur.fetchall()
                    if not fio_email_phone_list:  # если пустой
                        print(f"Ни один клиент с именем {name} не был найден")
                        return

                    self._print_clients_info(list_clients, fio_email_phone_list)

                case 's':
                    cur.execute(SQL.search_by_surname, (surname, ))
                    fio_email_phone_list = cur.fetchall()
                    if not fio_email_phone_list:  # если пустой
                        print(f"Ни один клиент с фамилией {surname} не был найден")
                        return

                    self._print_clients_info(list_clients, fio_email_phone_list)

                case 'ns':
                    cur.execute(SQL.search_by_name_surname, (name, surname))
                    fio_email_phone_list = cur.fetchall()
                    if not fio_email_phone_list:  # если пустой
                        print(f"Ни один клиент с именем {name} и \
фамилией {surname} не был найден")
                        return

                    self._print_clients_info(list_clients, fio_email_phone_list)

                case _:
                    if 'e' in mode:
                        cur.execute(SQL.search_by_email, (email, ))
                        fio_email_phone = cur.fetchone()
                        if not fio_email_phone:
                            print(f"Ни один клиент с адресом эл.почты \
{email} не был найден")
                            return
                        cl_name, cl_surname, cl_email, cl_phone = fio_email_phone
                        print(f"Найден клиент {cl_name} {cl_surname}. \
Адрес эл.почты: {cl_email}, телефон: {cl_phone}")
                    elif 'p' in mode:
                        cur.execute(SQL.search_by_phone, (phone, ))
                        fio_email_phone = cur.fetchone()
                        if not fio_email_phone:
                            print(f"Ни один клиент с телефоном {phone} не был найден")
                            return
                        cl_name, cl_surname, cl_email, cl_phone = fio_email_phone
                        print(f"Найден клиент {cl_name} {cl_surname}. \
Адрес эл.почты: {cl_email}, телефон: {cl_phone}")

    def close_connection(self):
        """
        Метод для закрытия подключения к базе данных
        """
        print(Messages.close_connection_success)
        self.connect_object.close()

    # статические методы валидации полей
    @staticmethod
    def _validate_email(email):
        result = True
        latin_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        allowed_chars = latin_alphabet + '@._' + '0123456789'

        if '@' not in email:
            result = False
        if email.count('@') > 1:
            result = False

        if '..' in email:
            result = False
        if '.' not in email:
            result = False

        for letter in email:
            if letter not in allowed_chars:
                result = False
        if not email.split('@')[0]:
            result = False
        if not email.split('@')[1]:
            result = False
        if (email[0] == '.' or email[-1] == '.'
        or email.split('@')[0][-1] == '.'
        or email.split('@')[1][0] == '.'):
            result = False
        if email.split('@')[-1].count('.') > 1:
            result = False
        if ((not email.split('@')[-1].split('.')[0])
        or (not email.split('@')[-1].split('.')[1])):
            result = False

        return result

    @staticmethod
    def _validate_name(name):
        result = True
        cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        allowed_chars = cyrillic_alphabet + cyrillic_alphabet.upper() + '- '

        if name[0].upper() != name[0]:
            result = False
        for letter in name:
            if letter not in allowed_chars:
                result = False

        return result

    @staticmethod
    def _validate_surname(surname):
        result = True
        cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        allowed_chars = cyrillic_alphabet + cyrillic_alphabet.upper() + '- '

        if surname[0].upper() != surname[0]:
            result = False
        for letter in surname:
            if letter not in allowed_chars:
                result = False

        return result

    @staticmethod
    def _validate_phone(phone):
        result = True
        if phone[0] != '+':
            result = False
        for digit in phone[1:]:
            if digit not in '0123456789':
                result = False
        if phone[1] == '7' and len(phone) != 12:
            result = False

        return result

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
