from parser import parse_file, parse_text

TEXT = """\
Фиксация 2024.09.15 "А123БВ777"
Скорость 2024.09.16 "В456ЕК99" 87.5
Камера 2024.09.17 "М789НР197" "CAM-42" 55.7558 37.6173
"""


def main() -> None:
    print("== Из строки ==")
    for obj in parse_text(TEXT):
        print(obj)

    print("\n== Из файла ==")
    for obj in parse_file("records.txt"):
        print(obj)


if __name__ == "__main__":
    main()