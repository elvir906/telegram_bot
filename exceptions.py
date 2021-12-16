class requestCausedError500(Exception):
    def __init__(self, message='Эндпоинт недоступен'):
        self.message = message


class dictionaryIsEempty(Exception):
    def __init__(self, message='Ответ API не содержит нужных ключей'):
        self.message = message
