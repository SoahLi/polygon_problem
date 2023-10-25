# Polygon Problem

Polygon Problem is a puzzle-solving algorithm designed for rectangular and square puzzles. It leverages the relationship between Shapely and GeoPandas geometries to perform comparisons on different objects, and employs a multi-tree structure to efficiently store and evaluate graphs using breadth-first search. The custom interface is implemented using Matplotlib.

## How It Works
1. Each Graph object comprises a unique map, a set of pieces, and a try point. Initially, a root Graph is created with the starting map and pieces.
2. The algorithm systematically determines every permutation of each piece at the try point, generating a new Graph object with the removed portion of the graph and piece.
3. This process continues until no new Graph objects are created.

## Examples
<img width="300" alt="Screen Shot 2023-10-24 at 9 14 43 PM" src="https://github.com/SoahLi/polygon_problem/assets/120991436/27729890-13d5-490d-af45-b2bd60be25db">
<img width="300" alt="Screen Shot 2023-10-21 at 9 31 59 AM" src="https://github.com/SoahLi/polygon_problem/assets/120991436/7bc25ca4-9300-46fa-a047-68a3d5d77e8e">
<img width="400" alt="Screen Shot 2023-10-24 at 9 37 50 PM" src="https://github.com/SoahLi/polygon_problem/assets/120991436/a7b0ba0e-e2e0-4675-81f3-d0c190955813">



## Limitations
### Slow Runtimes
The algorithm's runtime may increase significantly with the addition of more pieces due to its brute-force nature. Implementing a divide and conquer method, introducing multi-threading, or exploring a breadth-first search approach would improve efficiency.

### Pieces that Split the Map
Occasionally, the Shapely `.difference` method may return a MultiPolygon object as a result of a piece splitting a graph into two. Currently, this is an unavoidable error. One solution may be to solve each split graph separately and then reintegrate the pieces used into the original graph.
