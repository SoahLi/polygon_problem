from map import Map
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import geopandas as gpd

my_map = Map(['s', 'e', 'n', 'e', 'n', 'w', 'n', 'w', 's'], [3, 3, 3, 3, 3, 4, 2, 2, 5])
my_map.add_polygon([(0, 0), (5, 0), (5, 5), (0, 5)])
my_map.add_polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
my_map.add_polygon([(5, 5), (7, 5), (7, 7), (5, 7)])
objects = my_map.polygons

fig, ax = plt.subplots()  # Create a figure and axis

def restart():
    print("hello")
    ax.clear()
    objects[0].plot(ax = ax, color="blue") 


def update(frame):
    frame.plot(ax=ax, color = "red")  # Plot the GeoSeries on the specified axis

ani = FuncAnimation(fig, update, frames=objects[1:], init_func = restart, repeat = True)
plt.show()


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
