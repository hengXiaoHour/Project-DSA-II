"""
Tree Layer — Categorization System
====================================
Builds a hierarchical tree of campus locations organised by category.
Allows users to browse locations by category and demonstrates tree traversal.
"""


class TreeNode:
    """
    A node in the categorization tree.

    Attributes:
        name (str): The display name for this node.
        children (list[TreeNode]): Child nodes.
        is_building (bool): True if this node represents an actual building
                            (leaf), False if it is a category branch.
    """

    def __init__(self, name, is_building=False):
        self.name = name
        self.children = []
        self.is_building = is_building

    def add_child(self, child_node):
        """Add a child node to this node."""
        self.children.append(child_node)

    def __repr__(self):
        return f"TreeNode({self.name}, {len(self.children)} children)"


class CategoryTree:
    """
    A tree that organises campus buildings into hierarchical categories.

    Tree structure:
        RUPP Campus
        ├── Academic Buildings (branch)
        │   ├── Building A  (leaf)
        │   ├── Building B
        │   ...

    Traversal methods:
        - Pre-order:   root → left → right (used for display)
        - Post-order:  left → right → root
        - Level-order: breadth-first level by level
    """

    def __init__(self):
        """Build the campus category tree."""
        self.root = TreeNode("RUPP Campus")
        self._build_tree()

    def _build_tree(self):
        """Construct the category hierarchy."""
        # --- Academic Buildings ---
        academic = TreeNode("Academic Buildings")
        for name in ["Building A", "Building B", "Building C",
                      "Building D", "Building Stem", "Building T", "CKCC"]:
            academic.add_child(TreeNode(name, is_building=True))
        self.root.add_child(academic)

        # --- Services ---
        services = TreeNode("Services")
        for name in ["Library", "NICC", "Canteen"]:
            services.add_child(TreeNode(name, is_building=True))
        self.root.add_child(services)

        # --- Administration ---
        admin = TreeNode("Administration")
        admin.add_child(TreeNode("Study Office", is_building=True))
        self.root.add_child(admin)


    # ----- Tree Traversals -----

    def _compute_display(self):
        display = {self.root.name: self.root.name}
        def walk(node, prefix="", is_last=False):
            connector = "└── " if is_last else "├── "
            display[node.name] = f"{prefix}{connector}{node.name}"
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                walk(child, child_prefix, i == len(node.children) - 1)
        for i, child in enumerate(self.root.children):
            walk(child, "", i == len(self.root.children) - 1)
        return display

    def _collect(self, node, order, result):
        if order == "pre":
            result.append(self._display[node.name])
        for child in node.children:
            self._collect(child, order, result)
        if order == "post":
            result.append(self._display[node.name])

    def pre_order(self):
        """
        Pre-order traversal: root → children (left to right).

        Uses box-drawing characters for a clean tree hierarchy.
        Time complexity: O(n).
        """
        self._display = self._compute_display()
        result = []
        self._collect(self.root, "pre", result)
        return result

    def post_order(self):
        """
        Post-order traversal: children → root.

        Uses box-drawing characters. Time complexity: O(n).
        """
        self._display = self._compute_display()
        result = []
        self._collect(self.root, "post", result)
        return result

    def level_order(self):
        """
        Level-order (breadth-first) traversal using a queue.

        Uses box-drawing characters. Time complexity: O(n).
        """
        self._display = self._compute_display()
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(self._display[node.name])
            for child in node.children:
                queue.append(child)
        return result

    # ----- User-facing Methods -----

    def display_tree(self):
        """Print the full category tree (pre-order traversal)."""
        print("\n=== CAMPUS CATEGORY TREE ===\n")
        lines = self.pre_order()
        for line in lines:
            print(f"  {line}")
        print()

    def get_categories(self):
        """Return a list of top-level category names (exclude root)."""
        return [child.name for child in self.root.children]

    def get_buildings_in_category(self, category_name):
        """
        Retrieve all building names under a given category.

        Args:
            category_name (str): Name of the category.

        Returns:
            list[str]: Building names, or empty list if category not found.
        """
        for child in self.root.children:
            if child.name.lower() == category_name.lower():
                return [grandchild.name for grandchild in child.children]
        return []

    def browse_by_category(self):
        """
        Interactive category browser.
        Displays categories and lets the user pick one to see its buildings.
        """
        categories = self.get_categories()
        print("\n--- Available Categories ---")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")

        try:
            choice = int(input("\nSelect a category number: "))
            if 1 <= choice <= len(categories):
                selected = categories[choice - 1]
                buildings = self.get_buildings_in_category(selected)
                print(f"\n  [{selected}]")
                for b in buildings:
                    print(f"    - {b}")
                print()
            else:
                print("  Invalid category number.\n")
        except ValueError:
            print("  Please enter a valid number.\n")

    def explain_traversal(self):
        """Print an explanation of the tree traversals used."""
        print("""
=== TREE TRAVERSAL EXPLANATION ===

This project uses a multi-way tree where:
- The root node is "RUPP Campus"
- Internal nodes are categories (branches)
- Leaf nodes are individual buildings

Traversals implemented:

1. PRE-ORDER (Root → Children)
   Used for displaying the tree.
   Process: Visit the current node, then recursively visit each child.
   Output order: RUPP Campus → Academic Buildings → Building A ...

2. POST-ORDER (Children → Root)
   Children are visited before their parent.
   Output order: Building A ... → Academic Buildings → RUPP Campus

3. LEVEL-ORDER (Breadth-First)
   Nodes are visited level by level using a queue.
   Root first, then all nodes at depth 1, then depth 2, etc.

Time Complexity: O(n) for all traversals, where n = number of nodes.
Space Complexity: O(h) for pre/post-order (recursion stack)
                  O(w) for level-order (queue width)
""")


# ----- Demonstration when run directly -----
if __name__ == "__main__":
    tree = CategoryTree()
    tree.display_tree()

    print("\n--- Pre-order ---")
    for line in tree.pre_order():
        print("  " + line)

    print("\n--- Post-order ---")
    for line in tree.post_order():
        print("  " + line)

    print("\n--- Level-order ---")
    for line in tree.level_order():
        print("  " + line)

    print("\n--- Buildings in 'Academic Buildings' ---")
    print(tree.get_buildings_in_category("Academic Buildings"))

    tree.explain_traversal()
