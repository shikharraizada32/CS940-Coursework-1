from __future__ import annotations
from branch import Branch
from exceptions import DuplicateBranchError, MissingBranchError

class Line:
    def __init__(
            self,
            line_id: str,
            line_name: str
    )-> None:
        self.line_id = line_id
        self.line_name = line_name
        self.branches: dict[int, Branch] = {}

    def add_branch(
            self,
            branch: Branch
    )-> None:
        if branch.branch_id in self.branches:
            raise DuplicateBranchError(f"Branch ID {branch.branch_id} already exists on line {self.line_id}")
        self.branches[branch.branch_id] = branch

    def get_branch(
            self,
            id: int
    )-> Branch:
        if id not in self.branches:
            raise MissingBranchError(f"Branch ID {id} doesn't exit on the line {self.line_id}.")
        return self.branches[id]

    def get_stations(self)-> set[str]:
        station_set: set[str] = set()
        for branch in self.branches.values():
            for station_id in branch.stations:
                station_set.add(station_id)
        return station_set

    def __iter__(self):
        return iter(self.get_stations())

    def __len__(self):
        return len(self.get_stations())

    def __contains__(
                self,
                station: str
        ) -> bool:
            return station in self.get_stations()
    
    def __repr__(self) -> str:
            return f"Line(line_id={self.line_id}, line_name={self.line_name}, branches={len(self.branches)})"