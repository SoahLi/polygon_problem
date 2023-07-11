from Map import Map
from Piece import Piece
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import csv

class Graph:
    def __init__(self, map: Map, pieces: list):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xticks([0,5,10,15])
        self.ax.set_yticks([0,5,10,15])
        self.map = map
        self.pieces = pieces
        self.animation = None
        self.current_piece_index = 0
    def animate(self, interval = 1000):
        def update(obj):
            obj.plot(ax=self.ax, color='red')
            if len(self.ax.collections) > 2:
                print(self.current_piece_index)
                self.ax.collections[2-self.current_piece_index].remove()
        def next_piece():
            for i in range(2, len(self.pieces)):
                self.ax.collections[i].remove()
            if self.current_piece_index != len(self.pieces):
                self.current_piece_index += 1
            
        self.animation = FuncAnimation(self.fig, update, frames=self.pieces[self.current_piece_index].get_orientations(), repeat=True, interval=interval, init_func=next_piece)

    def plot_map(self):
        gpd.GeoSeries(self.map.map).plot(ax = self.ax, color='blue')
        gpd.GeoSeries(self.map.border).plot(ax = self.ax, color='white')
    def display_graph(self, animate: bool = False):
        if animate:
            self.animate()
        plt.show(block = True)