# dijkstra_gridworld
A grid of 100 x 100 is generated and initated with the following values: 0, 5, 10, 50. Each value corresponds to health cost. 
The algorithm is trying to find the path from the start to goal state with the minimum health cost. Start and end cells are randomly selected.

If health is depleted (max: 450) or the algorithm runs out of moves (max: 200), no optimal path has been found. 
