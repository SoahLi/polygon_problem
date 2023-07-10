import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import geopandas as gpd
import geopandas.geoseries as gs
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
        self.polygons = []
        self.line_lengths = line_lengths
        self.directions = directions
        self.num_lines = len(line_lengths)
        self.map_coordinates = []
        self.width, self.height = 0, 0
        self.border_coordinates = []
        if line_lengths and directions:
            self.map = self.add_polygon(self.create_map_coordinates())
            self.width, self.height = self.find_area()
            self.border_coordinates = self.create_border()
        

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
                    y_coordinates = self.shift_graph(y_coordinates, -y_coordinates[-1])
            elif self.directions[i] == "w":
                x_coordinates.append(x_coordinates[-1] - self.line_lengths[i])
                y_coordinates.append(y_coordinates[-1] + 0)
                if x_coordinates[-1] < 0:
                    x_coordinates = self.shift_graph(x_coordinates, -x_coordinates[-1])
        x_coordinates, y_coordinates = self.shift_graph(x_coordinates, 2), self.shift_graph(y_coordinates, 2)
        for i in range(self.num_lines):
            self.map_coordinates.append((x_coordinates[i], y_coordinates[i]))
        
        return self.map_coordinates
    
    def create_border(self):
        """
        Creates border for Map Object
        """
        self.border_coordinates = Polygon([(0,0),(self.width,0), (self.width, self.height), (0, self.height)])
        self.border_coordinates = self.border_coordinates.symmetric_difference(self.polygons[0])
        self.polygons.append(self.border_coordinates)
        return self.border_coordinates

    def shift_graph(self, coordinates, length):
        """
        Shifts graph to positive coordinates

        Args:
            coordinates (arr): Coordinates for Map Object
        """
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
        print(largest_x,largest_y)
        return largest_x+2, largest_y+2


    def add_polygon(self, coordinates=[]):
        if not coordinates:
                print("please input shape coordinates")
        else:
            self.polygons.append((gpd.GeoSeries([Polygon(coordinates)])))


"""
    REMOVED METHODS

    self.fig, self.ax = plt.subplots()
    self.ax.set_xticks([0,5,10,15])
    self.ax.set_yticks([0,5,10,15])

    def plot_map(self):
        res = pd.concat([polygon for polygon in self.polygons])
        #res.plot(ax=self.ax, color=['b'] + ['r' for _ in range(len(res.values) - 1)])
        return res

    def display_map(self):
        plt.show()

    def close_map(self):
        plt.close()

"""
        
    