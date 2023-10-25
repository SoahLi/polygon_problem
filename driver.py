from map import Map
from Piece import Piece
from tree import TreeNode
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, LineString
from Graph import Graph
import csv
import json
from random import random


class Driver:
    def __init__(self):

        self.map_pieces = None
        self.map = None
        self.graph = None
        self.root = None


    def load_map(self):
        with open("map.json") as file:
            content = file.read()
            data_dict = json.loads(content)
        #create map with map data
        if(data_dict["directions"] and data_dict["line_lengths"]):
            return self.map_creator(data_dict["directions"], data_dict["line_lengths"])

        else:
            raise IndexError("missing map inputs")

    def load_pieces(self):
        pieces = []
        with open("pieces.csv", 'r') as file:
            csvreader = csv.reader(file)
            next(csvreader) #skip the header
            for row in csvreader:
                pieces.append(Piece(int(row[0]), int(row[1])))
        if(pieces):
            return pieces
        else:
            raise IndexError("no pieces in file")
        
    def map_creator(self, directions: list[str], line_lengths: list[str]):
        """
        Create a Map() object based off of a list of directions and line_lengths
        """
        if not line_lengths and not directions:
            return
        if len(line_lengths) != len(directions):
            IndexExror: print("amount of lines and their dircetions do not match")
            return
        def create_coordinates(directions, line_lengths):
            num_lines = len(line_lengths)
            x_coordinates = [0]
            y_coordinates = [0]
            for i in range(num_lines):
                if directions[i] == "n":
                    x_coordinates.append(x_coordinates[-1] + 0)
                    y_coordinates.append(y_coordinates[-1] + line_lengths[i])
                elif directions[i] == "e":
                    x_coordinates.append(x_coordinates[-1] + line_lengths[i])
                    y_coordinates.append(y_coordinates[-1] + 0)                 
                elif directions[i] == "s":
                    x_coordinates.append(x_coordinates[-1] + 0)
                    y_coordinates.append(y_coordinates[-1] - line_lengths[i])
                    if y_coordinates[-1] < 0:
                        y_coordinates = self.shift_graph(y_coordinates, -y_coordinates[-1])
                elif directions[i] == "w":
                    x_coordinates.append(x_coordinates[-1] - line_lengths[i])
                    y_coordinates.append(y_coordinates[-1] + 0)
                    if x_coordinates[-1] < 0:
                        x_coordinates = self.shift_graph(x_coordinates, -x_coordinates[-1])
            #x_coordinates, y_coordinates = shift_graph(x_coordinates, 2), shift_graph(y_coordinates, 2)
            
            return [(x, y) for x, y in zip(x_coordinates, y_coordinates)]
        the_map = Map(create_coordinates(directions, line_lengths))
        return the_map

    def file_formater(self):
        with open("tree_data.json") as file:
            content = file.read()
            data_dict = json.loads(content)
        def dfs(node: dict):
            count = 1  # Initialize count to 1 for the current node
            if "branches" in node:
                for branch in node["branches"]:
                    count += dfs(branch)  # Recursively traverse branch nodes
            return count
        
        count = dfs(data_dict)
        
        count = dfs(data_dict)

        return {"highest_node": count, "tree": data_dict}


    def write_data(self):
        tree_dict = self.root.tree_to_dict(self.root)
        with open("tree_data.json", "w") as file:
            json.dump(tree_dict, file)



    # def display_map(idx = 1):
    #     with open('tree_data.json', 'r') as file:
    #         my_file = json.load(file)
    #         print((my_file["data"]))
        

    # def print_node_information(self.root: TreeNode):
    #     my_nodes = self.root.nodes_in_order()
    #     for i in range(1, self.root.count_nodes()+1):
    #         print(i)
    #         print(my_nodes[i-1])
    #         print()

    def color_generator(self):
        return ((random(), random(), random()))

    #need to change this so it works without idx
    def node_information_at_highest_index(self):
        def get_data_at_index(target_index):
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
        data = self.file_formater()
        d = get_data_at_index(data["highest_node"])
        my_graph = Graph([Piece(x,y) for x,y in d['pieces_len_height']], Map(d['map_coordinates']), [Piece.Orientation(coord, self.color_generator()) for coord in d['pieces_placed_coordinates']], d['try_point']) 
        my_graph.display_graph()


    def solve_puzzle(self):
        """
        main function for computing answer
        """
        self.map_pieces = self.load_pieces()
        self.map = self.load_map()
        self.graph = Graph(pieces = self.map_pieces, map = self.map)
        self.root = TreeNode(self.graph)
        self.graph.plot_map()

        branches = self.root.data.solve()
        branches = list(filter(lambda branch: branch is not None, branches))
        self.root.add_branches(branches)
        leaf_count = 0
        while True:
            leaves = self.root.get_leaves()
            for leaf in leaves:
                branches = leaf.data.solve()
                leaf.add_branches(branches)
                if(branches != None): leaf_count += len(branches)
            if(leaf_count == 0): break
            leaf_count = 0
        print("data written")
        self.write_data()


    #node_information_at_index(697)




    # def random_map(width, height):
    #     fig, ax = plt.subplots()
    #     directions = []
    #     line_lengths = []
    #     cardinal_directions = ['n', 'e', 's', 'w']
    #     width_until_edge = width
    #     height_until_height = height
    #     current_coord = [0,0]
    #     current_line = 0
    #     current_direction = ""
    #     current_GeoSeries_line = None
    #     all_GeoSeries_lines = []
    #     while sum(line_lengths) < width:
    #         current_line = randint(1,int(width/2))
    #         current_direction = cardinal_directions[randint(0, 3)]
    #         if current_direction == "n":
    #             if current_coord[1] + current_line > height: break #continue
    #             current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0], current_coord[1] + current_line]])).plot(ax = ax)
    #             current_coord[1] += current_line
    #         if current_direction == "s":
    #             if current_coord[1] - current_line < 0: break #continue
    #             current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0], current_coord[1] - current_line]])).plot(ax = ax)
    #             current_coord[1] -= current_line
    #         if current_direction == "e":
    #             if current_coord[0] + current_line > width: break #continue
    #             current_GeoSeries_line = gpd.GeoSeries(LineString([current_coord, [current_coord[0] + current_line, current_coord[1]]])).plot(ax = ax)
    #             current_coord[0] += current_line
    #         if current_direction == "w":
    #             current_GeoSeries_lin/Users/owenturnbull/Documents/cs_projects/polygon_problem/map.jsone = gpd.GeoSeries(LineString([current_coord, [current_coord[0] - current_line, current_coord[1]]])).plot(ax = ax)
    #             if current_coord[0] - current_line < 0: break #continue
    #             current_coord[0] -= current_line
    #         for line in all_GeoSeries_lines:
    #             if current_GeoSeries_line.intersects(line).bool():
    #                 ax.collections[-1].remove()
    #                 continue
    #         all_GeoSeries_lines.append(current_GeoSeries_line)
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


