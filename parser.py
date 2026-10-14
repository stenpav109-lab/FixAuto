import re
from datetime import date
from typing import List, Optional

from models import (
    VehiclePass,
    VehiclePassWithCamera,
    VehiclePassWithSpeed,
)

DATE_RE = re.compile(r"\b(\d{4})\.(\d{2})\.(\d{2})\b")
QUOTED_RE = re.compile(r'"([^"]*)"')
FLOAT_RE = re.compile(r"\b\d+\.\d+\b")


def _extract_date(line: str) -> date:
    clean = re.sub(r'"[^"]*"', " ", line)
    match = DATE_RE.search(clean)
    year, month, day = map(int, match.groups())
    return date(year, month, day)


def _extract_quoted(line: str) -> List[str]:
    return QUOTED_RE.findall(line)


def _extract_floats(line: str) -> List[float]:
    return [float(x) for x in FLOAT_RE.findall(line)]


def parse_line(line: str) -> Optional[VehiclePass]:
    line = line.strip()
    if not line:
        return None

    kind = line.split()[0].lower()
    record_date = _extract_date(line)
    quoted = _extract_quoted(line)
    floats = _extract_floats(line)

    if kind == "скорость":
        return VehiclePassWithSpeed(record_date, quoted[0], floats[0])
    if kind == "камера":
        return VehiclePassWithCamera(
            record_date, quoted[0], quoted[1], floats[0], floats[1]
        )
    return VehiclePass(record_date, quoted[0] if quoted else None)


def parse_text(text: str) -> List[VehiclePass]:
    result = []
    for raw in text.splitlines():
        obj = parse_line(raw)
        if obj is not None:
            result.append(obj)
    return result


def parse_file(path: str) -> List[VehiclePass]:
    with open(path, encoding="utf-8") as f:
        return parse_text(f.read())