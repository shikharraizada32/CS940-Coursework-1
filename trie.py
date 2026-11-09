from __future__ import annotations
from typing import Any
from exceptions import TrieError

class _TrieNode:
    """A private internal node for the Trie."""
    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.objects: list[Any] = []

class Trie:
    def __init__(self) -> None:
        """Initializes an empty string-prefix Trie."""
        self.root = _TrieNode()
        self._all_objects: list[Any] = []
    
    def insert(self, key: str, obj: Any) -> None:
        """Associates obj with key and indexes each word of the key."""
        # Validate key type and content
        if not isinstance(key, str):
            raise TrieError(f"Key must be a string, got {type(key).__name__}")
        if not key.strip():
            raise TrieError("Key cannot be empty or just whitespace.")

        # Store object globally once per insert call
        self._all_objects.append(obj)
        
        words = key.split()
        
        # Index each word independently
        for word in words:
            current = self.root
            for char in word:
                if char not in current.children:
                    current.children[char] = _TrieNode()
                current = current.children[char]
            
            current.objects.append(obj)

    def search_by_prefix(self, prefix: str) -> list[Any]:
        """Returns all objects where a word in their key starts with the prefix.
        Runs in O(m + size of matching subtree)[cite: 16]."""
        if not isinstance(prefix, str):
            raise TrieError(f"Prefix must be a string, got {type(prefix).__name__}")

        # Empty prefix returns all stored objects
        if prefix == "":
            return self._all_objects

        current = self.root
        
        # Walk down the tree to the end of the prefix (O(m) time)[cite: 16]
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        # Traverse the subtree to collect results, using a dict for O(1) deduplication
        results_map: dict[int, Any] = {}

        def dfs(node: _TrieNode) -> None:
            for obj in node.objects:
                obj_id = id(obj)
                if obj_id not in results_map:
                    results_map[obj_id] = obj
            
            for child in node.children.values():
                dfs(child)

        dfs(current)
        
        return list(results_map.values())