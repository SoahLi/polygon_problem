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
        self.width_until_edge = w
        self.height_until_edge = h
        self.current_coord = [0,0]
        #width of line to be added (int)
        self.current_line = 0
        self.current_direction = ""
        self.last_direction = 's'
        self.current_GeoSeries_line = None
        self.all_GeoSeries_lines = []
        self.directions = []
        self.fig, self.ax = plt.subplots() 
    def reset(self):
        self.width_until_edge = self.width
        self.height_until_edge = self.height
        self.current_coord = [0,0]
        #width of line to be added (int)
        self.current_line = 0
        self.current_direction = ""
        self.last_direction = 's'
        self.current_GeoSeries_line = None
        self.all_GeoSeries_lines = []
        self.directions = []
        self.fig, self.ax = plt.subplots() 

    def generate_map_coordinates(self):
        self.reset()
        line_lengths = []
        cardinal_cycles = {"e": ['e', 'n', 'e', 's'],
                           "n": ['n', 'w', 'n', 'e'],
                           "w": ['w', 's', 'w', 'n'],
                           "s": ['s', 'e', 's', 'w'] }
        cycle_key = "e"
        current_cycle = cardinal_cycles[cycle_key]
        cycle_pointer = 0
        recycle_counter = 1
        recycle_line_number = 0
        # add first line as east for consistency
        #self.add_line(randint(1, int(self.width/8)), "e")

        def line_does_not_change():
            if self.current_line == 0:
                return True
            else:
                return False
        def recycle():
            if len(self.all_GeoSeries_lines) == 0:
                return
            nonlocal cycle_pointer
            cycle_pointer -= 1
            if cycle_pointer == -1:
                cycle_pointer = 3
            self.current_direction = current_cycle[cycle_pointer]
            if self.current_direction == "n" or self.current_direction == "s":
                old_line_length = round(self.all_GeoSeries_lines[-1].iloc[-1].coords[1][1] - self.all_GeoSeries_lines[-1].iloc[-1].coords[0][1], 1)
            elif self.current_direction == "e" or self.current_direction == "w":
                old_line_length = round(self.all_GeoSeries_lines[-1].iloc[-1].coords[1][0] - self.all_GeoSeries_lines[-1].iloc[-1].coords[0][0], 1)
            if self.current_direction == "n":
                self.height_until_edge = round(self.height_until_edge + old_line_length, 1)
            elif self.current_direction == "e":
                self.width_until_edge = round((self.width_until_edge + old_line_length), 1)
            elif self.current_direction == "s":
                self.height_until_edge = round(self.height_until_edge + old_line_length, 1)
            elif self.current_direction == "w":
                self.width_until_edge = round(self.width_until_edge + old_line_length, 1)
            self.current_line -= old_line_length
            self.all_GeoSeries_lines.pop(-1)
            self.ax.collections[-1].remove()
            if len(self.all_GeoSeries_lines) == 0:
                self.current_coord = [0,0]
            else:
                self.current_coord[0] = self.all_GeoSeries_lines[-1].iloc[-1].coords[1][0]
                self.current_coord[1] = self.all_GeoSeries_lines[-1].iloc[-1].coords[1][1]


        def can_complete():
            #if cycle_key == "s" and (self.height_until_edge == 9.4):
            if cycle_key == "s" and (self.height_until_edge == 9.4):
                while self.current_direction != "w":
                    recycle()
                    self.current_direction = current_cycle[cycle_pointer]
                    self.current_line = randint(1, int(self.width/2))
                self.add_line(self.width - self.width_until_edge, self.current_direction, list(self.all_GeoSeries_lines[-1].iloc[-1].coords[1]))
                self.current_line = self.all_GeoSeries_lines[-1].length
                if self.line_intersects():
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    return "line_intersection"
                self.add_line(self.height - self.height_until_edge, "s")
                return "graph_completed"
            return "can't_complete"
                

        while sum(line_lengths) < self.width:
                
            self.current_line = randint(1, int(self.width/2))
            if len(self.all_GeoSeries_lines) == 0:
                self.current_line += randint(2, 3)
            self.current_direction = current_cycle[cycle_pointer]
            # if the direction chosen is on the same axis as the previous line placed
            """
            if self.last_direction == opposite_cardinal_directions[self.current_direction] or self.current_direction == self.last_direction:
                continue            
            """
            if self.current_direction == "n":
                
                #while the line is past the height barrier
                while self.current_coord[1] + self.current_line > self.height:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                while self.line_intersects():
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                    #decrease the length of the line
                    self.current_line = round(self.current_line - .1, 1)
                """
                """
                if self.not_too_close() == False:
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                #self.current_line = round(self.current_line - .1, 1)                
                if line_does_not_change():
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                self.add_line()
                if self.height_until_edge == 0:
                        if self.current_direction != cycle_key: 
                            cycle_pointer += 1
                            if cycle_pointer == len(current_cycle):
                                cycle_pointer = 0
                            continue
                        cycle_key = "w"
                        current_cycle = cardinal_cycles[cycle_key]
                        cycle_pointer = 0
                        continue
                        #self.width_until_edge = self.all_GeoSeries_lines[-1].iloc[-1].coords[1][0]
            if self.current_direction == "s":
                if (can_complete() == "graph_completed"):
                    map_coordinates = []
                    for i in range(len(self.all_GeoSeries_lines)):
                        map_coordinates.append(self.all_GeoSeries_lines[i].iloc[-1].coords[1])
                    return map_coordinates
                elif (can_complete() == "line_intersection"):
                    continue
                else:
                    pass
                
                # while the line is below the height barrier
                while self.current_coord[1] - self.current_line < 0:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                while self.line_intersects():
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                    self.current_line = round(self.current_line - .1, 1)
                """
                """
                if self.not_too_close() == False:
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                #self.current_line = round(self.current_line - .1, 1)                
                if line_does_not_change():
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                self.add_line()
                if self.height_until_edge == self.height:
                        if self.current_direction != cycle_key:
                            cycle_pointer += 1
                            if cycle_pointer == len(current_cycle):
                                cycle_pointer = 0
                            continue
                        cycle_key = "e"
                        current_cycle = cardinal_cycles[cycle_key]
                        cycle_pointer = 0
                        continue
                        #self.height_until_edge = self.all_GeoSeries_lines[-1].iloc[-1].coords[1][0]

            if self.current_direction == "e":
                # while line is past the width barrier
                while self.current_coord[0] + self.current_line > self.width: 
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1

                        continue
                while self.line_intersects():
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                    self.current_line = round(self.current_line - .1, 1)
                """
                """
                if self.not_too_close() == False:
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                #self.current_line = round(self.current_line - .1, 1)                
                if line_does_not_change():
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                self.add_line()
                if self.width_until_edge == 0:
                        if self.current_direction != cycle_key:
                            cycle_pointer += 1
                            if cycle_pointer == len(current_cycle):
                                cycle_pointer = 0
                            continue
                        cycle_key = "n"
                        current_cycle = cardinal_cycles[cycle_key]
                        cycle_pointer = 0
                        continue
                        #self.height_until_edge = self.all_GeoSeries_lines[-1].iloc[-1].coords[1][1]
            if self.current_direction == "w":
                # while line is past the width barrier
                while self.current_coord[0] - self.current_line < 0:
                    self.current_line = round(self.current_line - .1, 1)
                else:
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                while self.line_intersects():
                    if line_does_not_change():
                        for i in range(recycle_counter):
                            recycle()
                        recycle_counter += 1
                        recycle_line_number = len(self.all_GeoSeries_lines)-1
                        continue
                    self.current_line = round(self.current_line - .1, 1)
                """
                """
                if self.not_too_close() == False:
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                #self.current_line = round(self.current_line - .1, 1)                
                if line_does_not_change():
                    for i in range(recycle_counter):
                        recycle()
                    recycle_counter += 1
                    recycle_line_number = len(self.all_GeoSeries_lines)-1
                    continue
                self.add_line()
                if self.width_until_edge == self.width:
                        if self.current_direction != cycle_key:
                            cycle_pointer += 1
                            if cycle_pointer == len(current_cycle):
                                cycle_pointer = 0
                            continue
                        cycle_key = "s"
                        current_cycle = cardinal_cycles[cycle_key]
                        cycle_pointer = 0
                        continue
                        #self.height_until_edge = self.all_GeoSeries_lines[-1].iloc[-1].coords[1][1]
            if len(self.all_GeoSeries_lines)-1 == recycle_line_number:
                recycle_counter = 1
            cycle_pointer += 1
            if cycle_pointer == len(current_cycle):
                cycle_pointer = 0


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
    
    def add_line(self, line=None, direction=None, starting_coord=None):
        """
        Adds line to map permanently
        """
        if not line:
            line = self.current_line
        if not direction:
            direction = self.current_direction
        if not starting_coord:
            starting_coord = self.current_coord
        temp = deepcopy(starting_coord)
        
        if direction == "n":
            starting_coord[1] = round(starting_coord[1] + line, 1)
            self.height_until_edge = round(self.height_until_edge - line, 1)
        elif direction == "e":
            self.current_coord[0] = round(starting_coord[0] + line, 1)
            self.width_until_edge = round((self.width_until_edge - line), 1)
        elif direction == "s":
            starting_coord[1] = round(starting_coord[1] - line, 1)
            self.height_until_edge = round(self.height_until_edge + line, 1)
        elif direction == "w":
            starting_coord[0] = round(starting_coord[0] - line, 1)
            self.width_until_edge = round(self.width_until_edge + line, 1)
        self.current_coord = starting_coord
        
        gpd.GeoSeries(LineString([temp, self.current_coord])).plot(ax=self.ax)
        self.all_GeoSeries_lines.append(gpd.GeoSeries(LineString([temp, self.current_coord])))
        self.directions.append(self.current_direction)
        self.last_direction = self.current_direction

    
    def not_too_close(self):
        """
        Checks how close the current_line is to all permanently placed lines by a factor of .2
        """
        if self.current_direction == "n":
            companion_coord = [self.current_coord[0], self.current_coord[1] + self.current_line]
        if self.current_direction == "s":
            companion_coord = [self.current_coord[0], self.current_coord[1] - self.current_line]
        if self.current_direction == "e":
            companion_coord = [self.current_coord[0]  + self.current_line, self.current_coord[1]]
        if self.current_direction == "w":
            companion_coord = [self.current_coord[0]  - self.current_line, self.current_coord[1]]
        current_coord = gpd.GeoSeries(Point(companion_coord))
        current_coord.plot(ax = self.ax)
        for i in range(len(self.all_GeoSeries_lines)):
            while round(current_coord.distance(self.all_GeoSeries_lines[i])[0], 1) < .6:
                self.ax.collections[-1].remove()
                if self.current_direction == "n":
                    companion_coord[1] = round(companion_coord[1] - .1, 1)
                elif self.current_direction == "s":
                    companion_coord[1] = round(companion_coord[1] + .1, 1)
                elif self.current_direction == "w":
                    companion_coord[0] = round(companion_coord[0] + .1, 1)
                elif self.current_direction == "e":
                    companion_coord[0] = round(companion_coord[0] - .1, 1)
                if self.current_coord[0] == companion_coord[0] and self.current_coord[1] == companion_coord[1] :
                    return False
                current_coord = gpd.GeoSeries(Point(companion_coord))
                current_coord.plot(ax = self.ax)
        if self.current_direction == "n":
            self.current_line = round(abs(companion_coord[1] - self.current_coord[1]), 1)
        elif self.current_direction == "s":
            self.current_line = round(abs(companion_coord[1] - self.current_coord[1]), 1)
        elif self.current_direction == "w":
            self.current_line = round(abs(companion_coord[0] - self.current_coord[0]), 1)
        elif self.current_direction == "e":
            self.current_line = round(abs(companion_coord[0] - self.current_coord[0]), 1)
        print(self.current_line)
        self.ax.collections[-1].remove()
        return True

"""
new_map = MapGenerator(10,10)
new_map = new_map.create_map()
the_map = Map(new_map)
the_graph = Graph(map = the_map)
the_graph.display_graph()
print()
"""
maps = []
my_map_generator = MapGenerator(10,10)
for i in range(20):

    maps.append(Graph(map = Map(my_map_generator.generate_map_coordinates())))

maps[0].display_graph()

