"""Модуль для демонстрации работы программы"""

import os
from dotenv import load_dotenv
from client_manager import CallCentre


def load_password(conf_path: str) -> str:
    """
    Функция для чтения пароля из файла
    :param conf_path: [str] - путь к файлу с паролем
    :result: [str] - пароль
    """
    if os.path.exists(conf_path):
        load_dotenv(conf_path)
    else:
        raise FileNotFoundError("Файл не был найден.")

    return os.getenv("PASSWORD")

def test_create_tables(manager: CallCentre) -> None:
    """
    Функция для тестирования создания таблиц в базе данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    print("--1--")
    manager.create_tables()
    # демонстрация игнорирования повторного создания:
    print("--1-errors--")
    manager.create_tables()

def test_add_clients(manager: CallCentre) -> None:
    """
    Функция для тестирования добавления клиентов в базу данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    # добавление клиентов.
    print("--2--")
    manager.add_client("Виктор", "Цой", "viktor_tsoy@gmail.com")
    manager.add_client("Валентин", "Чебуреков", "4eburekov@yandex.ru")
    manager.add_client("Сергей", "Киблер", "k1bler_nag1bator@pfur.ru")
    manager.add_client("Тестировщик", "Удаления", "test@test.ru")
    manager.add_client("Тестировщик", "Удаления", "test2@test2.ru")
    manager.add_client("Виктор", "Канарейкин", "kanareyka@mail.ru")
    manager.add_client("Виктор", "Киблер", "kibla@gangster.ru")
    # демонстрация защиты от некорректных данных:
    print("--2.errors--")
    manager.add_client("виктор", "Цой", "viktor_tsoy@bk.ru")
    manager.add_client("Виктор", "Цdой", "viktor_tsoy@bk.ru")
    manager.add_client("Виктор", "Цой", "viktor_tsoy@gmail.com")
    manager.add_client("Виктор", "Цой", "viktor_tsoy@gmail.com")

def test_add_phones(manager: CallCentre) -> None:
    """
    Функция для тестирования добавления телефонов в базу данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    # добавление телефонов
    print("--3--")
    manager.add_phone(1, "+79938779124")
    manager.add_phone(1, "+78455657789")
    manager.add_phone(2, "+78909884636")
    manager.add_phone(2, "+79932567784")
    manager.add_phone(2, "+73232456644")
    manager.add_phone(2, "+74738438833")
    manager.add_phone(3, "+78939564645")
    # демонстрация защиты от некорректных данных:
    print("--3.errors--")
    manager.add_phone(1, "+7845565778119")
    manager.add_phone(2, "+78909884636")
    manager.add_phone(3, "89158443567")
    manager.add_phone(15, "+79158443567")

def test_edit_client_info(manager: CallCentre) -> None:
    """
    Функция для тестирования изменения данных о клиенте в базе данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    # изменение данных о клиенте
    print("--4--")
    manager.edit_client_info(1, name="Артём")
    manager.edit_client_info(2, surname="Ставкин")
    manager.edit_client_info(3, email="1132233497@pfur.ru")
    manager.edit_client_info(1, name="Иосиф", surname="Григорян")
    manager.edit_client_info(2, name="Кирилл", surname="Кривенков", email="krivenkov_ka@mgtu.ru")
    # демонстрация защиты от некорректных данных:
    print("--4.errors--")
    manager.edit_client_info(15, name="Артём")
    manager.edit_client_info(1, email=".244.@gmail.com")
    manager.edit_client_info(3)
    manager.edit_client_info(2, name="Joseppo")

def test_delete_phones(manager: CallCentre) -> None:
    """
    Функция для тестирования удаления телефонов из базы данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    # удаление телефонов
    print("--5--")
    manager.delete_phone("+79938779124")
    manager.delete_phone("+78455657789")
    # демонстрация защиты от некорректных данных:
    print("--5.errors--")
    manager.delete_phone("+79999999999")

def test_delete_clients(manager: CallCentre) -> None:
    """
    Функция для тестирования удаления клиентов из базы данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    # удаление существующего клиента
    print("--6--")
    manager.delete_client_by_fields(email='test@test.ru')
    manager.delete_client_by_fields(client_id=5)
    # демонстрация защиты от некорректных данных:
    print("--6.errors--")
    manager.delete_client_by_fields(email='test@tttttttest.ru')
    manager.delete_client_by_fields(client_id=1242)
    manager.delete_client_by_fields()

def test_find_clients(manager: CallCentre) -> None:
    """
    Функция для тестирования поиска клиентов в базе данных
    :param manager: [CallCentre] - объект класса CallCentre. Инструмент
                                    для работы с базой данных
    :result: [None] - функция успешно завершает работу в случае отсутсвия
                        ошибок во время исполнения кода
    """
    # поиск клиентов
    print("--7--")
    manager.find_client_by_fields(name="Кирилл")
    manager.find_client_by_fields(name="Виктор")
    manager.find_client_by_fields(surname="Киблер")
    manager.find_client_by_fields(name="Сергей", surname="Киблер")
    manager.find_client_by_fields(email="krivenkov_ka@mgtu.ru")
    manager.find_client_by_fields(phone="+78939564645")
    # поиск несуществующих клиентов:
    print("--7.errors--")
    manager.find_client_by_fields(name="Викторsss")
    manager.find_client_by_fields(surname="Киблерaa")
    manager.find_client_by_fields(email="krivenkodsv_ka@mgtu.ru")
    manager.find_client_by_fields(phone="+7893956499645")

def main():
    """Функция для демонстрации всех функций программы"""
    path_to_config_file = 'config.env'  # путь до файла с паролем
    name_of_database = 'call_centre'    # имя базы данных
    name_of_user = 'postgres'           # имя пользователя

    client_manager = CallCentre(
        load_password(path_to_config_file),
        name_of_database,
        name_of_user
    )

    client_manager.drop_all_tables()

    test_create_tables(client_manager)
    test_add_clients(client_manager)
    test_add_phones(client_manager)
    test_edit_client_info(client_manager)
    test_delete_phones(client_manager)
    test_delete_clients(client_manager)
    test_find_clients(client_manager)

    client_manager.close_connection()

if __name__ == "__main__":
    main()
