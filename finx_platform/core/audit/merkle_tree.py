"""Cryptographic Merkle Tree Engine for Immutable Bank Audit Trail Integrity."""

import hashlib
from typing import List, Optional


class MerkleTree:
    """Constructs a binary hash tree over platform audit log events for verifiable tamper resistance."""

    def __init__(self, leaf_hashes: List[str]):
        self.leaves = leaf_hashes
        self.tree: List[List[str]] = []
        if leaf_hashes:
            self._build_tree()

    def _hash_pair(self, left: str, right: str) -> str:
        return hashlib.sha256((left + right).encode("utf-8")).hexdigest()

    def _build_tree(self) -> None:
        current_layer = self.leaves[:]
        self.tree.append(current_layer)
        while len(current_layer) > 1:
            next_layer = []
            for i in range(0, len(current_layer), 2):
                left = current_layer[i]
                right = current_layer[i + 1] if i + 1 < len(current_layer) else left
                next_layer.append(self._hash_pair(left, right))
            self.tree.append(next_layer)
            current_layer = next_layer

    def get_root_hash(self) -> Optional[str]:
        if not self.tree or not self.tree[-1]:
            return None
        return self.tree[-1][0]

    def verify_inclusion(self, leaf_hash: str, proof: List[str], root_hash: str) -> bool:
        current = leaf_hash
        for p in proof:
            current = self._hash_pair(current, p)
        return current == root_hash
