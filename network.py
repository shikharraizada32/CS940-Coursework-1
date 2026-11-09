from __future__ import annotations
from typing import Any

from exceptions import NetworkError
from station import Station
from line import Line
from prediction import Prediction
from heap import Heap
from trie import Trie

class Network:
    def __init__(self) -> None:
        """Initializes an empty Tube network."""
        # Core entity storage
        self.lines: dict[str, Line] = {}
        self.stations: dict[str, Station] = {}
        
        # Trie for prefix searching stations
        self.trie = Trie()
        
        # Multiple Heaps to organize predictions for O(1) query routing 
        # and O(k log k) retrieval via ksmallest
        self._station_heaps: dict[str, Heap] = {}
        self._line_heaps: dict[str, Heap] = {}
        self._station_line_heaps: dict[tuple[str, str], Heap] = {}
        self._train_heaps: dict[tuple[str, str], Heap] = {}

    def add_line(self, line: Line) -> None:
        """Adds a Line object to the network."""
        self.lines[line.line_id] = line

    def get_line(self, line_id: str) -> Line:
        """Retrieves a Line object by its ID."""
        if line_id not in self.lines:
            raise NetworkError(f"Line '{line_id}' does not exist in the network.")
        return self.lines[line_id]

    def add_station(self, station: Station) -> None:
        """Adds a Station object to the network and indexes its name in the Trie."""
        self.stations[station.station_id] = station
        # Index in lowercase for robust, case-insensitive searching
        self.trie.insert(station.station_name.lower(), station)

    def get_station(self, station_id: str) -> Station:
        """Retrieves a Station object by its ID."""
        if station_id not in self.stations:
            raise NetworkError(f"Station '{station_id}' does not exist in the network.")
        return self.stations[station_id]

    def add_prediction(self, prediction: Prediction) -> None:
        """
        Pushes a prediction into the appropriate heaps. 
        Because Prediction has a custom __lt__ method, it acts as its own sorting key!
        """
        s_id = prediction.naptan_id
        l_id = prediction.line_id
        v_id = prediction.vehicle_id
        
        # Station Heap
        if s_id not in self._station_heaps:
            self._station_heaps[s_id] = Heap()
        self._station_heaps[s_id].push(prediction, prediction)

        # Line Heap
        if l_id not in self._line_heaps:
            self._line_heaps[l_id] = Heap()
        self._line_heaps[l_id].push(prediction, prediction)

        # Station + Line Heap
        if (s_id, l_id) not in self._station_line_heaps:
            self._station_line_heaps[(s_id, l_id)] = Heap()
        self._station_line_heaps[(s_id, l_id)].push(prediction, prediction)

        # Train Heap
        if (v_id, l_id) not in self._train_heaps:
            self._train_heaps[(v_id, l_id)] = Heap()
        self._train_heaps[(v_id, l_id)].push(prediction, prediction)

    def search_by_prefix(self, prefix: str) -> list[Station]:
        """Returns a list of stations matching the prefix."""
        return self.trie.search_by_prefix(prefix.lower())

    def next_arrivals_by_station(self, station_id: str, k: int) -> list[Prediction]:
        if station_id not in self._station_heaps:
            return []
        return self._station_heaps[station_id].ksmallest(k)

    def next_arrivals_by_line(self, line_id: str, k: int) -> list[Prediction]:
        if line_id not in self._line_heaps:
            return []
        return self._line_heaps[line_id].ksmallest(k)

    def next_arrivals_by_station_and_line(self, station_id: str, line_id: str, k: int) -> list[Prediction]:
        if (station_id, line_id) not in self._station_line_heaps:
            return []
        return self._station_line_heaps[(station_id, line_id)].ksmallest(k)

    def next_stations_by_train(self, vehicle_id: str, line_id: str, k: int) -> list[Prediction]:
        if (vehicle_id, line_id) not in self._train_heaps:
            return []
        return self._train_heaps[(vehicle_id, line_id)].ksmallest(k)

    def __repr__(self) -> str:
        return f"Network(lines={len(self.lines)}, stations={len(self.stations)})"