from typing import Optional
from shapely.geometry import Polygon, LineString
import geopandas as gpd
import copy

class Map:
    def __init__(self, coordinates):
        self.border_length = 10
        #self.shapely_map = self.create_coordinates()
        self.coordinates = coordinates
        self.shapely_map = Polygon(self.coordinates)
        self.width, self.height = self.find_area()
        self.border = self.create_border()
        self.invisible_lines = self.create_invisible_lines()
        self.width, self.height = 0, 0

        
    #want method to look like this
    #create_border(self, width: int = self.width, height: int =self.height, map: Polygon = self.shapely_map)
    def create_border(self):
        """
        Creates border for Map Object
        """
        self.border_coordinates = Polygon([(-self.border_length,-self.border_length),(self.width,-self.border_length), (self.width, self.height), (-self.border_length, self.height)])
        self.border_coordinates = self.border_coordinates.symmetric_difference(self.shapely_map)
        return self.border_coordinates
    
    def create_invisible_lines(self):
        invisible_lines = []
        additional_length = 20
        for i in range(len(self.coordinates)-1):
            if self.coordinates[i][0] == self.coordinates[i+1][0]:
                invisible_lines.append(LineString([(self.coordinates[i][0], self.coordinates[i][1]+additional_length), (self.coordinates[i+1][0], self.coordinates[i+1][1]-additional_length)]))
            else:
                invisible_lines.append(LineString([(self.coordinates[i][0]+additional_length, self.coordinates[i][1]), (self.coordinates[i+1][0]-additional_length, self.coordinates[i+1][1])]))
        return invisible_lines

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
        for coord in self.shapely_map.exterior.coords:
            current_x = coord[0]
            current_y = coord[1]
            if current_x > largest_x:
                largest_x = current_x
            if current_y > largest_y:
                largest_y = current_y
        return largest_x+self.border_length, largest_y+self.border_length
    def eat_map(self, chunk_to_eat):
        """
        remove the chunck, creating a new map with removed piece
        """
        new_map = copy.deepcopy(self.shapely_map)
        return new_map.difference(chunk_to_eat)



"""
    REMOVED METHODS

    def add_polygon(self, coordinates=[]):
        if not coordinates:
                print("please input shape coordinates")
        else:
            self.polygons.append((gpd.GeoSeries([Polygon(coordinates)])))


    self.fig, self.ax = plt.subplots()
    self.ax.set_xticks([0,5,self.border_length,15])
    self.ax.set_yticks([0,5,self.border_length,15])

    def plot_map(self):
        res = pd.concat([polygon for polygon in self.polygons])
        #res.plot(ax=self.ax, color=['b'] + ['r' for _ in range(len(res.values) - 1)])
        return res

    def display_map(self):
        plt.show()

    def close_map(self):
        plt.close()

"""
        
    