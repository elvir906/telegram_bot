## Telegram-bot

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

Telegram-bot, написанный на языке Python. Создался и использовался нами для отслеживания статуса домашних работ. Коротко: если отправленная
на проверку домашняя работа принималась ревьюером, то в мессенджер приходило сообщение, что работа принята. И, наоборот, - если были замечания,
то приходило сообщение о том, что требуется доработка.

### Запуск проекта на локальной машине:
Склонировать репозиторий и отрыть папку склонированного репозитория
```
git clone https://github.com/elvir906/telegram_bot
```

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Создать файл окружения .env и прописать в нём переменные:
* PRACTICUM_TOKEN
* TELEGRAM_TOKEN
* TELEGRAM_CHAT_ID

Запустить проект:
```
python manage.py runserver
```
