class ParseError(Exception):
    """Базовая ошибка разбора."""


class MissingFieldError(ParseError):
    """Не найдено обязательное поле."""


class InvalidDateError(ParseError):
    """Некорректная дата."""


class InvalidPlateError(ParseError):
    """Некорректный номер автомобиля."""


class UnknownTypeError(ParseError):
    """Неизвестный тип объекта."""