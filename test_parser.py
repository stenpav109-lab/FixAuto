from datetime import date

import pytest

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
from parser import FieldExtractor, ObjectFactory, RecordParser


def test_date_ok():
    assert FieldExtractor.date('Фиксация 2024.09.15 "А123БВ777"') \
        == date(2024, 9, 15)


def test_date_missing():
    with pytest.raises(InvalidDateError):
        FieldExtractor.date('Фиксация "А123БВ777"')


def test_date_bad_calendar():
    with pytest.raises(InvalidDateError):
        FieldExtractor.date('Фиксация 2024.13.40 "А123БВ777"')


def test_floats_ignore_date():
    assert FieldExtractor.floats(
        'Камера 2024.09.17 "М789НР197" "CAM-42" 55.7558 37.6173'
    ) == [55.7558, 37.6173]


def test_plate_ok():
    assert FieldExtractor.plate("А123БВ777") == "А123БВ777"


def test_plate_bad():
    with pytest.raises(InvalidPlateError):
        FieldExtractor.plate("XYZ")



def test_factory_base():
    obj = ObjectFactory.create("фиксация", date(2024, 9, 15),
                               ["А123БВ777"], [])
    assert isinstance(obj, VehiclePass)


def test_factory_speed():
    obj = ObjectFactory.create("скорость", date(2024, 9, 16),
                               ["В456ЕК99"], [87.5])
    assert isinstance(obj, VehiclePassWithSpeed)


def test_factory_camera():
    obj = ObjectFactory.create("камера", date(2024, 9, 17),
                               ["М789НР197", "CAM-42"],
                               [55.7558, 37.6173])
    assert isinstance(obj, VehiclePassWithCamera)


def test_factory_unknown():
    with pytest.raises(UnknownTypeError):
        ObjectFactory.create("нечто", date(2024, 1, 1),
                             ["А111АА77"], [])


def test_factory_missing_plate():
    with pytest.raises(MissingFieldError):
        ObjectFactory.create("фиксация", date(2024, 1, 1), [], [])



def test_parser_ok():
    parser = RecordParser()
    objects = parser.parse_text(
        'Фиксация 2024.09.15 "А123БВ777"\n'
        'Скорость 2024.09.16 "В456ЕК99" 87.5\n'
    )
    assert len(objects) == 2
    assert parser.errors == []


def test_parser_collects_errors():
    parser = RecordParser()
    objects = parser.parse_text(
        'Фиксация 2024.09.15 "А123БВ777"\n'
        'Неизвестно 2024.01.01 "А111АА77"\n'
        'Фиксация 2024.02.02\n'
    )
    assert len(objects) == 1
    assert len(parser.errors) == 2