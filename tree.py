import json
import jsbeautifier

class TreeNode:
    total_nodes = 0
    def __init__(self, data):
        self.data = data
        self.children = []
        TreeNode.total_nodes += 1  # Increment the total number of nodes
        self.index = TreeNode.total_nodes

    def __repr__(self, level=0):
        # For better visualization when printing the tree
        ret = "\t" * level + repr(self.index) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def __str__(self, level=0):
        # For better visualization when printing the tree
        ret = "\t" * level + str(self.data) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def add_child(self, child_node):
        if isinstance(child_node, TreeNode):
            self.children.append(child_node)
        else:
            raise TypeError("Child node must be of type TreeNode")

    def add_children(self, data_list):
        if data_list == None:
            return
        for data in data_list:
            new_child = TreeNode(data)
            self.add_child(new_child)

    def remove_child(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)
        else:
            raise ValueError("Child node not found in the children list")
    
    def count_nodes(self):
        count = 1  # Start with the current node itself
        for child in self.children:
            count += child.count_nodes()
        return count
    
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
    
    def count_leaves(self):
        if not self.children:
            return 1
        else:
            count = 0
            for child in self.children:
                count += child.count_leaves()
            return count
        
    def get_node_at_index(self, target_index):
        def dfs(node):
            if node.index == target_index:
                return node
            for child in node.children:
                result = dfs(child)
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

            # Enqueue all children of the current node
            for child in current_node.children:
                queue.append(child)

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
            "children": [],
        }

        for child_node in node.children:
            child_json = self.tree_to_dict(child_node)
            data["children"].append(child_json)
            
        return data
    
    def print_data(self, data):
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        formated = jsbeautifier.beautify(json.dumps(data), opts)

    def grab_data_at_index(self, target_index):
        with open("tree_data.json", "r") as file:
            content = file.read()
            data_dict = json.loads(content)
        
        def dfs(node):
            if int(node['index']) == target_index:
                return node['data']
            for child in node['children']:
                result = dfs(child)
                if result:
                    return result
            return None

        return dfs(data_dict)



