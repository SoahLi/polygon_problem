from map import Map
from piece import Piece
from tree import TreeNode
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, LineString
from graph import Graph
import csv
import json
from random import randint


#test_tree()

def file_formater():
    with open("tree_data.json") as file:
        content = file.read()
        data_dict = json.loads(content)
    def dfs(node: dict):
        count = 1  # Initialize count to 1 for the current node
        if "children" in node:
            for child in node["children"]:
                count += dfs(child)  # Recursively traverse child nodes
        return count
    
    count = dfs(data_dict)
    
    count = dfs(data_dict)
    print("this is the count")
    print(count)
    return {"highest_node": count, "tree": data_dict}


def write_data(root: TreeNode):
    tree_dict = root.tree_to_dict(root)
    with open("tree_data.json", "w") as file:
        json.dump(tree_dict, file)



def display_map(idx = 1):
    with open('tree_data.json', 'r') as file:
        my_file = json.load(file)
        print((my_file["data"]))
    

def print_node_information(root: TreeNode):
    my_nodes = root.nodes_in_order()
    for i in range(1, root.count_nodes()+1):
        print(i)
        print(my_nodes[i-1])
        print()


def node_information_at_index(idx: int = None):
    def get_data_at_index(target_index):
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
    colors = ['orange', 'yellow', 'pink', 'green', "magenta", 'cyan']
    data = file_formater()
    d = get_data_at_index(data["highest_node"])
    my_graph = Graph([Piece(x,y) for x,y in d['pieces_len_height']], Map(d['map_coordinates']), [Piece.Orientation(coord, colors[randint(0, len(colors)-1)]) for coord in d['pieces_placed_coordinates']], d['try_point']) 
    my_graph.display_graph()


def test_tree(iterations = 0):
    """
    main function for computing answer
    """
    #read in pieces & create Piece()
    my_pieces = []
    with open("pieces.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader) #skip the header
        for row in csvreader:
            my_pieces.append(Piece(int(row[0]), int(row[1])))
    my_graph = Graph(my_pieces) #root graph
    #print piece descriptions
    for piece in my_graph.pieces:  print("piece with width " + str(piece.width) + " and height " + str(piece.height) + " is color " + piece.color)
    root = TreeNode(my_graph)
    #get map data
    with open("map.json") as file:
        content = file.read()
        data_dict = json.loads(content)
    #create map with map data
    my_graph.map_creator(data_dict["directions"], data_dict["line_lengths"])

    my_graph.plot_map()

    #since I don't know the amount of iterations it will take, I need to define the number of iterations and manually iterate
    #This can be easily fixed
    root.add_children(root.data.solve())
    for i in range(iterations):
        for leaf in root.get_leaves():
            leaf.add_children(leaf.data.solve())
    write_data(root)
    my_graph.display_graph()



def random_map(width, height):
    fig, ax = plt.subplots()
    directions = []
    line_lengths = []
    cardinal_directions = ['n', 'e', 's', 'w']
    width_until_edge = width
    height_until_height = height
    current_coord = [0,0]
    current_line = 0
    current_direction = ""
    current_GeoSeries_line = None
    all_GeoSeries_lines = []
    while sum(line_lengths) < width:
        current_line = randint(1,int(width/2))
        current_direction = cardinal_directions[randint(0, 3)]
        if current_direction == "n":
            if current_coord[1] + current_line > height: break #continue
            current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0], current_coord[1] + current_line]])).plot(ax = ax)
            current_coord[1] += current_line
        if current_direction == "s":
            if current_coord[1] - current_line < 0: break #continue
            current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0], current_coord[1] - current_line]])).plot(ax = ax)
            current_coord[1] -= current_line
        if current_direction == "e":
            if current_coord[0] + current_line > width: break #continue
            current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0] + current_line, current_coord[1]]])).plot(ax = ax)
            current_coord[0] += current_line
        if current_direction == "w":
            current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0] - current_line, current_coord[1]]])).plot(ax = ax)
            if current_coord[0] - current_line < 0: break #continue
            current_coord[0] -= current_line
        for line in all_GeoSeries_lines:
            if current_GeoSeries_line.intersects(line).bool():
                ax.collections[-1].remove()
                continue
        all_GeoSeries_lines.append(current_GeoSeries_line)
    print("done")
    fig.show()

test_tree(4)


"""
"coordinates": ["e","n","e","n","w","s"],
"directions": [8,3,4,7,12,10]

Length, Width
2,5
6,3
10,2
5,6
5,6
"""


