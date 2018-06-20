import itertools
from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = unitlist + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

    
def naked_twins(values):
    """
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    
    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    for unit in unitlist:
        pairs = [box for box in unit if len(values[box]) == 2]
        possible_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
        for pair in possible_twins:
            box1 = pair[0]
            box2 = pair[1]
            if values[box1] == values[box2]:
                for box in unit:
                    if box != box1 and box != box2:
                        for digit in values[box1]:
                            values[box] = values[box].replace(digit, '')

    return values
                

def eliminate(values):
    """
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:    
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in '123456789':
            x = [box for box in unit for digit in values[box]]
            if len(x) == 1:
                values[x[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict or False
    """ 
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    solved = False
    while not solved:
        solved_values_before = [box for box in values.keys() if len(values[box]) == 1]
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = [box for box in values.keys() if len(values[box]) == 1]
        solved = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
        

def search(values):
    """
    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}
    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    """
    values = reduce_puzzle(values)
    if values == False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    

def solve(grid):
    """
    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns
    -------
    dict or False
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
