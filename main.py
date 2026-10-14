import re
from datetime import date


class VehiclePass:

    def __init__(self, record_date: date, plate_number: str):
        self.record_date = record_date
        self.plate_number = plate_number

    def __repr__(self):
        return (f"VehiclePass(record_date={self.record_date!r}, "
                f"plate_number={self.plate_number!r})")

    def __str__(self):
        return (f"Фиксация проезда: дата = {self.record_date.strftime('%Y.%m.%d')}, "
                f"номер автомобиля = {self.plate_number}")


PLATE_PATTERN = re.compile(r'^[А-Я]\d{3}[А-Я]{2}\d{2,3}$')

def parse_record(line: str) -> VehiclePass:

    quoted = re.findall(r'"([^"]*)"', line)
    plate = quoted[0] if quoted else None

    line_wo_quotes = re.sub(r'"[^"]*"', ' ', line)

    date_match = re.search(r'\b(\d{4})\.(\d{2})\.(\d{2})\b', line_wo_quotes)
    year, month, day = map(int, date_match.groups())
    record_date = date(year, month, day)

    return VehiclePass(record_date, plate)


if __name__ == "__main__":

    samples = [
        'Фиксация 2024.09.15 "А123БВ777"',
        'Проезд 2023.01.01 "В456ЕК99"',
        'Автомобиль 2022.12.31 "М789НР197"',
        'Камера 2025.06.07 "О321РС750"',
    ]

    for s in samples:
        obj = parse_record(s)
        print(f"Вход : {s}")
        print(f"Выход: {obj}")