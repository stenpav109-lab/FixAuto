from datetime import date


class VehiclePass:

    def __init__(self, record_date: date, plate_number: str) -> None:
        self.record_date = record_date
        self.plate_number = plate_number

    def __str__(self) -> str:
        return (f"Фиксация проезда: дата = "
                f"{self.record_date:%Y.%m.%d}, "
                f"номер = {self.plate_number}")


class VehiclePassWithSpeed(VehiclePass):

    def __init__(self, record_date: date, plate_number: str,
                 speed_kmh: float) -> None:
        super().__init__(record_date, plate_number)
        self.speed_kmh = speed_kmh

    def __str__(self) -> str:
        return f"{super().__str__()}, скорость = {self.speed_kmh} км/ч"


class VehiclePassWithCamera(VehiclePass):

    def __init__(self, record_date: date, plate_number: str,
                 camera_id: str, latitude: float,
                 longitude: float) -> None:
        super().__init__(record_date, plate_number)
        self.camera_id = camera_id
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self) -> str:
        return (f"{super().__str__()}, камера = {self.camera_id}, "
                f"координаты = ({self.latitude}, {self.longitude})")