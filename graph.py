import matplotlib.pyplot as plt
import matplotlib as mpl


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
        self.fig, self.ax = plt.subplots()
        self.ax.set_xticks([2,4,6,8,10])
        self.ax.set_yticks([2,4,6,8,10])
        self.line_lengths = line_lengths
        self.directions = directions
        self.num_lines = len(line_lengths)
        self.coordinates = []

    def create_coordinates(self):
        x_coordinates = [0]
        y_coordinates = [0]
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
            self.coordinates.append((x_coordinates[i], y_coordinates[i]))
        return self.coordinates
    def plot_map(self):
        print(self.coordinates)
        self.ax.plot(self.coordinates)
    def display_map(self):
        self.fig.tight_layout()
        plt.show(block = True)
    def add_polygon(self):
        self.ax.add_patch(mpl.patches.Polygon(self.coordinates))


    
my_map = Map(['e','n','w','s'],[3,3,3,3])
map_coordinates = my_map.create_coordinates()
my_map.add_polygon()
my_map.display_map()

        
