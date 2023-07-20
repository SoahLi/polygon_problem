from shapely.geometry import Polygon, LineString
import geopandas as gpd

class Map:
    def __init__(self, directions: list[str], line_lengths: list[str]):
        if not line_lengths and not directions:
            return
        if len(line_lengths) != len(directions):
            IndexExror: print("amount of lines and their dircetions do not match")
            return
        #self.map = self.create_coordinates()
        self.coordinates = self.create_coordinates(line_lengths, directions)
        self.map = Polygon(self.coordinates)
        self.width, self.height = self.find_area()
        self.border = self.create_border()
        self.invisible_lines = self.create_invisible_lines()
        print(self.invisible_lines)
        self.width, self.height = 0, 0
        self.try_point = (0,0)
        
    def create_coordinates(self, line_lengths, directions):
        num_lines = len(line_lengths)
        x_coordinates = [0]
        y_coordinates = [0]
        cardinal_directions = {
        "n": ["", "+"],
        "e": ["+", ""],
        "s": ["", "-"],
        "w": ["-", ""],
        }
        for i in range(num_lines):
            if directions[i] == "n":
                x_coordinates.append(x_coordinates[-1] + 0)
                y_coordinates.append(y_coordinates[-1] + line_lengths[i])
            elif directions[i] == "e":
                x_coordinates.append(x_coordinates[-1] + line_lengths[i])
                y_coordinates.append(y_coordinates[-1] + 0)                 
            elif directions[i] == "s":
                x_coordinates.append(x_coordinates[-1] + 0)
                y_coordinates.append(y_coordinates[-1] - line_lengths[i])
                if y_coordinates[-1] < 0:
                    y_coordinates = self.shift_graph(y_coordinates, -y_coordinates[-1])
            elif directions[i] == "w":
                x_coordinates.append(x_coordinates[-1] - line_lengths[i])
                y_coordinates.append(y_coordinates[-1] + 0)
                if x_coordinates[-1] < 0:
                    x_coordinates = self.shift_graph(x_coordinates, -x_coordinates[-1])
        #x_coordinates, y_coordinates = shift_graph(x_coordinates, 2), shift_graph(y_coordinates, 2)
        
        return [(x, y) for x, y in zip(x_coordinates, y_coordinates)]
    
    
    def create_border(self):
        """
        Creates border for Map Object
        """
        self.border_coordinates = Polygon([(-2,-2),(self.width,-2), (self.width, self.height), (-2, self.height)])
        self.border_coordinates = self.border_coordinates.symmetric_difference(self.map)
        return self.border_coordinates
    
    def create_invisible_lines(self):
        invisible_lines = []
        additional_length = 100
        for i in range(len(self.coordinates)-1):
            if self.coordinates[i][0] == self.coordinates[i+1][0]:
                invisible_lines.append(LineString([(self.coordinates[i][0], self.coordinates[i][1]+additional_length), (self.coordinates[i+1][0], self.coordinates[i+1][1]-additional_length)]))
            else:
                invisible_lines.append(LineString([(self.coordinates[i][0]+additional_length, self.coordinates[i][1]), (self.coordinates[i+1][0]-additional_length, self.coordinates[i+1][1])]))
        print(invisible_lines)
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
        for coord in self.map.exterior.coords:
            current_x = coord[0]
            current_y = coord[1]
            if current_x > largest_x:
                largest_x = current_x
            if current_y > largest_y:
                largest_y = current_y
        return largest_x+2, largest_y+2




"""
    REMOVED METHODS

    def add_polygon(self, coordinates=[]):
        if not coordinates:
                print("please input shape coordinates")
        else:
            self.polygons.append((gpd.GeoSeries([Polygon(coordinates)])))


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
        
    