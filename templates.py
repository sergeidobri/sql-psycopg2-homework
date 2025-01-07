"""Модуль для хранения шаблонов SQL-запросов и ответов программы"""

class SQL:
    """Класс для хранения шаблонов запросов"""
    request_existance = """SELECT EXISTS (
                                    SELECT *
                                    FROM INFORMATION_SCHEMA.TABLES 
                                    WHERE TABLE_CATALOG = %s
                                    AND TABLE_NAME = %s
                                ) AS table_exists;"""
    find_by_email = """SELECT EXISTS (
                                SELECT * 
                                FROM clients 
                                WHERE email=%s
                            );"""
    insert_request = """INSERT INTO clients(name, surname, email)
                                    VALUES (%s, %s, %s);"""
    delete_by_id = """DELETE FROM clients
                                      WHERE id=%s;"""
    delete_by_email = """DELETE FROM clients
                                        WHERE email=%s;"""
    delete_by_both = """DELETE FROM clients
                                        WHERE email=%s 
                                        AND id=%s;"""

    select_by_id = """SELECT name, surname
                                      FROM clients 
                                      WHERE id=%s;"""
    select_by_email = """SELECT name, surname
                                        FROM clients 
                                        WHERE email=%s;"""
    select_by_both = """SELECT name, surname
                                        FROM clients 
                                        WHERE email=%s 
                                        AND id=%s;"""
    insert_phone = """INSERT INTO phone_numbers(number)
                                            VALUES (%s);"""
    select_by_phone = """SELECT id
                                        FROM phone_numbers 
                                        WHERE number=%s;"""
    insert_client_phone = """INSERT INTO client_phones
                                                VALUES (%s, %s);"""
    select_all_by_id = """SELECT name, surname, email
                                        FROM clients 
                                        WHERE id=%s;"""
    select_id_by_email = """SELECT id
                                        FROM clients 
                                        WHERE email=%s;"""
    update_name = """UPDATE clients
                                    SET name=%s 
                                    WHERE id=%s;"""
    update_surname =  """UPDATE clients
                                    SET surname=%s 
                                    WHERE id=%s;"""
    update_email = """UPDATE clients
                                    SET email=%s 
                                    WHERE id=%s;"""
    update_name_surname = """UPDATE clients
                                    SET name=%s, surname=%s 
                                    WHERE id=%s;"""
    update_email_name = """UPDATE clients
                                    SET email=%s, name=%s 
                                    WHERE id=%s;"""
    update_email_surname = """UPDATE clients
                                    SET email=%s, surname=%s 
                                    WHERE id=%s;"""
    update_all = """UPDATE clients
                                    SET name=%s, surname=%s, email=%s 
                                    WHERE id=%s;"""
    select_all_by_phone = """SELECT ph.id, name, surname
                        FROM clients AS cl
                            JOIN client_phones AS cp ON cp.client_id = cl.id
                            JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                        WHERE ph.number=%s;"""
    delete_by_id = """DELETE FROM phone_numbers
                                    WHERE id=%s;"""
    search_by_name = """SELECT name, surname, email, ph.number
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE name = %s;"""
    search_by_surname = """SELECT name, surname, email, ph.number
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE surname = %s;"""
    search_by_name_surname = """SELECT name, surname, email, ph.number
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE name = %s
                                AND surname = %s;"""
    search_by_email = """SELECT name, surname, email, ph.number
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE email = %s;"""
    search_by_phone = """SELECT name, surname, email, ph.number
                                FROM clients AS cl
                                LEFT JOIN client_phones AS cp ON cp.client_id = cl.id
                                LEFT JOIN phone_numbers AS ph ON ph.id = cp.phone_id
                                WHERE ph.number = %s;"""


class Messages:
    """Класс для хранения сообщений """
    tables_exist = """Таблицы \'clients\', \'phone_numbers\' и \'client_phones\'уже существуют"""
    connect_success = """Подключение к базе данных произошло успешно"""
    create_tables_success = """Таблицы были успешно созданы"""
    delete_tables_success = """В базе данных больше нет таких таблиц"""
    close_connection_success = """Закрытие подключения к базе данных"""
    error_incorrect_email = """Некорректное значение email"""
    error_incorrect_name = """Некорректное имя"""
    error_incorrect_surname = """Некорректная фамилия"""
    error_incorrect_phone = """Номер некорректен"""
    error_client_already_exists = """Клиент с таким адресом электронной почты уже зарегистрирован"""
    error_script_file_does_not_exist = """Возникла ошибка с чтением файла со скриптами"""
    error_empty_search_fields = """Клиента невозможно найти без идентификатора \
или адреса электронной почты"""
    error_id_is_not_int = """Идентификатор должен быть целым числом"""
    error_client_does_not_exist = """Такого клиента нет в базе данных"""
    error_phone_reserved = """Такой телефон уже зарегистрирован и привязан к другому клиенту"""
    error_nothing_to_update = """Обновлять нечего"""
    error_email_already_exists = """Обновить адрес электронной почты невозможно. \
Адрес уже зарегистрирован"""
    error_phone_does_not_exists = """Такого телефона нет в базе данных"""
    error_empty_client_fields = """Недостаточно информации для поиска клиента"""