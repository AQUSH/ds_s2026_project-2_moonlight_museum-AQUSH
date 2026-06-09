"""Project 2 starter code: Moonlight Museum After Dark.

Students should implement all required behavior in this file.
Use stdlib only.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass(frozen=True)
class Artifact:
    """A museum artifact stored in the archive BST."""

    artifact_id: int
    name: str
    category: str
    age: int
    room: str


@dataclass(frozen=True)
class RestorationRequest:
    """A request to inspect or repair an artifact."""

    artifact_id: int
    description: str


class TreeNode:
    """A node for the artifact BST."""

    def __init__(
        self,
        artifact: Artifact,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.artifact = artifact
        self.left = left
        self.right = right


class ArtifactBST:
    """Binary search tree keyed by artifact_id."""

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, artifact: Artifact) -> bool:
        """Insert an artifact.

        Return True if the artifact was inserted.
        Return False if an artifact with the same ID already exists.
        """
        inserted = [False]

        def _insert(node: TreeNode | None, artifact: Artifact) -> TreeNode:
            if node is None:
                inserted[0] = True
                return TreeNode(artifact)
            if artifact.artifact_id == node.artifact.artifact_id:
                return node  # duplicate — ignore
            if artifact.artifact_id < node.artifact.artifact_id:
                node.left = _insert(node.left, artifact)
            else:
                node.right = _insert(node.right, artifact)
            return node

        self.root = _insert(self.root, artifact)
        return inserted[0]

    def search_by_id(self, artifact_id: int) -> Artifact | None:
        """Return the matching artifact, or None if it does not exist."""
        current = self.root
        while current is not None:
            if artifact_id == current.artifact.artifact_id:
                return current.artifact
            elif artifact_id < current.artifact.artifact_id:
                current = current.left
            else:
                current = current.right
        return None

    def inorder_ids(self) -> list[int]:
        """Return a list of artifact IDs using inorder traversal."""
        result: list[int] = []

        def _inorder(node: TreeNode | None) -> None:
            if node is None:
                return
            _inorder(node.left)
            result.append(node.artifact.artifact_id)
            _inorder(node.right)

        _inorder(self.root)
        return result

    def preorder_ids(self) -> list[int]:
        """Return a list of artifact IDs using preorder traversal."""
        result: list[int] = []

        def _preorder(node: TreeNode | None) -> None:
            if node is None:
                return
            result.append(node.artifact.artifact_id)
            _preorder(node.left)
            _preorder(node.right)

        _preorder(self.root)
        return result

    def postorder_ids(self) -> list[int]:
        """Return a list of artifact IDs using postorder traversal."""
        result: list[int] = []

        def _postorder(node: TreeNode | None) -> None:
            if node is None:
                return
            _postorder(node.left)
            _postorder(node.right)
            result.append(node.artifact.artifact_id)

        _postorder(self.root)
        return result


class RestorationQueue:
    """FIFO queue of restoration requests."""

    def __init__(self) -> None:
        self._items: Deque[RestorationRequest] = deque()

    def add_request(self, request: RestorationRequest) -> None:
        """Add a request to the back of the queue."""
        self._items.append(request)

    def process_next_request(self) -> RestorationRequest | None:
        """Remove and return the next request, or None if the queue is empty."""
        if not self._items:
            return None
        return self._items.popleft()

    def peek_next_request(self) -> RestorationRequest | None:
        """Return the next request without removing it, or None if empty."""
        if not self._items:
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        """Return True if the queue has no requests."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of queued requests."""
        return len(self._items)


class ArchiveUndoStack:
    """LIFO stack of recent archive actions."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push_action(self, action: str) -> None:
        """Push an action onto the stack."""
        self._items.append(action)

    def undo_last_action(self) -> str | None:
        """Remove and return the most recent action, or None if empty."""
        if not self._items:
            return None
        return self._items.pop()

    def peek_last_action(self) -> str | None:
        """Return the most recent action without removing it, or None if empty."""
        if not self._items:
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no actions."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of stored actions."""
        return len(self._items)


class ExhibitNode:
    """A node in the singly linked exhibit route."""

    def __init__(self, stop_name: str, next_node: ExhibitNode | None = None) -> None:
        self.stop_name = stop_name
        self.next = next_node


class ExhibitRoute:
    """Singly linked list of exhibit stops."""

    def __init__(self) -> None:
        self.head: ExhibitNode | None = None

    def add_stop(self, stop_name: str) -> None:
        """Add a stop to the end of the route."""
        new_node = ExhibitNode(stop_name)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def remove_stop(self, stop_name: str) -> bool:
        """Remove the first matching stop.

        Return True if a stop was removed.
        Return False if the stop does not exist.
        """
        if self.head is None:
            return False
        # Remove head
        if self.head.stop_name == stop_name:
            self.head = self.head.next
            return True
        # Remove middle or tail
        current = self.head
        while current.next is not None:
            if current.next.stop_name == stop_name:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def list_stops(self) -> list[str]:
        """Return the route as a list of stop names in order."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.stop_name)
            current = current.next
        return result

    def count_stops(self) -> int:
        """Return the number of stops in the route."""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count


def count_artifacts_by_category(artifacts: list[Artifact]) -> dict[str, int]:
    """Return a dictionary counting artifacts in each category."""
    counts: dict[str, int] = {}
    for artifact in artifacts:
        counts[artifact.category] = counts.get(artifact.category, 0) + 1
    return counts


def unique_rooms(artifacts: list[Artifact]) -> set[str]:
    """Return a set of all rooms used by the given artifacts."""
    return {artifact.room for artifact in artifacts}


def sort_artifacts_by_age(
    artifacts: list[Artifact],
    descending: bool = False,
) -> list[Artifact]:
    """Return a new list of artifacts sorted by age.

    If descending is False, sort from youngest to oldest.
    If descending is True, sort from oldest to youngest.
    """
    return sorted(artifacts, key=lambda a: a.age, reverse=descending)


def linear_search_by_name(
    artifacts: list[Artifact],
    name: str,
) -> Artifact | None:
    """Return the first artifact with an exact matching name, or None."""
    for artifact in artifacts:
        if artifact.name == name:
            return artifact
    return None


def demo_museum_night() -> None:
    """Run a small integration demo showing the system working together."""
    print("=== Moonlight Museum After Dark ===")
    print()

    # 1. Create artifacts and insert into BST
    artifacts = [
        Artifact(40, "Cursed Mirror", "mirror", 220, "North Hall"),
        Artifact(20, "Clockwork Bird", "machine", 80, "Workshop"),
        Artifact(60, "Whispering Map", "paper", 140, "Archive"),
        Artifact(10, "Glowing Key", "metal", 35, "Vault"),
        Artifact(30, "Moon Dial", "device", 120, "North Hall"),
        Artifact(50, "Silver Mask", "costume", 160, "Gallery"),
        Artifact(70, "Lantern Jar", "glass", 60, "Gallery"),
        Artifact(25, "Ink Compass", "device", 120, "Archive"),
    ]

    bst = ArtifactBST()
    for artifact in artifacts:
        bst.insert(artifact)

    print("Inorder IDs:", bst.inorder_ids())
    print("Preorder IDs:", bst.preorder_ids())
    print("Postorder IDs:", bst.postorder_ids())
    print()

    # 2. Search
    found = bst.search_by_id(50)
    print(f"Search ID 50: {found.name if found else 'Not found'}")
    missing = bst.search_by_id(999)
    print(f"Search ID 999: {missing if missing else 'Not found'}")
    print()

    # 3. Restoration queue
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(40, "Polish cracked frame"))
    queue.add_request(RestorationRequest(20, "Oil the wing gears"))
    queue.add_request(RestorationRequest(60, "Flatten folded corner"))

    print("Next restoration request:", queue.peek_next_request().description)
    queue.process_next_request()
    print(f"After processing, queue size: {queue.size()}")
    print()

    # 4. Undo stack
    stack = ArchiveUndoStack()
    stack.push_action("Added Cursed Mirror to archive")
    stack.push_action("Queued Clockwork Bird repair")
    stack.push_action("Removed Secret Vault stop")

    print("Undo action:", stack.undo_last_action())
    print(f"After undo, stack size: {stack.size()}")
    print()

    # 5. Exhibit route
    route = ExhibitRoute()
    for stop in ["Entrance", "Mirror Room", "Clockwork Gallery", "Vault", "Exit"]:
        route.add_stop(stop)
    print("Exhibit route:", route.list_stops())
    route.remove_stop("Vault")
    print("After removing Vault:", route.list_stops())
    print()

    # 6. Reports
    print("Category counts:", count_artifacts_by_category(artifacts))
    print("Unique rooms:", unique_rooms(artifacts))
    print("Sorted by age (asc):", [a.name for a in sort_artifacts_by_age(artifacts)])
    found_by_name = linear_search_by_name(artifacts, "Whispering Map")
    print(f"Search by name 'Whispering Map': {found_by_name.name if found_by_name else 'Not found'}")