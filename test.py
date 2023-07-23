from Map import Map
from Piece import Piece
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from Graph import Graph
import csv
polygon1 = Polygon([(0, 0), (0, 3), (3, 3), (3, 0)])
polygon2 = Polygon([(2, 2), (2, 5), (5, 5), (5, 2)])

# Calculate the difference between the polygons
resulting_geometry = polygon2.difference(polygon1)

# Check the type of the resulting geometry
if isinstance(resulting_geometry, Polygon):
    print("Result is a single Polygon.")
elif isinstance(resulting_geometry, MultiPolygon):
    print("Result is a MultiPolygon with multiple disjointed polygons.")
else:
    print("Result is of another type.")

# Print the individual polygons in the MultiPolygon (if applicable)
if isinstance(resulting_geometry, MultiPolygon):
    for poly in resulting_geometry:
        print(poly)
    



"""
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')

def init():
    print("hello")
    ax.clear()
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True,repeat=True, interval=1)
plt.show()

"""

