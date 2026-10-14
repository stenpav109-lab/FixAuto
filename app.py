"""Демонстрация работы парсера."""
from parser import RecordParser

TEXT = """\
Фиксация 2024.09.15 "А123БВ777"
Скорость 2024.09.16 "В456ЕК99" 87.5
Камера 2024.09.17 "М789НР197" "CAM-42" 55.7558 37.6173
Фиксация 2024.13.40 "XYZ"
Неизвестно 2024.01.01 "А111АА77"
"""


def main() -> None:
    parser = RecordParser()
    for obj in parser.parse_text(TEXT):
        print(obj)
    print("\nОшибки:")
    for err in parser.errors:
        print(err)


if __name__ == "__main__":
    main()