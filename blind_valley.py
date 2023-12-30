from sys import argv
from unittest import result

restrictions = []
directions = []
grid = []
max_row, max_col = 0, 0
blocks = []
posibilities = [("H","B"), ("B", "H"), ("N", "N")]

def main():
    #check for valid input
    if len(argv) != 3:
        print("Invalid Input")
        return 1
    if argv[1][-4:] != ".txt" or argv[2][-4:] != ".txt":
        print("Invalid file format")
        return 1
    
    #open file and put it to memory
    try:
        with open(argv[1], "r") as finput:
            input = finput.readlines()
            global max_row, max_col
            max_row, max_col = make_list(input)
    except IOError:
        print("Invalid input file")
        return 1

    #solve the game
    solved = solve(grid, blocks[0])

    #write out the result
    try:
        with open(argv[2], "w") as foutput:
            if solved == True:
                output = "\n".join(" ".join(map(str, row)) for row in grid)
            else:
                output = "No solution!"
            foutput.write(output)
    except IOError:
        print("Invalid output file")
        return 1


def make_list(input):
    # append restrictions and directions
    for index, line in enumerate(input):
        if index < 4:
            restrictions.append([int(val) for val in line.strip("/n").split()])
        else:
            directions.append(line.strip("/n").split())

    # make empty grid
    for i in range(len(directions)):
        grid.append([])
        for j in range(len(directions[0])):
            grid[i].append(0)
    
    max_row = len(grid)
    max_col = len(grid[0])

    # make blocks list
    for i in range(len(directions)):
        for j in range(len(directions[0])):
            if directions[i][j] == "L":
                blocks.append([(i, j), (i, j+1)])
            if directions[i][j] == "U":
                blocks.append([(i, j), (i+1, j)])
    
    return max_row, max_col

def safe(val, row, col):
    # N has no restriction so return True regardless
    if val == "N":
        return True
    
    #if there is a neighboring cell with the same value, return false
    neighbors_positions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    for i, j in neighbors_positions:
        try:
            if grid[row+i][col+j] == val:
                return False
        except IndexError:
            continue

    # get restrictions
    current_restricts_row = -1
    current_restricts_row = -1
    if val == "B":
        current_restricts_row, current_restricts_col = restrictions[3][col], restrictions[1][row]
    elif val == "H":
        current_restricts_row, current_restricts_col = restrictions[2][col], restrictions[0][row]
    
    # get the amount of the same val in row and col. if there's no restrictions, continue
    if current_restricts_row != -1:
        val_copy_count_row = 1
        for i in range(max_row):
            if grid[i][col] == val:
                val_copy_count_row += 1
        # print(val_copy_count_row, current_restricts_row, val_copy_count_row > current_restricts_row)
        if val_copy_count_row > current_restricts_row:
            return False
    
    if current_restricts_col != -1:
        val_copy_count_col = 1
        for i in range(max_col):
            if grid[row][i] == val:
                val_copy_count_col += 1
        # print(val_copy_count_col, current_restricts_col, val_copy_count_col > current_restricts_col)
        if val_copy_count_col > current_restricts_col:
            return False

    return True

def get_next_block(current_block):
    for index, val in enumerate(blocks):
        if current_block == val:
            if index < len(blocks) - 1:
                return blocks[index + 1]
    return None

def restrics_fulfilled():
    # check if a row or a col is filled
    filled_row = []
    for i in range(len(grid)):
        filled_cell = 0
        for j in range(len(grid[0])):
            if type(grid[i][j]) == str and grid[i][j] in "BHN":
                filled_cell += 1
        if filled_cell == max_col:
            filled_row.append(i)

    filled_col = []
    for i in range(len(grid[0])):
        filled_cell = 0
        for j in range(len(grid)):
            if type(grid[j][i]) == str and grid[j][i] in "BHN":
                filled_cell += 1
        if filled_cell == max_row:
            filled_col.append(i)
    
    # check if filled row and columns have fulfilled restrictions
    for row in filled_row:
        row_restrics_b = restrictions[1][row]
        row_restrics_h = restrictions[0][row]
        val_count_b = 0
        val_count_h = 0
        for i in range(len(grid[0])):
            if grid[row][i] == "B":
                val_count_b += 1
            elif grid[row][i] == "H":
                val_count_h += 1
        if val_count_b != row_restrics_b and row_restrics_b != -1:
            return False
        if val_count_h != row_restrics_h and row_restrics_h != -1:
            return False
        
    for col in filled_col:
        col_restrics_b = restrictions[3][col]
        col_restrics_h = restrictions[2][col]
        val_count_b = 0
        val_count_h = 0
        for i in range(len(grid)):
            if grid[i][col] == "B":
                val_count_b += 1
            elif grid[i][col] == "H":
                val_count_h += 1
        if val_count_b != col_restrics_b and col_restrics_b != -1:
            return False
        if val_count_h != col_restrics_h and col_restrics_h != -1:
            return False

    return True

def solve(grid, current_block):
    # Base case: If we have reached or exceeded the end of the grid, return the current grid
    if current_block == None:
        return True

    # put B, H, and N into the selected cell
    for val in posibilities:
        safe_1 = safe(val[0], current_block[0][0], current_block[0][1])
        safe_2 = safe(val[1], current_block[1][0], current_block[1][1])

        if safe_1 and safe_2:
            grid[current_block[0][0]][current_block[0][1]] = val[0]
            grid[current_block[1][0]][current_block[1][1]] = val[1]

            if not restrics_fulfilled():
                grid[current_block[0][0]][current_block[0][1]] = 0
                grid[current_block[1][0]][current_block[1][1]] = 0
                continue

            next_block = get_next_block(current_block)
            if solve(grid, next_block):
                return True
            grid[current_block[0][0]][current_block[0][1]] = 0
            grid[current_block[1][0]][current_block[1][1]] = 0

    return False  # No solution found for the current configuration
    

main()