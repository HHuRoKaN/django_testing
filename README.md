`Python` `Django` `Pytest` `Unittest`
# **_Django testing_**
## **_Описание проектов:_**
Ya_news - Django-приложение для новостей с тестами, написанными на Pytest. Включает в себя проверку маршрутов, контента и логики приложения.

Ya_note - Django-приложение для заметок с тестами, написанными на Unittest. Включает в себя проверку маршрутов, контента и логики приложения.

Проект демонстрирует два подхода к тестированию в Django.

**_Основные зависимости:_**
```
django==3.2.15
pytest==7.1.3
pytest-django==4.5.2
```
Полный список зависимостей смотрите в requirements.txt.

## **_Структура репозитория:_**
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```

## 1. **_Установка и настройка_**
1. **_Клонируйте репозиторий:_**
```
git clone git@github.com:HHuRoKaN/django_testing.git
cd django_testing
```
2. **_Создайте виртуальное окружение:_**
```
python -m venv venv
```
3. **_Активируйте виртуальное окружение:_**
```
# Для Linux/MacOS:
source venv/bin/activate

# Для Windows:
venv\Scripts\activate
```
4. **_Установите зависимости:_**
```
pip install -r requirements.txt
```

## 2. **_Запуск тестов_**
```
# Для проекта ya_news (Pytest)
cd ya_news
pytest

# Для проекта ya_note (Unittest)
cd ya_note
python manage.py test
```

### Автор
Александр Кубенин
