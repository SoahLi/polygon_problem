from map import Map
from piece import Piece
from tree import TreeNode
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
from graph import Graph
import csv
import json
"""
correct_node = None
correct_node_idx = 62
my_pieces = []
with open("pieces.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        my_pieces.append(Piece(int(row[0]), int(row[1])))
my_graph = Graph(my_pieces)
for piece in my_graph.pieces:
    print("piece with width " + str(piece.width) + " and height " + str(piece.height) + " is color " + piece.color)
root = TreeNode(my_graph)
my_graph.map_creator(['e','n','e','n','w','s'], [8,3,4,7,12,10])
my_graph.plot_map()
root.add_children(root.data.fill_perimater())
for i in range(4):
    for leaf in root.get_leaves():
        leaf.add_children(leaf.data.fill_perimater())
if root.count_nodes() >= correct_node_idx:
    correct_node = root.get_node_at_index(correct_node_idx)
tree_dict = root.tree_to_dict(root)
with open("tree_data.json", "w") as file:
    json.dump(tree_dict, file)
print(root.grab_data_at_index(5))
"""



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
    


"""
for node in correct_node.children:
    print("hi")
    print(node.index)
print(root.__repr__())

print(root.count_nodes())
print()
print(plt.get_fignums())
for i in range(1,correct_node_idx):
    plt.close(i)
print()
print(plt.get_fignums())
for i in range(15, root.count_nodes()+4):
    plt.close(i)
print()
"""
"""
print("the supposed correct node\n\n\n")
print(correct_node.data)
my_nodes = root.nodes_in_order()
for i in range(1, root.count_nodes()+1-90):
    print(i)
    print(my_nodes[i-1])
    print()

print("finished")
"""
"""
tree_dict = root.tree_to_dict(root)
with open("tree_data.json", "w") as file:
    json.dump(tree_dict, file)
"""

d = get_data_at_index(62)
my_graph = Graph([Piece(x,y) for x,y in d['pieces_len_height']], Map(d['map_coordinates']), [Piece.Orientation(coord, "pink") for coord in d['pieces_placed_coordinates']], d['try_point'])
print(my_graph.pieces[0].color)
my_graph.display_graph()
"""
"""





"""
#my_map.add_polygon([(0, 0), (5, 0), (5, 5), (0, 5)])™
#my_map.add_polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
#my_map.add_polygon([(5, 5), (7, 5), (7, 7), (5, 7)])
    

with open("pieces.csv", "r") as pieces:
    example = pieces.readline(1)
    print(example)

objects = my_map.polygons

fig, ax = plt.subplots()  # Create a figure and axis

def restart():
    ax.clear()
    
objects[0].plot(ax = ax, color="blue") 
objects[1].plot(ax = ax, color="red")

def update(frame):
    frame.plot(ax=ax, color = "red")  # Plot the GeoSeries on the specified axis

#ani = FuncAnimation(fig, update, frames=objects[1:], init_func = restart, repeat = True)
"""


#test = my_map.plot_map()
#test.plot()
#plt.show()



# my_polygon = (Polygon([(0, 0), (5,0), (5,5), (0,5)]))
# my_graph = gpd.GeoSeries(my_polygon)
# my_polygon2 =  (Polygon([(1, 1), (6,1), (6,6), (1,6)]))
# my_graph2 = gpd.GeoSeries(my_polygon2)
# res = pd.concat([my_graph, my_graph2])
# print(res.values)
# res.plot(color=['b'] + ['r' for _ in range(len(res.values) - 1)])
# plt.show()


# my_poly = gpd.GeoSeries([Polygon([(0, 0), (5,0), (5,5), (0,5)])])
# print("this is the poly")
# print(my_poly)


# poly1 = Polygon( [(0, 0), (5,0), (5,5), (0,5) ] )
# poly3 = Polygon([(0,0), (.5,0), (.5,.5),(0,.5)])
# myPoly = gpd.GeoSeries([poly1, poly3])
# print(poly3.intersects(poly1))
# myPoly.plot()
# plt.show()


#EXAMPLE CODE#

"""import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()"""
