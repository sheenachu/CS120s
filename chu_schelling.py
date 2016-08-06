#  CS121: Schelling Model of Housing Segregation
#
#   Program for simulating of a variant of Schelling's model of
#   housing segregation.  This program takes four parameters:
#    
#    filename -- name of a file containing a sample grid
#
#    R - The radius of the neighborhood: home (i, j) is in the
#        neighborhood of home (k,l) if |k-i| + |l-j| <= R.
#
#    threshold - minimum acceptable threshold for ratio of neighbor
#    value to the total number of homes in his neighborhood.
#
#    max_steps - the maximum number of passes to make over the
#    neighborhood during a simulation.
#
#  Sample use:python schelling.py tests/grid4.txt 1 0.51 3
#
# Estelle Ostro and Sheena Chu

import os
import sys
import utility

def is_satisfied(grid, R, threshold, location):
    ''' 
    Is the homeowner at the specified location satisfied?

    Inputs: 
        grid: the grid
        R: radius for the neighborhood
        threshold: satisfaction threshold
        location: a grid location
      
    Returns: 
        True, if the location's neighbor score is at or above the threshold
    '''
    S = 0
    P = 0
    N = 0

    for i in range(max(0, (location[0]-R)), min(len(grid), ((location[0]+R))+1)):
        for j in range(max(0,(location[1]-R)), min(len(grid), ((location[1]+R))+1)):
            if 0 <= (abs(location[0] - i) + abs(location[1]-j)) <= R:
                N = N + 1
                if grid[i][j] == grid[location[0]][location[1]]:
                    S = S + 1
                elif grid[i][j] == "O":
                    P = P + 1
    score = S + 0.5 * P
    return (score / N) >= threshold

def open_location(grid):
    '''
    Prints list of open locations.
    grid: the grid

    This function should return the coordinates of open homes
    '''
    open_loc = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == "O":
                open_loc.append((i, j))
    return open_loc

def not_satisfied(grid, R, threshold):
    '''
    Prints location of unsatisfied homeowners

    Inputs:
        grid: the grid
        R: radius for the neighborhood
        threshold: satisfaction threshold

    Returns:
        ns: list of touples of locations/homeowners that are not satisfied

    '''
    ns = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != "O":
                if not is_satisfied(grid, R, threshold, (i, j)):
                    ns.append((i,j))
    return ns

def relocate(grid, R, threshold):
    '''
    Relocates unsatisfied homeowner and
    returns list of touples of new open locations

    Inputs:
        grid: the grid
        R: radius for the neighborhood
        threshold: satisfaction threshold

    Returns:
        open_loc: new list of touples of open locations
    '''
    ns = not_satisfied(grid, R, threshold)
    open_loc = open_location(grid)
    for i in ns:
        for j in open_loc:
            grid[j[0]][j[1]] = grid[i[0]][i[1]]
            grid[i[0]][i[1]] = "O"
            if is_satisfied(grid, R, threshold, j):
                open_loc.remove(j)
                open_loc.insert(0, i)
                break
            else:
                grid[i[0]][i[1]] = grid[j[0]][j[1]]
                grid[j[0]][j[1]] = "O"
    return open_loc
    
def do_simulation(grid, R, threshold, max_steps):
    ''' 
    Do a full simulation.
    
    grid: the grid
    R: radius for the neighborhood
    threshold: satisfaction threshold
    max_steps: maximum number of steps to do

    This function should return the number of steps executed.
    '''
    counts = 0
    ns = not_satisfied(grid, R, threshold)
    for i in range(max_steps):
        counts = counts + 1
        relocate(grid, R, threshold)
        if len(ns) == 0:
            break

    return counts
        
    
def go(args):
    usage = "usage: python schelling.py <grid file name> <R > 0> <0 < threshold <= 1.0> <max steps >= 0>\n"
    grid = None
    threshold = 0.0
    R = 0
    max_steps = 0
    MAX_SMALL_GRID = 20

    
    if (len(args) != 5):
        print(usage)
        sys.exit(0)

    # parse and check the arguments
    try:
        grid = utility.read_grid(args[1])

        R = int(args[2])
        if R <= 0:
            print("R must be greater than zero")
            sys.exit(0)

        threshold = float(args[3])
        if (threshold <= 0.0 or threshold > 1.0):
            print("threshold must be between 0.0 and 1.0 not inclusive")
            sys.exit(0)

        max_steps = int(args[4])
        if max_steps <= 0:
            print("max_steps must be greater than or equal to zero")
            sys.exit(0)

    except:
        print(usage)
        sys.exit(0)
        

    num_steps = do_simulation(grid, R, threshold, max_steps)
    if len(grid) < MAX_SMALL_GRID:
        for row in grid:
            print(row)
    else:
        print("Result grid too large to print")

    print("Number of steps simulated: " + str(num_steps))

if __name__ == "__main__":
    go(sys.argv)

