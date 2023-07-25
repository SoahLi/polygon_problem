class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child_node):
        if isinstance(child_node, TreeNode):
            self.children.append(child_node)
        else:
            raise TypeError("Child node must be of type TreeNode")

    def remove_child(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)
        else:
            raise ValueError("Child node not found in the children list")

    def __repr__(self, level=0):
        # For better visualization when printing the tree
        ret = "\t" * level + repr(self.data) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def __str__(self, level=0):
        # For better visualization when printing the tree
        ret = "\t" * level + str(self.data) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret
        
    def get_leaves(self):
        leaves = []
        def dfs(node):
            if not node.children:
                leaves.append(node)
            else:
                for child in node.children:
                    dfs(child)
        dfs(self)
        return leaves
    def add_children(self, data_list):
        if data_list == None:
            return
        for data in data_list:
            new_child = TreeNode(data)
            self.add_child(new_child)






