from Map import Map
from Piece import Piece
import itertools
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import csv
import time

class Graph:
    def __init__(self, map: Map, pieces: list):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xticks([0,5,10,15])
        self.ax.set_yticks([0,5,10,15])
        self.map = map
        self.pieces = pieces
        self.animation = None
        self.current_piece_index = 0
        self.total_pieces_placed = 2
    def animate(self, interval: int = 1000):
        def update(obj):
            if len(self.ax.collections) > self.total_pieces_placed:
                self.ax.collections[self.total_pieces_placed-self.current_piece_index].remove()
            obj.plot(ax=self.ax, color='red')
        ani = FuncAnimation(self.fig, update, frames=list(itertools.chain.from_iterable([obj.get_orientations() for obj in self.pieces])), interval=interval)


    def plot_map(self):
        gpd.GeoSeries(self.map.map).plot(ax = self.ax, color='blue')
        gpd.GeoSeries(self.map.border).plot(ax = self.ax, color='white')
    def display_graph(self, animate: bool = False):
        if animate:
            self.animate()
        plt.show(block = True)






#        def update(obj):
#            obj.plot(ax=self.ax, color='red')
#            if len(self.ax.collections) > 2:
#                print(self.current_piece_index)
#                self.ax.collections[2-self.current_piece_index].remove()