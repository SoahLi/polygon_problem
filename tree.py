import json
import matplotlib.pyplot as plt

class TreeNode:
    total_nodes = 0
    def __init__(self, data):
        self.data = data
        self.branches = []
        TreeNode.total_nodes += 1  # Increment the total number of nodes
        self.index = TreeNode.total_nodes

    def __repr__(self, level=0):
        # For better visualization when printing the tree
        ret = "\t" * level + repr(self.index) + "\n"
        for branch in self.branches:
            ret += branch.__repr__(level + 1)
        return ret

    def __str__(self, level=0):
        # For better visualization when printing the tree
        ret = "\t" * level + str(self.data) + "\n"
        for branch in self.branches:
            ret += branch.__str__(level + 1)
        return ret

    def add_branch(self, branch_node):
        if isinstance(branch_node, TreeNode):
            self.branches.append(branch_node)
        else:
            raise TypeError("branch node must be of type TreeNode")

    def add_branches(self, data_list):
        if data_list == None:
            return
        for data in data_list:
            new_branch = TreeNode(data)
            self.add_branch(new_branch)

    def remove_branch(self, branch_node):
        if branch_node in self.branches:
            self.branches.remove(branch_node)
        else:
            raise ValueError("branch node not found in the branchren list")
    
    
    def get_leaves(self):
        leaves = []
        def dfs(node):
            if not node.branches:
                leaves.append(node)
            else:
                for branch in node.branches:
                    dfs(branch)
        dfs(self)
        return leaves
    
    def count_leaves(self):
        if not self.branches:
            return 1
        else:
            count = 0
            for branch in self.branches:
                count += branch.count_leaves()
            return count
        
    def get_node_at_index(self, target_index):
        def dfs(node):
            if node.index == target_index:
                return node
            for branch in node.branches:
                result = dfs(branch)
                if result:
                    return result
            return None
        return dfs(self)


    def nodes_in_order(self):
        queue = [self]  # Initialize the queue with the root node
        nodes_data = []

        while queue:
            current_node = queue.pop(0)  # Dequeue the first node in the queue
            nodes_data.append(current_node.data)

            # Enqueue all branchren of the current node
            for branch in current_node.branches:
                queue.append(branch)

        return nodes_data
    

    def tree_to_dict(self, node):
        data = {
            "index": str(node.index),
            "data": {
                "pieces_len_height": [[piece.width, piece.height] for piece in node.data.pieces],
                "map_coordinates": node.data.map.coordinates[:-1],
                "pieces_placed_coordinates": [orientation.coordinates for orientation in node.data.pieces_placed],
                "try_point": node.data.try_point,
            },
            "branches": [],
        }

        for branch in node.branches:
            branch_json = self.tree_to_dict(branch)
            data["branches"].append(branch_json)
            
        return data


    def grab_data_at_index_from_file(self, target_index):
        with open("tree_data.json", "r") as file:
            content = file.read()
            data_dict = json.loads(content)
        
        def dfs(node):
            if int(node['index']) == target_index:
                return node['data']
            for branch in node['branches']:
                result = dfs(branch)
                if result:
                    return result
            return None

        return dfs(data_dict)



