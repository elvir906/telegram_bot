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

RETRY_TIME = 600
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
    timestamp = current_timestamp or int(time.time() - 3888000)
    params = {'from_date': timestamp}
    api_answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if api_answer.status_code != 200:
        raise exceptions.requestCausedError500
    return api_answer.json()


def check_response(response):
    """Получаем домашние работы с ответа api."""
    hw = response.get('homeworks')
    homework = hw[0]
    return homework

def parse_status(homework):
    """Тут проверяется и определяется статус д/з."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    print(homework_name, homework_status)

a = get_api_answer(int(time.time()) - 3888000)
print(a)
b = check_response(a)
print(b)
parse_status(b)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

send_message(bot, b)
