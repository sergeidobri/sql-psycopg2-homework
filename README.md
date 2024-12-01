# Домашнее задание к лекции «Работа с PostgreSQL из Python»

## Про содержимое репозитроия

Для работы с базой данных, используя модуль `client_manager.py`, необходимо создать экземпляр класса `Call_centre`, передав аргументами пароль, название базы данных и название пользователя.

В файле `test.py` предоставлен пример использования этого класса.

Моя программа загружает пароль из прикрепленного файла `config.env`. Пример заполнения этого файла загружен в репозиторий.

## Про методы создания и удаления таблиц

Метод `.create_tables()` выполняет скрипт, записанный в файле `create_requests.sql` в директории `sql_request`. При необходимости добавление дополнительных ограничений на поля таблиц, изменении самих полей таблиц и т.д. изменить код можно в этих файлах, а использование метода никак не поменяется.

Метод `.drop_all_tables()` выполняет скрипт из файла `drop_requests.sql` в директории `sql_request`

## Про корректные данные

* Корректное имя - это такое имя, которое состоит исключительно из русских букв, независимо от регистра, пробелов и дефисов. Также корректное имя начинается с заглавной буквы.

* Корректная фамилия - это такая фамилия, которая состоит исключительно из русских букв, независимо от регистра, пробелов и дефисов. Также корректная фамилия начинается с заглавной буквы.

* Корректный адрес электронной почты подчиняется следующим условиям:
  * в адресе содержится только один символ `@`;
  * в адресе после символа `@` допустима всего одна точка;
  * все символы - строчные символы латинского алфавита, символ `@`, точки, нижние подчеркивания, а также цифры от 0 до 9;
  * Первый и последний символ не должны быть точками;
  * До символа `@` нужен хотя бы один символ;
  * После символа `@` нужно, чтобы до точки и после точки было хотя бы по одному символу;
  * В адресе не должно быть подряд двух точек.

* Корректный телефон начинается с символа `+`. Если телефон начинается с `+7`, то он должен иметь ровно 10 символов после этого кода региона.

## Про логику работы некоторых отдельных функций

* Метод `.delete_client_by_fields()` способен удалять клиентов только по уникальным полям, т.е. по идентификатору или адресу электронной почты. Нет смысла удалять пользователя по имени или фамилии, потому что существуют тёски и однофамильцы.

* 

