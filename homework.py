import os

import requests
import telegram
import telegram.ext
import time
import hw_status
import logging
import exceptions

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

BOT = telegram.Bot(token=TELEGRAM_TOKEN)

RETRY_TIME = 60
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Функция отправки сообщения 'message' ботом 'bot'."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f'Сообщение {message} отправлено в Telegram')
    except Exception as error:
        logging.error(f'{error}. Бот не доступен')


def get_api_answer(current_timestamp):
    """Здесь мы получаем ответ от api и преобразовываем его в json-формат."""
    timestamp = current_timestamp or int(time.time()) - 3888000
    params = {'from_date': timestamp}
    api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if api_answer.status_code != 200:
        logging.error(f'Эндпоинт {ENDPOINT} недоступен')
        send_message(BOT, f'Эндпоинт {ENDPOINT} недоступен')
        raise exceptions.requestCausedError500
    return api_answer.json()


def check_response(response):
    """Получаем домашние работы с ответа api."""
    if response != {}:
        if type(response) != dict:
            response = dict(response)
            hw = response.get('homeworks')
            homework = hw[0]
        else:
            hw = response.get('homeworks')
            homework = hw[0]
    else:
        send_message(BOT, 'Отсутствуют ожидаемые ключи в ответе API')
        logging.error('Отсутствуют ожидаемые ключи в ответе API')
        raise exceptions.dictionaryIsEempty
    return homework


def parse_status(homework):
    """Тут проверяется и определяется статус д/з."""
    current_timestamp = int(time.time()) - 3888000
    timestamp = current_timestamp or int(time.time()) - 3888000
    if type(homework) != dict:
        homework = {'homework': homework[0], 'current_date': timestamp}
        homework_name = homework.get('homework_name')
        homework_status = homework.get('status')
    else:
        homework_name = homework.get('homework_name')
        homework_status = homework.get('status')
    if homework_status != hw_status.status:
        if (homework_status in HOMEWORK_STATUSES) and (homework_name):
            verdict = HOMEWORK_STATUSES[homework_status]
            hw_status.status = homework_status
            text = ('Изменился статус проверки '
                    f'работы "{homework_name}". {verdict}')
            return text
        else:
            send_message(BOT, 'Обнаружен незадокументированный статус дз')
            logging.error('Обнаружен незадокументированный статус дз')
            raise KeyError
    else:
        logging.debug(
            f'Статус проверки {homework_status} домашней '
            f'работы {homework_name} не изменился'
        )


def check_tokens():
    """Проверка токенов."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        if not PRACTICUM_TOKEN:
            logging.critical('Отсутствует обязательная '
                             f'переменная окружения {PRACTICUM_TOKEN}')
        if not TELEGRAM_TOKEN:
            logging.critical('Отсутствует обязательная '
                             f'переменная окружения {TELEGRAM_TOKEN}')
        if not TELEGRAM_CHAT_ID:
            logging.critical('Отсутствует обязательная '
                             f'переменная окружения {TELEGRAM_CHAT_ID}')
        return False


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time()) - 3888000
    while check_tokens:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            send_message(bot, message)
            logging.info(f'Бот отправил сообщение {message}')
            current_timestamp = int(time.time()) - 3888000
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            logging.error(message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
