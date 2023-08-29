from map import Map
from piece import Piece
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString
from graph import Graph
import csv
from tree import TreeNode
import json
import ctypes
"""
root = TreeNode(1)
root.add_children([10,22,45,33])
print(root.__repr__())
print(root.get_node_at_index(1))
"""
"""
d = {'index': '1', 'data': {'pieces': [[2, 5], [6, 3], [10, 2], [5, 6], [5, 6]], 'map': [(0, 0), (8, 0), (8, 3), (12, 3), (12, 10), (0, 10)], 'pieces_placed': [], 'try_point': (0, 0)}, 'children': [{'index': '2', 'data': {'pieces': [[6, 3], [10, 2], [5, 6], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (2.0, 0.0), (2.0, 5.0), (0.0, 5.0)), 'pieces_placed': [[[0, 0], [2, 0], [2, 5], [0, 5]]], 'try_point': [0, 5]}, 'children': []}, {'index': '3', 'data': {'pieces': [[6, 3], [10, 2], [5, 6], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (5.0, 0.0), (5.0, 2.0), (0.0, 2.0)), 'pieces_placed': [([0, 0], [5, 0], [5, 2], [0, 2])], 'try_point': [0, 2]}, 'children': []}, {'index': '4', 'data': {'pieces': [[2, 5], [10, 2], [5, 6], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (6.0, 0.0), (6.0, 3.0), (0.0, 3.0)), 'pieces_placed': [[[0, 0], [6, 0], [6, 3], [0, 3]]], 'try_point': [0, 3]}, 'children': []}, {'index': '5', 'data': {'pieces': [[2, 5], [10, 2], [5, 6], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (3.0, 0.0), (3.0, 6.0), (0.0, 6.0)), 'pieces_placed': [([0, 0], [3, 0], [3, 6], [0, 6])], 'try_point': [0, 6]}, 'children': []}, {'index': '6', 'data': {'pieces': [[2, 5], [6, 3], [5, 6], [5, 6]], 'map': ((12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (2.0, 0.0), (2.0, 10.0)), 'pieces_placed': [([0, 0], [2, 0], [2, 10], [0, 10])], 'try_point': [2, 10]}, 'children': []}, {'index': '7', 'data': {'pieces': [[2, 5], [6, 3], [10, 2], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (5.0, 0.0), (5.0, 6.0), (0.0, 6.0)), 'pieces_placed': [[[0, 0], [5, 0], [5, 6], [0, 6]]], 'try_point': [0, 6]}, 'children': []}, {'index': '8', 'data': {'pieces': [[2, 5], [6, 3], [10, 2], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (6.0, 0.0), (6.0, 5.0), (0.0, 5.0)), 'pieces_placed': [([0, 0], [6, 0], [6, 5], [0, 5])], 'try_point': [0, 5]}, 'children': []}, {'index': '9', 'data': {'pieces': [[2, 5], [6, 3], [10, 2], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (5.0, 0.0), (5.0, 6.0), (0.0, 6.0)), 'pieces_placed': [[[0, 0], [5, 0], [5, 6], [0, 6]]], 'try_point': [0, 6]}, 'children': []}, {'index': '10', 'data': {'pieces': [[2, 5], [6, 3], [10, 2], [5, 6]], 'map': ((0.0, 10.0), (12.0, 10.0), (12.0, 3.0), (8.0, 3.0), (8.0, 0.0), (6.0, 0.0), (6.0, 5.0), (0.0, 5.0)), 'pieces_placed': [([0, 0], [6, 0], [6, 5], [0, 5])], 'try_point': [0, 5]}, 'children': []}]}
print (json.dumps(d, indent = 2, separators=(',', ': ')))
import jsbeautifier
opts = jsbeautifier.default_options()
opts.indent_size = 2
formated = jsbeautifier.beautify(json.dumps(d), opts)
with open("tree_data.json", 'w', encoding="utf8") as file:
    json.dump(d, file, indent=4)
    test = file.read()
print(test)
"""
"""
fig, ax = plt.subplots()
first = gpd.GeoSeries(LineString([[2,0], [2,2]]))
first.plot(ax = ax)
second = gpd.GeoSeries(LineString([[2,2],[2,0]]))
second.plot(ax = ax)
print(first.crosses(second))
plt.show()
"""

current_coord = [1,2]
print([tuple(current_coord)])


def erase_the_tree_and_write_hello():
    with open("tree_data.json", "w") as file:
        file.write("hello")

erase_the_tree_and_write_hello()

"""
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')

def init():
    print("hello")
    ax.clear()
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True,repeat=True, interval=1)
plt.show()

"""

