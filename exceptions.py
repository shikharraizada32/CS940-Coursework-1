class TubeError(Exception):
    """Base exception for all tube-related errors."""
    pass

class DataStructureError(Exception):
    """Base exception for operations failing within our data structures."""
    pass

class DuplicateBranchError(TubeError):
    pass

class MissingBranchError(TubeError):
    pass

class NegativeTimeError(TubeError):
    pass

class HeapError(DataStructureError):
    pass

class TrieError(DataStructureError):
    pass