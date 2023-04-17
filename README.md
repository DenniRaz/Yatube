# Проект социальной сети Yatube для блогеров
Yatube - социальная сеть, даёт пользователям возможность создать учётную запись,
публиковать посты, оставлять комментарии и подписываться на любимых авторов.

## Описание проекта:
В проекте социальная сеть Yatube реализованы следующие функции:

* регистрация новых пользователей;
* изменение и восстановления пароля через email;
* добавление/удаление текстовых постов, постов с картинками и возможность
присвоить пост к тематической группе;
* редактирование постов только его автором;
* возможность пользователям оставлять комментарии к постам;
* подписка/отписка на понравившихся авторов;
* создание отдельной ленты с постами авторов, на которых подписан пользователь;
* создание отдельной ленты постов по группам.

## Покрытие тестами:

Покрытие тестами выполнено при помощи ```Unittest```. Каждому тесту соответствует
отдельный файл. Тесты покрывают следующие области:
* тесты кэширования страниц;
* тесты комментариев;
* тесты подписок на авторов;
* тесты форм;
* тесты загрузки изображений;
* тесты моделей базы данных;
* тесты URL проекта;
* тесты view функций.

## Стек технологий:

* [Python 3.7+](https://www.python.org/downloads/)
* [Django 2.2.16](https://www.djangoproject.com/download/)
* [django-debug-toolbar 3.2.4](https://pypi.org/project/django-debug-toolbar/)
* [Faker 12.0.1](https://pypi.org/project/Faker/)
* [mixer 7.1.2](https://pypi.org/project/mixer/)
* [Pillow 9.2.0](https://pypi.org/project/Pillow/)
* [pytest-django 4.4.0](https://pypi.org/project/pytest-django/)
* [pytest-pythonpath 0.7.3](https://pypi.org/project/pytest-pythonpath/)
* [pytest 6.2.4](https://pypi.org/project/pytest/)
* [requests 2.26.0](https://pypi.org/project/requests/)
* [six 1.16.0](https://pypi.org/project/six/)
* [sorl-thumbnail 12.7.0](https://pypi.org/project/sorl-thumbnail/)

## Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:DenniRaz/Yatube.git
```

```
cd yatube
```

* Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
venv/scripts/activate
```

* Установить зависимости из файла ```requirements.txt```:

```
pip install -r requirements.txt
```

* Выполнить миграции:

```
python manage.py migrate
```

* Создать суперпользователя:
```
python manage.py createsuperuser
```
* Запустить проект:

```
python manage.py runserver
```
После создания суперпользователя и запуска проекта, вам будет доступна админка
```/admin```, из которой можно управлять проектом, добавлять и удалять группы, посты,
пользователей и т.д.

## Тесты:
* Тесты запускаются командой:
```
python manage.py test
```
    
или: ```pytest```