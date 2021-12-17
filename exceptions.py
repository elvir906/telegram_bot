class dictionaryIsEempty(Exception):
    """Класс исключения на случай, если словарь окажется пустым."""

    def __init__(self, message='Ответ API не содержит нужных ключей'):
        """Отправка сообщения об ошибке."""
        self.message = message
