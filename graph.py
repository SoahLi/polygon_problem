import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon
from descartes import PolygonPatch
import geopandas as gpd
import pandas as pd
class Map:
    cardinal_directions = {
        "n": ["", "+"],
        "e": ["+", ""],
        "s": ["", "-"],
        "w": ["-", ""],
    }

    def __init__(self, directions=[], line_lengths=[]):
        if len(line_lengths) != len(directions):
            IndexError: print("amount of lines and their dircetions do not match")
        # create a graph
        # self.fig, self.ax = plt.subplots()
        # self.ax.set_xticks([0,5,10,15])
        # self.ax.set_yticks([0,5,10,15])
        self.polygons = []
        #variables for methods
        self.line_lengths = line_lengths
        self.directions = directions
        self.num_lines = len(line_lengths)
        self.map_coordinates = []
        self.length, self.width = 0, 0
        self.border = []
        if line_lengths and directions:
            self.map = self.add_polygon(self.create_map_coordinates())
            self.length, self.width = self.find_area()
            self.border = self.create_border()
        

    def create_map_coordinates(self):
        x_coordinates = [0]
        y_coordinates = [0]
        for i in range(self.num_lines):
            if self.directions[i] == "n":
                x_coordinates.append(x_coordinates[-1] + 0)
                y_coordinates.append(y_coordinates[-1] + self.line_lengths[i])
            elif self.directions[i] == "e":
                x_coordinates.append(x_coordinates[-1] + self.line_lengths[i])
                y_coordinates.append(y_coordinates[-1] + 0)                 
            elif self.directions[i] == "s":
                x_coordinates.append(x_coordinates[-1] + 0)
                y_coordinates.append(y_coordinates[-1] - self.line_lengths[i])
                if y_coordinates[-1] < 0:
                    y_coordinates = self.shift_graph_to_positive(y_coordinates, -y_coordinates[-1])
            elif self.directions[i] == "w":
                x_coordinates.append(x_coordinates[-1] - self.line_lengths[i])
                y_coordinates.append(y_coordinates[-1] + 0)
                if x_coordinates[-1] < 0:
                    x_coordinates = self.shift_graph_to_positive(x_coordinates, -x_coordinates[-1])
        for i in range(self.num_lines):
            self.map_coordinates.append((x_coordinates[i], y_coordinates[i]))
        self.find_area()
        return self.map_coordinates
    
    def create_border(self):
        pass
    
    def shift_graph_to_positive(self, coordinates, length):
        for i in range(len(coordinates)):
            coordinates[i] += length
        return coordinates

    def find_area(self):
        largest_x = 0
        largest_y = 0
        for coord in self.map_coordinates:
            current_x = coord[0]
            current_y = coord[1]
            if current_x > largest_x:
                largest_x = current_x
            if current_y > largest_y:
                largest_y = current_y
        return largest_x, largest_y
            

    def plot_map(self):
        self.ax.plot(self.map_coordinates)
        
    def display_map(self):
        print("before")
        for polygon in self.polygons:
            print(polygon)
        print("after")
        print("\n\n\n")
        res = pd.concat([polygon for polygon in self.polygons])
        res.plot(color=['b'] + ['r' for _ in range(len(res.values) - 1)])
        plt.show()

    def close_map(self):
        plt.close()

    def add_polygon(self, coordinates=[]):
        if not coordinates:
                print("please input shape coordinates")
        else:
            print("im in here!!!")
            self.polygons.append((gpd.GeoSeries([Polygon(coordinates)])))
        # if not coordinates:
        #     self.ax.add_patch(mpl.patches.Polygon(self.map_coordinates, color=my_color))
        # else:
        #     self.ax.add_patch(mpl.patches.Polygon(coordinates, color=my_color))

my_map = Map(['s','e','n','e', 'n', 'w', 'n', 'w', 's', ],[3,3,3,3,3,4,2,2,5])
#my_map = Map(['w','s','e','n'], [3,3,3,3])
#my_map = Map()
#map_coordinates = my_map.create_map_coordinates()
my_map.add_polygon([(0, 0), (5,0), (5,5), (0,5)])
#my_map.add_polygon([(0,0),(0,1),(1,1),(1,0)])
my_map.display_map()

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


        
