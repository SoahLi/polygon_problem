from map import Map
from piece import Piece
from tree import TreeNode
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
from graph import Graph
import csv
import json
from random import randint
from copy import deepcopy

class MapGenerator:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.width_until_edge = 0
        self.height_until_edge = 0
        self.current_coord = [0,0]
        #width of line to be added (int)
        self.current_line = 0
        self.current_direction = ""
        self.last_direction = 's'
        self.current_GeoSeries_line = None
        self.all_GeoSeries_lines = []
        self.directions = []
        self.count = 0   
        self.fig, self.ax = plt.subplots()     

    def create_map(self):
        line_lengths = []
        cardinal_directions = ['n', 'e', 's', 'w']
        opposite_cardinal_directions = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e',
        }
        # add first line as east for consistency
        self.add_line(randint(1, int(self.width/8)), "e")

        while sum(line_lengths) < self.width:
            self.current_line = randint(1, int(self.width/8))
            self.current_direction = cardinal_directions[randint(0, 3)]
            # if the direction chosen is on the same axis as the previous line placed
            if self.last_direction == opposite_cardinal_directions[self.current_direction] or self.current_direction == self.last_direction:
                continue
            if self.current_direction == "n":
                
                #while the line is past the height barrier
                while self.current_coord[1] + self.current_line > self.height:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    # if no changes were made
                    if self.current_line == 0:
                        continue
                while self.line_intersects():
                    if self.current_line == 0:
                        continue
                    #decrease the length of the line
                    self.current_line = round(self.current_line - .1, 1)
                if self.current_line == 0:
                    continue
                self.add_line()
            if self.current_direction == "s":
                # whlie the line is below the height barrier
                while self.current_coord[1] - self.current_line < 0:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    # if no changes were made
                    if self.current_line == 0:
                        continue
                while self.line_intersects():
                    if self.current_line == 0:
                        continue
                    self.current_line = round(self.current_line - .1, 1)
                if self.current_line == 0:
                    continue
                self.add_line()
            if self.current_direction == "e":
                # while line is past the width barrier
                while self.current_coord[0] + self.current_line > self.width:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    #if no changes were made
                    if self.current_line == 0:
                        continue
                while self.line_intersects():
                    if self.current_line == 0:
                        continue
                    self.current_line = round(self.current_line - .1, 1)
                if self.current_line == 0:
                    continue
                self.add_line()
            if self.current_direction == "w":
                # while line is past the width barrier
                while self.current_coord[0] - self.current_line < 0:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    #if no changes were made
                    if self.current_line == 0:
                        continue
                while self.line_intersects():
                    if self.current_line == 0:
                        continue
                    self.current_line = round(self.current_line - .1, 1)
                if self.current_line == 0:
                    continue
                self.add_line()
            if self.width_until_edge == self.width or self.height_until_edge == self.height:
                break
            self.count += 1

    def line_intersects(self):
        """
        Checks current_line and returns True if current_line intersects any permanently placed line
        """
        if self.current_direction == 'n':
            new_coord = [self.current_coord[0], self.current_coord[1] + self.current_line]
            new_coord = [round(coord, 1) for coord in new_coord]
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, new_coord]))

        if self.current_direction == 's':
            new_coord = [self.current_coord[0], self.current_coord[1] - self.current_line]
            new_coord = [round(coord, 1) for coord in new_coord]
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, new_coord]))


        if self.current_direction == 'e':
            new_coord = [self.current_coord[0] + self.current_line, self.current_coord[1]]
            new_coord = [round(coord, 1) for coord in new_coord]
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, new_coord]))

        if self.current_direction == 'w':
            new_coord = [self.current_coord[0] - self.current_line, self.current_coord[1]]
            new_coord = [round(coord, 1) for coord in new_coord]
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, new_coord]))
        current_GeoSeries_line.plot(ax = self.ax)
        for i in range(len(self.all_GeoSeries_lines)-1):
            if current_GeoSeries_line.intersects(self.all_GeoSeries_lines[i]).bool():
                #print("self.current_line intersects with " + str(i))
                self.ax.collections[-1].remove()
                return True
            if current_GeoSeries_line.touches(self.all_GeoSeries_lines[i]).bool():
                #print("self.current_line intersects with " + str(i))
                self.ax.collections[-1].remove()
                return True
        self.ax.collections[-1].remove()
        return False
    
    def add_line(self, line = None, direction = None):
        """
        Adds line to map permanently
        """
        if line:
            self.current_line = line
        if direction:
            self.current_direction = direction
        temp = deepcopy(self.current_coord)
        if self.current_direction == "n":
            self.current_coord[1] += self.current_line
            self.height_until_edge += self.current_line
        if self.current_direction == "e":
            self.current_coord[0] += self.current_line
            self.width_until_edge += self.current_line
        if self.current_direction == "s":
            self.current_coord[1] -= self.current_line
            self.height_until_edge -= self.current_line
        if self.current_direction == "w":
            self.current_coord[0] -= self.current_line
            self.width_until_edge -= self.current_line
        gpd.GeoSeries(LineString([temp, self.current_coord])).plot(ax = self.ax)
        self.all_GeoSeries_lines.append(gpd.GeoSeries(LineString([temp, self.current_coord])))
        self.directions.append(self.current_direction)
        self.last_direction = self.current_direction
    
    def not_too_close(self):
        """
        Checks how close the current_line is to all permanently placed lines by a factor of .2
        """
        current_point = gpd.GeoSeries(Point(self.current_coord))
        current_point.plot(ax = self.ax)
        for i in range(len(self.all_GeoSeries_lines)-1):
            print("point " + str(i) + " is " + str(current_point.distance(self.all_GeoSeries_lines[i])[0]) + " units away")
            while current_point.distance(self.all_GeoSeries_lines[i])[0] < .2:
                self.ax.collections[-1].remove()
                if self.current_direction == "n" or self.current_direction == "s":
                    self.current_coord[1] = round(self.current_coord[1] - .1, 1)
                elif self.current_direction == "e" or self.current_direction == "w":
                    self.current_coord[0] = round(self.current_coord[0] - .1, 1)
                current_point = gpd.GeoSeries(Point(self.current_coord))
                current_point.plot(ax = self.ax)
        self.ax.collections[-1].remove()

new_map = MapGenerator(25,25)
new_map = new_map.create_map()
print()
