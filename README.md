# polygon_problem

Polygon Problem is a puzzle-solving algorithm designed for rectangular and square puzzles. It leverages the relationship between Shapely and GeoPandas geometries to perform comparisons on different objects, and employs a multi-tree structure to efficiently store and evaluate graphs using breadth-first search. The custom interface is implemented using Matplotlib.

## How It Works
1. Each Graph object comprises a unique map, a set of pieces, and a try point. Initially, a root Graph is created with the starting map and pieces.
2. The algorithm systematically determines every permutation of each piece at the try point, generating a new Graph object with the removed portion of the graph and piece.
3. This process continues until no new Graph objects are created.

## Limitations
### Slow Runtimes
The algorithm's runtime may increase significantly with the addition of more pieces due to its brute-force nature. Implementing a divide and conquer method, introducing multi-threading, or exploring a breadth-first search approach would improve efficiency.

### Pieces that Split the Map
Occasionally, the Shapely `.difference` method may return a MultiPolygon object as a result of a piece splitting a graph into two. Currently, this is an unavoidable error. To address this, you may need to solve each graph separately and then reintegrate the pieces used into the original graph.
