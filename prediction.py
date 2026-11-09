from __future__ import annotations
from exceptions import NegativeTimeError

class Prediction:
    """Represents a live arrival prediction for a specific train at a station."""

    def __init__(
            self,
            vehicle_id: str,
            naptan_id: str,
            line_id: str,
            platform_name: str,
            destination_id: str,
            time_to_station: int,
            current_location: str
    )-> None:
        # Catch bad TfL data at the source
        if time_to_station < 0:
            raise NegativeTimeError(f"Time to station can't be negative: {time_to_station}")

        self.vehicle_id = vehicle_id
        self.naptan_id = naptan_id
        self.line_id = line_id
        self.platform_name = platform_name
        self.destination_id = destination_id
        self.time_to_station = time_to_station
        self.current_location = current_location
    def __lt__(
            self,
            other: Prediction
    )-> bool:
        # tie-breaker: if times are equal, fall back to vehicle_id
        return (self.time_to_station, self.vehicle_id) < (other.time_to_station, other.vehicle_id)

    def __repr__(self)-> str:
        return (f"Prediction(vehicle_id='{self.vehicle_id}', naptan_id='{self.naptan_id}', "
                f"line_id='{self.line_id}', time_to_station={self.time_to_station})")