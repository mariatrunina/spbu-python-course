import random
from collections.abc import MutableMapping
from typing import Optional, Iterator, Any


class Node:
    """A Node in the Cartesian Tree.

    Attributes:
        key (Any): The key of the node.
        value (Any): The value associated with the key.
        priority (float): The priority of the node, randomly assigned for balancing.
        left (Optional[Node]): The left child of the node.
        right (Optional[Node]): The right child of the node.
    """

    def __init__(self, key: Any, value: Any) -> None:
        """Initialize a Node with a key and a value.

        Args:
            key (Any): The key for this node.
            value (Any): The value associated with the key of this node.
        """
        self.key = key
        self.value = value
        self.priority = random.random()  # Random priority for balancing
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class CartesianTree(MutableMapping):
    """A MutableMapping implementation using a Cartesian Tree.

    This class supports the standard mapping operations: __getitem__,
    __setitem__, __delitem__, __iter__, __contains__, and __len__.
    """

    def __init__(self) -> None:
        """Initialize an empty Cartesian Tree."""
        self.root: Optional[Node] = None

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set the value for a key in the tree.

        If the key already exists, update its value. Otherwise, insert a new key-value pair.

        Args:
            key (Any): The key to insert or update.
            value (Any): The value to associate with the key.
        """
        self.root = self._insert(self.root, key, value)

    def _insert(self, node: Optional[Node], key: Any, value: Any) -> Node:
        """Insert a key-value pair into the subtree rooted at the specified node.

        Args:
            node (Optional[Node]): The root of the subtree.
            key (Any): The key to insert or update.
            value (Any): The value to associate with the key.

        Returns:
            Node: The new root of the subtree after insertion.
        """
        if node is None:
            return Node(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
            if node.left and node.left.priority > node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
            if node.right and node.right.priority > node.priority:
                node = self._rotate_left(node)
        else:
            node.value = value  # Update existing key

        return node

    def _rotate_right(self, node: Node) -> Node:
        """Perform a right rotation on the specified node.

        Args:
            node (Node): The node to rotate right.

        Returns:
            Node: The new root of the rotated subtree.
        """
        new_root = node.left
        if new_root is None:  # Safety check
            return node  # No rotation possible
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_left(self, node: Node) -> Node:
        """Perform a left rotation on the specified node.

        Args:
            node (Node): The node to rotate left.

        Returns:
            Node: The new root of the rotated subtree.
        """
        new_root = node.right
        if new_root is None:  # Safety check
            return node  # No rotation possible
        node.right = new_root.left
        new_root.left = node
        return new_root

    def __getitem__(self, key: Any) -> Any:
        """Get the value associated with a key in the tree.

        Args:
            key (Any): The key to retrieve.

        Returns:
            Any: The value associated with the key.

        Raises:
            KeyError: If the key is not found in the tree.
        """
        value = self._find(self.root, key)
        if value is None:
            raise KeyError(f"Key {key} not found.")
        return value

    def _find(self, node: Optional[Node], key: Any) -> Optional[Any]:
        """Find the value associated with a key in the subtree rooted at the specified node.

        Args:
            node (Optional[Node]): The root of the subtree.
            key (Any): The key to find.

        Returns:
            Optional[Any]: The value associated with the key or None if not found.
        """
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def __delitem__(self, key: Any) -> None:
        """Delete the key-value pair associated with the key in the tree.

        Args:
            key (Any): The key to delete.

        Raises:
            KeyError: If the key is not found in the tree.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[Node], key: Any) -> Optional[Node]:
        """Delete a key-value pair from the subtree rooted at the specified node.

        Args:
            node (Optional[Node]): The root of the subtree.
            key (Any): The key to delete.

        Returns:
            Optional[Node]: The new root of the subtree after deletion.

        Raises:
            KeyError: If the key is not found to delete.
        """
        if node is None:
            raise KeyError(f"Key {key} not found to delete.")

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            if node.left.priority > node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete(node.left, key)

        return node

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator for the keys of the tree in sorted order.

        Yields:
            Iterator[Any]: An iterator for the keys in sorted order.
        """
        yield from self._in_order(self.root)

    def _in_order(self, node: Optional[Node]) -> Iterator[Any]:
        """Perform an in-order traversal of the subtree rooted at the specified node.

        Args:
            node (Optional[Node]): The root of the subtree.

        Yields:
            Iterator[Any]: The keys of the nodes in in-order.
        """
        if node is not None:
            yield from self._in_order(node.left)
            yield node.key
            yield from self._in_order(node.right)

    def __len__(self) -> int:
        """Return the number of key-value pairs in the tree.

        Returns:
            int: The number of elements in the tree.
        """
        return self._count_nodes(self.root)

    def _count_nodes(self, node: Optional[Node]) -> int:
        """Count the number of nodes in the subtree rooted at the specified node.

        Args:
            node (Optional[Node]): The root of the subtree.

        Returns:
            int: The number of nodes in the subtree.
        """
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def __contains__(self, key: Any) -> bool:
        """Check if a key exists in the tree.

        Args:
            key (Any): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self._find(self.root, key) is not None

    def __repr__(self) -> str:
        """Return a string representation of the Cartesian Tree.

        Returns:
            str: A string representation of the Cartesian Tree.
        """
        return f"CartesianTree({list(self)})"
