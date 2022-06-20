# homework_bot
telegram-bot, написанный на языке Python. Создался и использовался нами для отслеживания статуса домашних работ. Коротко: если отправленная
на проверку домашняя работа принималась ревьюером, то в мессенджер приходило сообщение, что работа принята. И, наоборот, - если были замечания,
то приходило сообщение о том, что требуется доработка.

## Запуск проекта:
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
Создать .env файл и прописать в нём переменные
* PRACTICUM_TOKEN
* TELEGRAM_TOKEN
* TELEGRAM_CHAT_ID

Запустить проект:

```
python manage.py runserver
```
