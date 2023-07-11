from shapely.geometry import Polygon
import geopandas as gpd

class Piece:
    def __init__(self, width, height):
        """
        Args:
            width (int): width length of Piece
            height (int): height (length) of Piece
        """
        self.width = width
        self.height = height
        self.area = width*height
        self.orientations = [[(0,0), (width, 0), (width, height), (0, height)], [(0,0), (height,0), (height,width), (0, width)]]
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_orientations(self):
        return self.orientations
    def set_width(self, width):
        self.width = width
        return self.width
    def set_height(self, height):
        self.height = height
        return self.height
    def set_orientations(self, orientations):
        self.orientations = orientations
        return self.orientations