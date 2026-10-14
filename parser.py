import re
from datetime import date
from typing import List, Optional

from errors import (
    InvalidDateError,
    InvalidPlateError,
    MissingFieldError,
    UnknownTypeError,
)
from models import (
    VehiclePass,
    VehiclePassWithCamera,
    VehiclePassWithSpeed,
)

DATE_RE = re.compile(r"\b(\d{4})\.(\d{2})\.(\d{2})\b")
QUOTED_RE = re.compile(r'"([^"]*)"')
FLOAT_RE = re.compile(r"\b\d+\.\d+\b")
PLATE_RE = re.compile(r'^[А-Я]\d{3}[А-Я]{2}\d{2,3}$')


class FieldExtractor:

    @staticmethod
    def date(line: str) -> date:
        clean = re.sub(r'"[^"]*"', " ", line)
        match = DATE_RE.search(clean)
        if not match:
            raise InvalidDateError(f"Дата не найдена: {line!r}")
        year, month, day = map(int, match.groups())
        try:
            return date(year, month, day)
        except ValueError as exc:
            raise InvalidDateError(str(exc)) from exc

    @staticmethod
    def quoted(line: str) -> List[str]:
        return QUOTED_RE.findall(line)

    @staticmethod
    def floats(line: str) -> List[float]:
        clean = re.sub(r"\b\d{4}\.\d{2}\.\d{2}\b", " ", line)
        clean = re.sub(r'"[^"]*"', " ", clean)
        return [float(x) for x in FLOAT_RE.findall(clean)]

    @staticmethod
    def plate(plate: str) -> str:
        if not PLATE_RE.match(plate):
            raise InvalidPlateError(f"Некорректный номер: {plate!r}")
        return plate


class ObjectFactory:

    ALIASES = {
        "фиксация": "base",
        "проезд": "base",
        "автомобиль": "base",
        "скорость": "speed",
        "камера": "camera",
    }

    @classmethod
    def create(cls, kind: str, rec_date: date,
               quoted: List[str], floats: List[float]) -> VehiclePass:
        key = cls.ALIASES.get(kind)
        if key is None:
            raise UnknownTypeError(f"Неизвестный тип: {kind!r}")
        if not quoted:
            raise MissingFieldError("Не найден номер автомобиля")

        plate = FieldExtractor.plate(quoted[0])

        if key == "base":
            return VehiclePass(rec_date, plate)
        if key == "speed":
            if not floats:
                raise MissingFieldError("Не найдена скорость")
            return VehiclePassWithSpeed(rec_date, plate, floats[0])
        if len(quoted) < 2 or len(floats) < 2:
            raise MissingFieldError("Не хватает полей камеры")
        return VehiclePassWithCamera(
            rec_date, plate, quoted[1], floats[0], floats[1]
        )


class RecordParser:

    def __init__(self) -> None:
        self.errors: List[str] = []

    def parse_line(self, line: str) -> Optional[VehiclePass]:
        line = line.strip()
        if not line:
            return None
        kind = line.split()[0].lower()
        rec_date = FieldExtractor.date(line)
        quoted = FieldExtractor.quoted(line)
        floats = FieldExtractor.floats(line)
        return ObjectFactory.create(kind, rec_date, quoted, floats)

    def parse_text(self, text: str) -> List[VehiclePass]:
        self.errors = []
        result: List[VehiclePass] = []
        for number, raw in enumerate(text.splitlines(), start=1):
            try:
                obj = self.parse_line(raw)
            except Exception as exc:            # noqa: BLE001
                self.errors.append(f"Строка {number}: {exc}")
                continue
            if obj is not None:
                result.append(obj)
        return result

    def parse_file(self, path: str) -> List[VehiclePass]:
        try:
            with open(path, encoding="utf-8") as file:
                return self.parse_text(file.read())
        except OSError as exc:
            self.errors.append(f"Ошибка файла {path!r}: {exc}")
            return []