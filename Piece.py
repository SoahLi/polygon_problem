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
        self.default_orientation = [[0,0],[width,0],[width,height],[0,height]]  #left, right, up,left
        self.orientations = self.get_all_orientations(self.default_orientation)

    def get_all_orientations(self, default_orientation):
        def flip_up(self, piece):
            pass

        def flip_down(piece):
            return [(piece[0]), [piece[1][0],piece[1][1]], [piece[2][0], piece[2][1]-(piece[2][1]*2)], [piece[3][0],piece[3][1]-(piece[3][1]*2)]]
            

        def flip_left(piece):
            return [piece[0],[piece[1][0]-(piece[1][0]*2), piece[1][1]],[piece[1][0]-(piece[1][0]*2),piece[2][1]],piece[3]]
            

        def flip_right(piece):
            return [piece[0], [piece[1][0]+(piece[1][0]*-2), piece[1][1]], [piece[2][0]+(piece[2][0]*-2), piece[2][1]], piece[3]]     

        def rotate_90_clockwise(piece, width, height):
            return ([0,0], [self.height,0], [height, width], [0, width])

        def rotate_90_counterclockwise(piece):
            pass
        orientations = [default_orientation]
        #orientations.append(flip_right(orientations.append(flip_down(orientations.append(flip_left(default_orientation))))))
        orientations.append(flip_left(default_orientation))
        orientations.append(flip_down(orientations[1]))        
        orientations.append(flip_right(orientations[2]))
        orientations.append(rotate_90_clockwise(orientations[3], self.width, self.height))
        orientations.append(flip_left(orientations[4]))
        orientations.append(flip_down(orientations[5]))
        orientations.append(flip_right(orientations[6]))   
        """
        """
        return orientations

    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_orientations(self):
        return self.orientations
    def get_orientation(self):
        return self.default_orientations
    def set_width(self, width):
        self.width = width
        return self.width
    def set_height(self, height):
        self.height = height
        return self.height
    def set_default_orientation(self, orientation):
        self.default_orientations = orientation
        return self.default_orientations
    def set_orientations(self, orientations):
        self.orientations = orientations
        return self.orientations