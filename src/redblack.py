import random

class RedBlackNode:
    def __init__(self, key):
        self.key = key
        self.value = set()  # Stores strings in a set
        self.color = "RED"  # Nodes are initially red
        self.parent = None
        self.left = None
        self.right = None


class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackNode(0)  # Sentinel node for leaves
        self.TNULL.color = "BLACK"
        self.root = self.TNULL

    def insert(self, key, string):
        # Insert a string into the tree, stored in the node's set
        new_node = RedBlackNode(key)
        new_node.left = self.TNULL
        new_node.right = self.TNULL

        parent = None
        current = self.root

        # Find the parent for the new node
        while current != self.TNULL:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:  # If the key already exists, add the string to the set and return
                current.value.add(string)
                return

        new_node.parent = parent

        if parent is None:  # Tree is empty
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.value.add(string)  # Add the string to the new node's set
        self.fix_insert(new_node)

    def fix_insert(self, node):
        while node.parent and node.parent.color == "RED":
            grandparent = node.parent.parent
            if node.parent == grandparent.left:
                uncle = grandparent.right
                if uncle.color == "RED":
                    # Case 1: Uncle is red
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    grandparent.color = "RED"
                    node = grandparent
                else:
                    if node == node.parent.right:
                        # Case 2: Node is right child
                        node = node.parent
                        self.left_rotate(node)
                    # Case 3: Node is left child
                    node.parent.color = "BLACK"
                    grandparent.color = "RED"
                    self.right_rotate(grandparent)
            else:
                uncle = grandparent.left
                if uncle.color == "RED":
                    # Case 1: Uncle is red
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    grandparent.color = "RED"
                    node = grandparent
                else:
                    if node == node.parent.left:
                        # Case 2: Node is left child
                        node = node.parent
                        self.right_rotate(node)
                    # Case 3: Node is right child
                    node.parent.color = "BLACK"
                    grandparent.color = "RED"
                    self.left_rotate(grandparent)

        self.root.color = "BLACK"

    def left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left != self.TNULL:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right != self.TNULL:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def search(self, key):
        current = self.root
        while current != self.TNULL and current.key != key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current.value if current != self.TNULL else None

    def print_helper(self, node, space, count=5):
        # Base case: if the node is TNULL (null leaf), return
        if node == self.TNULL:
            return

        # Increase distance between levels
        space += count

        # Print the right child first (recurse)
        self.print_helper(node.right, space)

        # Print the current node after padding with spaces
        print()
        for i in range(count, space):
            print(" ", end="")
        print(f"{node.key} ({node.color}) {node.value}")

        # Print the left child (recurse)
        self.print_helper(node.left, space)

    def print_tree(self):
        self.print_helper(self.root, 0)

    def get_random_song(self, key, song_list):
        """
        Searches for a random song in the tree starting from the specified key.
        If the key does not exist, it will search the next available key.
        """
        song_set = self.search(key)

        # If the key exists and has songs, choose one randomly
        if song_set:
            random_song = random.choice(list(song_set))  # Convert set to list for random.choice
            song_list.append(random_song)  # Add the song to the list
        else:
            # If the key does not exist and is within bounds, try the next key
            if key < 99:
                self.get_random_song(key + 1, song_list)  # Recursive call for the next key

    def create_playlist(self):
        random_songs = []  # List to store the random playlist

        # Define ranges for song selection
        ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50)]

        for r in ranges:
            num_range1 = random.randint(*r)
            num_range2 = random.randint(*r)
            num_range3 = random.randint(*r)
            num_range4 = random.randint(*r)

            # Fetch random songs from the tree
            self.get_random_song(num_range1, random_songs)
            self.get_random_song(num_range2, random_songs)
            self.get_random_song(num_range3, random_songs)
            self.get_random_song(num_range4, random_songs)

        # Print the final list of random songs
        return(random_songs)


# Example Usage
if __name__ == "__main__":
    rb_tree = RedBlackTree()

    rb_tree.insert(15, "cherry")
    rb_tree.insert(15, "date")
    rb_tree.insert(10, "apple")
    rb_tree.insert(10, "elderberry")
    rb_tree.insert(20, "banana")
    rb_tree.insert(30, "grape")
    rb_tree.insert(12, "fig")
    rb_tree.insert(40, "kiwi")


    rb_tree.print_tree()

    print("Search for key 10:", rb_tree.search(10))
    print("Search for key 50:", rb_tree.search(50))
