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
        self.current_line = 0
        self.current_direction = ""
        self.last_direction = 's'
        self.current_GeoSeries_line = None
        self.all_GeoSeries_lines = []
        self.count = 0   
        self.fig, self.ax = plt.subplots()     

    def create_map(self):
        directions = []
        line_lengths = []
        cardinal_directions = ['n', 'e', 's', 'w']
        opposite_cardinal_directions = {
            'n': 's',
            's': 'n',
            'e': 'w',
            'w': 'e',
        }
        while sum(line_lengths) < self.width:
            #current_line = random_double_to_tenths(1,int(width/2))
            self.current_line = randint(1, int(self.width/2))
            self.current_direction = cardinal_directions[randint(0, 3)]
            if self.current_direction == opposite_cardinal_directions[self.last_direction] or self.current_direction == self.last_direction:
                continue
            if self.current_direction == "n":
                print("iteration" + str(self.count))
                if self.current_coord[1] + current_line < self.height:
                    while self.line_intersects():
                        if self.current_direction == 'n' or self.current_direction == 'e':
                            current_line = round(current_line - .1, 1)
                        elif self.current_direction == 's' or self.current_direction == 'w':
                            current_line = round(current_line + .1, 1)
                        print(current_line)
                    temp = deepcopy(self.current_coord)
                    self.current_coord[1] += current_line
                    #not_too_close()
                    self.all_GeoSeries_lines.append(gpd.GeoSeries(LineString([temp, self.self.current_coord])))
                    print("line from")
                    print(self.current_coord)
                    print('to')
                    print(self.current_coord)
                    self.height_until_edge += current_line
                else:
                    continue
            if self.current_direction == "s":
                print("iteration" + str(self.count))
                if self.current_coord[1] - current_line > 0:
                    while self.line_intersects():
                        if self.current_direction == 'n' or self.current_direction == 'e':
                            current_line = round(current_line - .1, 1)
                        elif self.current_direction == 's' or self.current_direction == 'w':
                            current_line = round(current_line - .1, 1)
                        print(current_line)
                    temp = deepcopy(self.self.current_coord)
                    self.current_coord[1] -= current_line
                    #not_too_close()
                    self.all_GeoSeries_lines.append(gpd.GeoSeries(LineString([temp, self.current_coord])))
                    print("line from")
                    print(self.current_coord)
                    print('to')
                    print(self.current_coord)
                    self.height_until_edge -= current_line
                else:
                    continue
            if self.current_direction == "e":
                print("iteration" + str(self.count))
                if self.current_coord[0] + self.current_line < self.width:
                    while self.line_intersects():
                        if self.current_direction == 'n' or self.current_direction == 'e':
                            current_line = round(current_line - .1, 1)
                        elif self.current_direction == 's' or self.current_direction == 'w':
                            current_line = round(current_line - .1, 1)
                        print(current_line)
                    temp = deepcopy(self.current_coord)
                    self.current_coord[0] += self.current_line
                    #not_too_close()
                    self.all_GeoSeries_lines.append(gpd.GeoSeries(LineString([temp, self.current_coord])))
                    print("line from")
                    print(self.current_coord)
                    print('to')
                    print(self.current_coord)
                    self.width_until_edge += self.current_line
                else:
                    continue
            if self.current_direction == "w":
                print("iteration" + str(self.count))
                if self.current_coord[0] - self.current_line > 0:
                    while self.line_intersects():
                        if self.current_direction == 'n' or self.current_direction == 'e':
                            current_line = round(self.current_line - .1, 1)
                        elif self.current_direction == 's' or self.current_direction == 'w':
                            current_line = round(self.current_line - .1, 1)
                        print(current_line)
                    temp = deepcopy(self.current_coord)
                    self.current_coord[0] -= current_line
                    #not_too_close()
                    self.all_GeoSeries_lines.append(gpd.GeoSeries(LineString([temp, self.current_coord])))
                    print("line from")
                    print(self.current_coord)
                    print('to')
                    print(self.current_coord)
                    self.width_until_edge -= current_line
                else:
                    continue
            if self.width_until_edge == self.width or self.height_until_edge == self.height:
                break
            directions.append(self.current_direction)
            last_direction = self.current_direction
            self.count += 1

    def line_intersects(self):
        if self.current_direction == 'n':
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, [self.current_coord[0], self.current_coord[1] + self.current_line]]))
            print("current line with modification")
            print([self.current_coord, [self.current_coord[0], self.current_coord[1] + self.current_line]])

        if self.current_direction == 's':
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, [self.current_coord[0], self.current_coord[1] - self.current_line]]))
            print("current line with modification")
            print([self.current_coord, [self.current_coord[0], self.current_coord[1] - self.current_line]])

        if self.current_direction == 'e':
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, [self.current_coord[0] + self.current_line, self.current_coord[1]]]))
            print("current line with modification")
            #print([current_coord, [current_coord[0] + current_line, current_coord[1]]])

        if self.current_direction == 'w':
            current_GeoSeries_line = gpd.GeoSeries(LineString([self.current_coord, [self.current_coord[0] - self.current_line, self.current_coord[1]]]))
            print("current line with modification")
           # print([current_coord, [current_coord[0] - current_line, current_coord[1]]])
            

        current_GeoSeries_line.plot(ax = self.ax)
        for i in range(len(self.all_GeoSeries_lines)-1):
            if current_GeoSeries_line.intersects(self.all_GeoSeries_lines[i]).bool():
                print("current_line intersects with " + str(i))
                self.ax.collections[-1].remove()
                return True
        return False
    
    def not_too_close(self):
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

new_map = MapGenerator(5, 5)
new_map = new_map.create_map()
print()
