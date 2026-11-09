from __future__ import annotations

class Branch:
    """Represents a sequence of stations forming a branch on a Tube line."""

    def __init__(
            self,
            branch_id: int,
            next_branch_ids: list[int]
    ) -> None:
        self.branch_id = branch_id
        # Keep track of where this branch connects to next
        self.next_branch_ids = next_branch_ids
        self.stations: list[str] = []

    def add_station(
            self,
            station: str
    )-> None:
        self.stations.append(station)

    def station_edges(self) -> list[tuple[str,str]]:
        # Zip pairs up adjacent stations to create directed edges for the graph
        return list(zip(self.stations[:-1], self.stations[1:]))

    def branch_edges(self) -> list[tuple[int,int]]:
        # Connects this branch to all its subsequent branches
        return [(self.branch_id, next_id) for next_id in self.next_branch_ids]

    def __iter__(self):
        return iter(self.stations)

    def __len__(self) -> int:
        return len(self.stations)

    def __contains__(
            self,
            station: str
    ) -> bool:
        return station in self.stations

    def __getitem__(
            self,
            index
    ):
        return self.stations[index]

    def __repr__(self) -> str:
        return f"Branch(branch_id={self.branch_id}, next_branch_ids={self.next_branch_ids}, stations={len(self.stations)})"