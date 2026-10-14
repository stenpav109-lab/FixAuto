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

class VehiclePassWithSpeed(VehiclePass):

    def __init__(self, record_date, plate_number, speed_kmh):
        super().__init__(record_date, plate_number)
        self.speed_kmh = speed_kmh

    def __str__(self):
        return f"{super().__str__()}, скорость = {self.speed_kmh} км/ч"


class VehiclePassWithCamera(VehiclePass):

    def __init__(self, record_date, plate_number,
                 camera_id, latitude, longitude):
        super().__init__(record_date, plate_number)
        self.camera_id = camera_id
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return (f"{super().__str__()}, камера = {self.camera_id}, "
                f"координаты = ({self.latitude}, {self.longitude})")

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
    print("== Базовый тип: parse_record ==")
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

    print("\n== Новые типы ==")

    speed_pass = VehiclePassWithSpeed(date(2024, 9, 16), "В456ЕК99", 87.5)
    print(f"Вход : Скорость 2024.09.16 \"В456ЕК99\" 87.5")
    print(f"Выход: {speed_pass}")

    camera_pass = VehiclePassWithCamera(
        date(2024, 9, 17), "М789НР197", "CAM-42", 55.7558, 37.6173
    )
    print(f'Вход : Камера 2024.09.17 "М789НР197" "CAM-42" 55.7558 37.6173')
    print(f"Выход: {camera_pass}")