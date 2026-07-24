from src.navigation.tree import TreeNode, Tree


class TestTree:
    def test_tree_node_add_child(self):
        root = TreeNode("Root")
        child = TreeNode("Child")
        root.add_child(child)
        assert child.parent == root
        assert child in root.children

    def test_get_path(self):
        root = TreeNode("Campus")
        b1 = TreeNode("B1")
        f1 = TreeNode("F1")
        r = TreeNode("R101")
        root.add_child(b1)
        b1.add_child(f1)
        f1.add_child(r)
        assert r.get_path() == ["Campus", "B1", "F1", "R101"]

    def test_find(self):
        root = TreeNode("Root")
        child = TreeNode("Target")
        root.add_child(child)
        tree = Tree(root)
        assert tree.find("Target") == child
        assert tree.find("Nope") is None

    def test_get_level(self):
        root = TreeNode("Root")
        c1 = TreeNode("C1")
        c2 = TreeNode("C2")
        root.add_child(c1)
        c1.add_child(c2)
        assert root.get_level() == 0
        assert c1.get_level() == 1
        assert c2.get_level() == 2

    def test_is_leaf(self):
        root = TreeNode("Root")
        leaf = TreeNode("Leaf")
        root.add_child(leaf)
        assert leaf.is_leaf() is True
        assert root.is_leaf() is False

    def test_get_all_nodes(self):
        root = TreeNode("Root")
        c1 = TreeNode("C1")
        c2 = TreeNode("C2")
        root.add_child(c1)
        root.add_child(c2)
        tree = Tree(root)
        assert len(tree.get_all_nodes()) == 3
