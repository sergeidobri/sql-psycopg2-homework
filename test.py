from client_manager import Call_centre
import os
from dotenv import load_dotenv

def load_password(conf_path):
    if os.path.exists(conf_path):
        load_dotenv(conf_path)
    else:
        raise FileNotFoundError("Файл не был найден.")

    return os.getenv("PASSWORD")

def main():
    path_to_confin_file = 'config.env'  # путь до файла с паролем
    name_of_database = 'call_centre'    # имя базы данных
    name_of_user = 'postgres'           # имя пользователя

    client_manager = Call_centre(
        load_password(path_to_confin_file),
        name_of_database,
        name_of_user
    )

    client_manager.drop_all_tables()

    # создание таблиц
    print("--1--")
    client_manager.create_tables()
    # демонстрация игнорирования повторного создания:
    client_manager.create_tables()

    print("--2--")
    # добавление клиентов.
    client_manager.add_client("Виктор", "Цой", "viktor_tsoy@gmail.com")
    client_manager.add_client("Валентин", "Чебуреков", "4eburekov@yandex.ru")
    client_manager.add_client("Сергей", "Киблер", "k1bler_nag1bator@pfur.ru")
    client_manager.add_client("Тестировщик", "Удаления", "test@test.ru")
    client_manager.add_client("Тестировщик", "Удаления", "test2@test2.ru")
    client_manager.add_client("Виктор", "Канарейкин", "kanareyka@mail.ru")
    client_manager.add_client("Виктор", "Киблер", "kibla@gangster.ru")
    # демонстрация защиты от некорректных данных:
    print("--2.errors--")
    client_manager.add_client("виктор", "Цой", "viktor_tsoy@bk.ru")
    client_manager.add_client("Виктор", "Цdой", "viktor_tsoy@bk.ru")
    client_manager.add_client("Виктор", "Цой", "viktor_tsoy@gmail.com")
    client_manager.add_client("Виктор", "Цой", "viktor_tsoy@gmail.com")

    # добавление телефонов
    print("--3--")
    client_manager.add_phone(1, "+79938779124")
    client_manager.add_phone(1, "+78455657789")
    client_manager.add_phone(2, "+78909884636")
    client_manager.add_phone(3, "+78939564645")
    # демонстрация защиты от некорректных данных:
    print("--3.errors--")
    client_manager.add_phone(1, "+7845565778119")
    client_manager.add_phone(2, "+78909884636")
    client_manager.add_phone(3, "89158443567")
    client_manager.add_phone(15, "+79158443567")

    # изменение данных о клиенте
    print("--4--")
    client_manager.edit_client_info(1, name="Артём")
    client_manager.edit_client_info(2, surname="Ставкин")
    client_manager.edit_client_info(3, email="1132233497@pfur.ru")
    client_manager.edit_client_info(1, name="Иосиф", surname="Григорян")
    client_manager.edit_client_info(2, name="Кирилл", surname="Кривенков", email="krivenkov_ka@mgtu.ru")
    # демонстрация защиты от некорректных данных:
    print("--4.errors--")
    client_manager.edit_client_info(15, name="Артём")
    client_manager.edit_client_info(1, email=".244.@gmail.com")
    client_manager.edit_client_info(3)
    client_manager.edit_client_info(2, name="Joseppo")

    # удаление телефонов
    print("--5--")
    client_manager.delete_phone("+79938779124")
    client_manager.delete_phone("+78455657789")
    # демонстрация защиты от некорректных данных:
    print("--5.errors--")
    client_manager.delete_phone("+79999999999")

    # удаление существующего клиента
    print("--6--")
    client_manager.delete_client_by_fields(email='test@test.ru')
    client_manager.delete_client_by_fields(id=5)
    # демонстрация защиты от некорректных данных:
    print("--6.errors--")
    client_manager.delete_client_by_fields(email='test@tttttttest.ru')
    client_manager.delete_client_by_fields(id=1242)
    client_manager.delete_client_by_fields()

    # поиск клиентов
    print("--7--")
    client_manager.find_client_by_fields(name="Виктор")
    client_manager.find_client_by_fields(surname="Киблер")
    client_manager.find_client_by_fields(name="Сергей", surname="Киблер")
    client_manager.find_client_by_fields(email="krivenkov_ka@mgtu.ru")
    client_manager.find_client_by_fields(phone="+78939564645")
    # поиск несуществующих клиентов:
    print("--7.errors--")
    client_manager.find_client_by_fields(name="Викторsss")
    client_manager.find_client_by_fields(surname="Киблерaa")
    client_manager.find_client_by_fields(email="krivenkodsv_ka@mgtu.ru")
    client_manager.find_client_by_fields(phone="+7893956499645")

if __name__ == "__main__":
    main()