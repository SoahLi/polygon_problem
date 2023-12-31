from map import Map
from Piece import Piece
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
import copy
import os, psutil


class Graph:
    def __init__(self, pieces: list = [], map: Map = None, pieces_placed: list[Piece] = [], try_point: tuple = (0,0)):
        self.fig, self.ax = plt.subplots()
        #These ticks are helpful for now but will need to make dynamic at some point
        self.x_values = [i*5 for i in range(100)]
        self.y_values = [i*5 for i in range(100)]
        self.ax.set_xticks(self.x_values)
        self.ax.set_yticks(self.y_values)
        self.ax.axvline(x=self.x_values[0], color='black', linestyle='-', alpha=0.5)
        self.ax.axhline(y=self.y_values[0], color='black', linestyle='-', alpha=0.5)
        self.map = map
        self.border = None
        self.pieces_placed = pieces_placed
        if self.map: 
            self.border = self.map.border
            #The 2 comes from the Map and the border
            self.total_pieces_placed = 2+len(self.pieces_placed)# + len(self.map.invisible_lines)
            self.plot_map()
        #The reason(I think) You need to replace the pieces, is because the pieces effectively become the new border. Without placing the pieces, create a hole in the border
        self.GeoSeries_pieces_placed = self.place_pieces(self.pieces_placed)
        self.pieces = pieces
        if try_point != (0,0) and pieces:
            def adjust_pieces_to_try_point(pieces, distance: list[int]):
                """
                transform piece coordinates to be tested on try point
                Args:
                    pieces: the pieces
                    distance: the x and y distances to transform pieces
                """
                for piece in pieces:
                    for orientation in piece.orientations:                 
                        orientation.coordinates = [[coord[0] + distance[0], coord[1] + distance[1]] for coord in orientation.coordinates]  
                return pieces  
            old_try_point = self.pieces[0].orientations[0].coordinates[0]
            distance_between_try_points = [try_point[0]-old_try_point[0], try_point[1]-old_try_point[1]]
            self.pieces = adjust_pieces_to_try_point(self.pieces, distance_between_try_points)
        self.animation = None
        self.current_piece_index = 0
        self.try_point = try_point
        self.is_complete = False
        #self.displace_pieces(piece_displacement)

    def plot_map(self):
        self.border = gpd.GeoSeries(self.map.border)
        self.border.plot(ax = self.ax, facecolor = "none", edgecolor = "none")
        gpd.GeoSeries(self.map.shapely_map).plot(ax = self.ax, color='blue')

    """
    SETS PIECES OUTSIDE OF MAP
    """
    def get_memory_location(self):
        return hex(id(self))

    def __str__(self):
        pieces_str = "\n".join([f"Piece {i+1}: {piece.default_orientation}" for i, piece in enumerate(self.pieces)])
        pieces_placed_str = "\n".join([f"Piece {i+1}: {piece.coordinates}" for i, piece in enumerate(self.pieces_placed)])
        return f"Graph:\n" \
            f"Map: {self.map}\n" \
            f"Pieces: \n{pieces_str}\n" \
            f"Pieces Placed: \n{pieces_placed_str}\n" \
            f"Try Point: {self.try_point}\n"

    def solve(self):
        """
        for each piece, determine whether it can fit at the try_point 0,0
        if if can, keep going with this piece, updating the try_point and testing pieces until completing the perimater
        create a new Map with the perimater filled (it would be a smaller version of the previous map)
        repeat until all pieces are filled
        
        """
        #at the end of this code I need:
            # new Map ✓
            # reduced set of Pieces ✓ 
            # new try_point with ✓
            # piece adjustment metric with new try point ✓

        #generated by chatgpt
        def on_line(point_a, point_b, check_point):
            # Calculate the cross product and dot product
            cross_product = (check_point[1] - point_a[1]) * (point_b[0] - point_a[0]) - (point_b[1] - point_a[1]) * (check_point[0] - point_a[0])
            dot_product = (check_point[0] - point_a[0]) * (point_b[0] - point_a[0]) + (check_point[1] - point_a[1]) * (point_b[1] - point_a[1])

            # Check if the points are collinear and if check_point is between point_a and point_b
            if abs(cross_product) < 0.001 and dot_product >= 0 and dot_product <= (point_b[0] - point_a[0]) * (point_b[0] - point_a[0]) + (point_b[1] - point_a[1]) * (point_b[1] - point_a[1]):
                return True

            return False
        def doesent_touch_placed_pieces(current_coordinate):
            for piece in self.pieces_placed:
                for coordinate in piece.coordinates:
                    if coordinate == current_coordinate:
                        return False
            return True
        def doesent_touch_map_corner(current_coordinate):
            for coordinate in [[int(x),int(y)] for x,y in tuple(self.map.shapely_map.exterior.coords)]:
                if current_coordinate == coordinate:
                    
                    return False
            return True
        def find_highest_coord(coordinates):
            if not coordinates: return None
            highest_coord_idx = 0
            for i in range(len(coordinates)):
                if coordinates[i][1] > coordinates[highest_coord_idx][1]:
                    highest_coord_idx = i
            return coordinates[highest_coord_idx]
        def iterate_to_next_point(current_coord, destination_coord):
            if destination_coord[0] < current_coord[0]:
                current_coord[0] -= .1
            elif destination_coord[0] > current_coord[0]:
                current_coord[0] += .1
            else:
                pass
            if destination_coord[1] < current_coord[1]:
                current_coord[1] -= .1
            elif destination_coord[1] > current_coord[1]:
                current_coord[1] += .1
            else:
                pass
            return list(map(lambda x: round(x, 1), current_coord))
        def find_next_coord():
            """
            Traverse the edge of the map until a new point is found that does not touch 
            another piece(The point usually lies on the corner of a piece)
            """
            #grab coordinates of map corners
            map_coords = [list(coord) for coord in self.map.shapely_map.exterior.coords[::-1]]
            current_coord = [map_coords[0][0], map_coords[0][1]]
            for i in range(1, len(map_coords)-1):
                #while current coord not equal the next coord
                while current_coord != map_coords[i]:
                    #I should probably do something about this
                    if current_coord == map_coords[i]:
                        break
                    does_touch_piece = False
                    current_GeoSeries_coord = gpd.GeoSeries(Point(current_coord))
                    current_GeoSeries_coord.plot(ax = self.ax, color = 'orange')
                    for piece in self.GeoSeries_pieces_placed:
                        if piece.touches(current_GeoSeries_coord).bool():
                            does_touch_piece = True
                    if does_touch_piece:
                        current_coord = iterate_to_next_point(current_coord, map_coords[i])
                        self.ax.collections[-1].remove()
                        continue
                    else:
                        self.ax.collections[-1].remove()
                        return list(map(int, current_coord))
            self.ax.collections[-1].remove()
            current_coord = [int(elem) for elem in current_coord]
            return current_coord

                    

        #method instuction start
        new_graphs = [] #child_graphs
        #for each piece
        for index in range(len(self.pieces)):
            #for each orientation of each piece
            for orientation in self.pieces[index].orientations:

                shapely_orientation = Polygon(orientation.coordinates)
                GeoSeries_orientation = gpd.GeoSeries(shapely_orientation)
                GeoSeries_orientation.plot(ax=self.ax)
                self.GeoSeries_pieces_placed.append(GeoSeries_orientation)
                #if the placed piece is outside of the map
                if GeoSeries_orientation.touches(self.border, align=True).bool():
                    new_try_point = find_next_coord()
                    new_map = self.map.eat_map(shapely_orientation)

                    #if new map creates multimap(Break in map from piece)
                    if isinstance(new_map, MultiPolygon):
                        continue
                        
                    new_map = Map(tuple(new_map.exterior.coords))
                    new_pieces = copy.deepcopy(self.pieces)
                    #remove placed piece
                    new_pieces.pop(index)
                    new_graph = Graph(new_pieces, new_map, self.pieces_placed+[orientation], new_try_point)
                    new_graphs.append(new_graph)
                    self.ax.collections[-1].remove()
                    self.GeoSeries_pieces_placed.pop(-1)
                else:
                    self.ax.collections[-1].remove()
                    self.GeoSeries_pieces_placed.pop(-1)
        plt.close(self.fig)
        #print(plt.get_fignums())
        print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
        # my_driver.node_information_at_highest_index(633)
        if not new_graphs:
            return None
        return new_graphs
            

    
    def display_graph(self, animate: bool = False):
        if animate:
            self.animate()
        plt.show()

    def displace_pieces(self, displacement):
        for piece in self.pieces:
            for orientation in piece:
                for coordinate in orientation.coordinates:
                    coordinate[0] += displacement[0]
                    coordinate[1] += displacement[1]
    def place_pieces(self, pieces):
        """
        Function to display pieces, which become the new border
        """
        GeoSeries_pieces = []
        for piece in pieces:
            placed_piece = gpd.GeoSeries(Polygon(piece.coordinates))
            GeoSeries_pieces.append(placed_piece)
            placed_piece.plot(ax = self.ax, color = piece.color)
        return GeoSeries_pieces
    
    def animate(self, interval: int = 500):
        def update(obj_coordinates):
            if len(self.ax.collections) > self.total_pieces_placed:
                self.ax.collections[self.total_pieces_placed-self.current_piece_index].remove()
            gpd.GeoSeries(Polygon(obj_coordinates)).plot(ax=self.ax, color='white')
        ani = FuncAnimation(self.fig, update, frames=[Polygon(orientation.coordinates) for piece in self.pieces for orientation in piece.orientations], interval=interval)
        plt.show()
#        def update(obj):
#            obj.plot(ax=self.ax, color='red')
#            if len(self.ax.collections) > 2:
#                print(self.current_piece_index)
#                self.ax.collections[2-self.current_piece_index].remove()
#                hello world!