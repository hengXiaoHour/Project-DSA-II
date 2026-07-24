class TreeNode:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_path(self):
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return list(reversed(path))

    def find(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.find(name)
            if result:
                return result
        return None

    def get_level(self):
        level = 0
        current = self
        while current.parent:
            level += 1
            current = current.parent
        return level

    def is_leaf(self):
        return len(self.children) == 0

    def __repr__(self, level=0):
        indent = "  " * level + ("└── " if level > 0 else "")
        result = f"{indent}{self.name}"
        for child in self.children:
            result += "\n" + child.__repr__(level + 1)
        return result


class Tree:
    def __init__(self, root=None):
        self.root = root

    def find(self, name):
        if self.root is None:
            return None
        return self.root.find(name)

    def get_all_nodes(self):
        nodes = []

        def dfs(node):
            nodes.append(node)
            for child in node.children:
                dfs(child)

        if self.root:
            dfs(self.root)
        return nodes

    def __repr__(self):
        if self.root is None:
            return "Tree(empty)"
        return repr(self.root)
