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
        return (f"Фиксация проезда: дата = "
                f"{self.record_date:%Y.%m.%d}, "
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


def parse_line(line: str):
    line = line.strip()
    if not line:
        return None

    kind = line.split()[0].lower()

    # 1) сначала вытаскиваем дату
    date_match = re.search(r'\b(\d{4})\.(\d{2})\.(\d{2})\b', line)
    year, month, day = map(int, date_match.groups())
    record_date = date(year, month, day)

    # 2) строки в кавычках
    quoted = re.findall(r'"([^"]*)"', line)

    # 3) удаляем дату И кавычки — чтобы не путались с числами
    clean = re.sub(r'\b\d{4}\.\d{2}\.\d{2}\b', ' ', line)
    clean = re.sub(r'"[^"]*"', ' ', clean)

    # 4) оставшиеся дробные числа — это скорость / широта / долгота
    floats = [float(x) for x in re.findall(r'\b\d+\.\d+\b', clean)]

    if kind == "скорость":
        return VehiclePassWithSpeed(record_date, quoted[0], floats[0])
    if kind == "камера":
        return VehiclePassWithCamera(
            record_date, quoted[0], quoted[1], floats[0], floats[1]
        )
    return VehiclePass(record_date, quoted[0] if quoted else None)


def parse_text(text):
    result = []
    for raw in text.splitlines():
        obj = parse_line(raw)
        if obj is not None:
            result.append(obj)
    return result


def parse_file(path):
    with open(path, encoding="utf-8") as f:
        return parse_text(f.read())


if __name__ == "__main__":
    print("== Из строки ==")
    TEXT = (
        'Фиксация 2024.09.15 "А123БВ777"\n'
        'Скорость 2024.09.16 "В456ЕК99" 87.5\n'
        'Камера 2024.09.17 "М789НР197" "CAM-42" 55.7558 37.6173\n'
    )
    for obj in parse_text(TEXT):
        print(obj)

    print("\n== Из файла ==")
    for obj in parse_file("records.txt"):
        print(obj)