from __future__ import annotations
import math
import re
from exceptions import TubeError

class Station:
    TUBE_LINES = {
        "bakerloo", "central", "circle", "district", "hammersmith-city",
        "jubilee", "metropolitan", "northern", "piccadilly", "victoria", "waterloo-city"
    }

    def __init__(
            self,
            station_id: str,
            station_name: str,
            interchange_lines: list,
            zones: str,
            lat: float,
            lon: float
    ) -> None:

        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise TubeError(f"Invalid geographic coordinates: lat={lat}, lon={lon}")

        self.station_id = station_id
        self.station_name = station_name
        self.lat = lat
        self.lon = lon

        self.zones = re.split(r'\s*[+/]\s*', zones) if zones else []

        self.interchange_lines = [
            line.get("id") for line in interchange_lines if isinstance(line, dict) and "id" in line 
        ]

    def is_interchange(self) -> bool:
        valid_tube_lines = [line_id for line_id in self.interchange_lines if line_id in self.TUBE_LINES]
        return len(set(valid_tube_lines)) > 1

    def distance_to(
            self, 
            other: Station
    ) -> float:
            R = 6371.0

            lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
            lat2, lon2 = math.radians(other.lat), math.radians(other.lon)

            diff_lat = lat2 - lat1
            diff_lon = lon2 - lon1

            a = math.sin(diff_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

            return R * c

    def __eq__(
            self,
            other: object
    ) -> bool:
            if not isinstance(other, Station):
                return False
            return self.station_id == other.station_id

    def __hash__(self) -> int:
        return hash(self.station_id)

    def __repr__(self) -> str:
        return f"Station(station_id='{self.station_id}', station_name='{self.station_name}')"

    def __str__(self) -> str:
        return f"{self.station_name} [{self.station_id}]"