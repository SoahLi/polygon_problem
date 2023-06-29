import matplotlib.pyplot as plt
from shapely.geometry import Polygon

class Map:
    cardinal_directions = {
        "n": ["", "+"],
        "e": ["+", ""],
        "s": ["", "-"],
        "w": ["-", ""],
    }
    def __init__(self, directions=[], line_lengths=[]):
        if len(line_lengths) != len(directions):
            IndexError: print("amount of lines and their dircetions do not match")
        self.line_lengths = line_lengths
        self.directions = directions
        self.num_lines = len(line_lengths)

    def create_map(self):
        x_coordinates = [1]
        y_coordinates = [1]
        for i in range(self.num_lines):
            if self.directions[i] == "n":
                x_coordinates.append(x_coordinates[-1])
                y_coordinates.append(y_coordinates[-1] + self.line_lengths[i])
            elif self.directions[i] == "e":
                x_coordinates.append(x_coordinates[-1] + self.line_lengths[i])
                y_coordinates.append(y_coordinates[-1])     
            elif self.directions[i] == "s":
                x_coordinates.append(x_coordinates[-1])
                y_coordinates.append(y_coordinates[-1] - self.line_lengths[i])
            elif self.directions[i] == "w":
                x_coordinates.append(x_coordinates[-1] - self.line_lengths[i])
                y_coordinates.append(y_coordinates[-1])
        plt.plot(x_coordinates,y_coordinates)
        print(x_coordinates)

    
my_map = Map(['n','e','n','e'],[3,3,3,3])
my_map.create_map()
plt.show(block=True)
print("hello")

        
