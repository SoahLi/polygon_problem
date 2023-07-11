from Map import Map
from Piece import Piece
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
import csv


fig, ax = plt.subplots()
ax.set_xticks([tick for tick in range(0,100,10)])
ax.set_yticks([tick for tick in range(0,100,10)])
my_piece = Piece(2,3)
my_map = Map(['e','n','w','s'], [20,20,20,20])
objects = my_map.polygons
print(objects[1])
objects[0].plot(ax = ax, color="blue") 
objects[1].plot(ax = ax, color="red")   
my_piece_orientations = my_piece.get_orientations()

def update(frame):
    if len(ax.collections) > 2:
        ax.collections[len(ax.collections)-1].remove()
    gpd.GeoSeries(Polygon(frame)).plot(ax = ax, color='purple')



ani = FuncAnimation(fig, update, frames=my_piece_orientations, repeat=True, interval = 500)
plt.show()


"""
my_map = Map(['s', 'e', 'n', 'e', 'n', 'w', 'n', 'w', 's'], [3, 3, 3, 3, 3, 4, 2, 2, 5])
#my_map.add_polygon([(0, 0), (5, 0), (5, 5), (0, 5)])
#my_map.add_polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
#my_map.add_polygon([(5, 5), (7, 5), (7, 7), (5, 7)])
    

with open("pieces.csv", "r") as pieces:
    example = pieces.readline(1)
    print(example)

objects = my_map.polygons

fig, ax = plt.subplots()  # Create a figure and axis

def restart():
    ax.clear()
    
objects[0].plot(ax = ax, color="blue") 
objects[1].plot(ax = ax, color="red")

def update(frame):
    frame.plot(ax=ax, color = "red")  # Plot the GeoSeries on the specified axis

#ani = FuncAnimation(fig, update, frames=objects[1:], init_func = restart, repeat = True)
"""


#test = my_map.plot_map()
#test.plot()
#plt.show()



# my_polygon = (Polygon([(0, 0), (5,0), (5,5), (0,5)]))
# my_graph = gpd.GeoSeries(my_polygon)
# my_polygon2 =  (Polygon([(1, 1), (6,1), (6,6), (1,6)]))
# my_graph2 = gpd.GeoSeries(my_polygon2)
# res = pd.concat([my_graph, my_graph2])
# print(res.values)
# res.plot(color=['b'] + ['r' for _ in range(len(res.values) - 1)])
# plt.show()


# my_poly = gpd.GeoSeries([Polygon([(0, 0), (5,0), (5,5), (0,5)])])
# print("this is the poly")
# print(my_poly)


# poly1 = Polygon( [(0, 0), (5,0), (5,5), (0,5) ] )
# poly3 = Polygon([(0,0), (.5,0), (.5,.5),(0,.5)])
# myPoly = gpd.GeoSeries([poly1, poly3])
# print(poly3.intersects(poly1))
# myPoly.plot()
# plt.show()


#EXAMPLE CODE#

"""import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()"""
