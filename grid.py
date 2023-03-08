import numpy as np

# Check if the potential cell is a valid cell and not outside of the grid space
def valid_cell(cell, size_of_grid):
    if cell[0] < 0 or cell[0] >= size_of_grid:
        return False
    if cell[1] < 0 or cell[1] >= size_of_grid:
        return False
    return True

# Moves the player can make from the current cell
def up(cell):
    return (cell[0]-1, cell[1])

def down(cell):
    return (cell[0]+1, cell[1])

def left(cell):
    return (cell[0], cell[1]-1)

def right(cell):
    return (cell[0], cell[1]+1)

# Find the path with the least number of steps
def backtrack(start_cell, end_cell, routes):
    path = [end_cell]

    size_of_grid = routes.shape[0]

    while True:
        potential_routes = []
        potential_cells = []

        directions = [up, down, left, right]

        for direction in directions:
            cell = direction(path[-1])
            if valid_cell(cell, size_of_grid):
                potential_cells.append(cell)
                potential_routes.append(routes[cell[0], cell[1]])

        least_route_index = np.argmin(potential_routes)
        path.append(potential_cells[least_route_index])

        if path[-1][0] == start_cell[0] and path[-1][1] == start_cell [1]:
            break

    return list(reversed(path))
def check_health_moves(grid, path):
    health = 450
    moves = 200

    # Determine if the path found has not depleted health or exceeded number of moves
    for p in path:
        cost = grid[p[0], p[1]] - 1
        if cost == 0:
            moves -= 1
        elif cost == 5:
            health -= 5
        elif cost == 50:
            health -= 50
            moves -= 10
        elif cost == 10:
            health -= 10
            moves -= 5
        
        if moves <= 0 or health <= 0:
            return False
    return True

# Algorithm for finding shortest path between two cells
def dijkstra(start_cell, end_cell, grid):
    grid = grid.copy()
    grid += np.ones(grid.shape)
    grid[start_cell[0], start_cell[1]] = 0
    grid[end_cell[0], end_cell[1]] = 0

    size_of_grid = grid.shape[0]

    # To keep track of visited cells
    visited = np.zeros([size_of_grid, size_of_grid], bool)

    # To keep track of the routes taken
    routes = np.ones([size_of_grid, size_of_grid]) * np.inf
    routes[start_cell[0], start_cell[1]] = 0

    current_cell = [start_cell[0], start_cell[1]]
    while True:
        directions = [up, down, left, right]
        for direction in directions:
            potential_cell = direction(current_cell)
            if valid_cell(potential_cell, size_of_grid):
                if not visited[potential_cell[0], potential_cell[1]]:
                    route = routes[current_cell[0], current_cell[1]] + grid[potential_cell[0], potential_cell[1]]
                    # Update route if it is the shortest route 
                    if route < routes[potential_cell[0], potential_cell[1]]:
                        routes[potential_cell[0], potential_cell[1]] = route

        # Set current cell as visited            
        visited[current_cell[0], current_cell[1]] = True

        # Selecting next node
        temp = routes.copy()
        temp[np.where(visited)] = np.inf
        cell_index = np.argmin(temp)

        # Update the current cell
        cell_row = cell_index // size_of_grid
        cell_col = cell_index % size_of_grid
        current_cell = (cell_row, cell_col)

        # Stop loop if the goal has been reached
        if current_cell[0] == end_cell[0] and current_cell[1] == end_cell[1]:
            break
    
    # Construct path
    path = backtrack(start_cell, end_cell, routes)

    # Determine if grid is solvable 
    if check_health_moves(grid, path):
        return path

    return 'No path found'

# Create 100x100 grid with random instances of health damage
grid = np.random.choice([0.0, 5.0, 10.0, 50.0], (100, 100))

# Generate random start and end cell indexes
start_x = np.random.randint(0, 50)
start_y = np.random.randint(0, 50)
end_x = np.random.randint(50, 99)
end_y = np.random.randint(50, 99)

# Run algorithm to solve
path = dijkstra([start_x, start_y], [end_x, end_y], grid)

# Output
print(path)