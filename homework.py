import os

import requests
import telegram
import telegram.ext
import time
import exceptions
import hw_status
import logging

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

RETRY_TIME = 60
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logging.info(f'Сообщение {message} отправлено в Telegram')


def get_api_answer(current_timestamp):
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp - 2678400*2}
    try:
        api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        logging.error(f'Эндпоинт {ENDPOINT} не доступен')
    return api_answer.json()


def check_response(response):
    try:
        homework = response.get('homeworks')
    except Exception as error:
        logging.error('В ответе API неожидаемый формат данных')
    return homework


def parse_status(homework):
    try:
        homework_name = homework[0].get('homework_name')
        homework_status = homework[0].get('status')
    except Exception as error:
        logging.error(
            f'Отсутствуют ожидаемые ключи в ответе API'
        )

    if homework_status != hw_status.status:
        try:
            homework_status in HOMEWORK_STATUSES
        except Exception as error:
            logging.error('Недокументированный статус домашки')
            
        verdict = HOMEWORK_STATUSES[homework_status]
        hw_status.status = homework_status
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    else:
        logging.debug('Статус проверки домашней работы не изменился')


def check_tokens():
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        return False


def main():
    """Основная логика работы бота."""
    try:
        check_tokens()==True
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
    except Exception as error:
        logging.critical('Ошибка при чтении токена(-ов)')   
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            send_message(bot, message)
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
