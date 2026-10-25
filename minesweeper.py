# MINESWEEPER
# Unicode characters
# ─ "\u2500"
# │ "\u2502"
# ┌ "\u250C"
# ┐ "\u2510"
# └ "\u2514"
# ┘ "\u2518"
# ├ "\u251C"
# ┤ "\u2524"
# ┬ "\u252C"
# ┴ "\u2534"
# ┼ "\u253C"

# RANDOM
import random

def grid(m=5,n=5): # generates a matrix corresponding to the printing characters to generate a mxn grid
    output=[]
    output.append(["\u250C"] + 3 * ["\u2500"] + (n - 1) * ["\u252C","\u2500","\u2500","\u2500"] + ["\u2510"])
    output.append((n+1)*["\u2502"," "," "," "])
    for i in range(m-1):
        output.append(["\u251C"] + 3 * ["\u2500"] + (n-1) * ["\u253C","\u2500","\u2500","\u2500"] + ["\u2524"])
        output.append((n + 1) * ["\u2502", " ", " ", " "])
    output.append(["\u2514"] + 3 * ["\u2500"] + (n-1) * ["\u2534","\u2500","\u2500","\u2500"] + ["\u2518"])
    return output

def m2g(m,n): # converts cell matrix coordinates to printing coordinates in a grid
    m = 2*m+1
    n = 4*n+2
    return m,n

def fill_grid(matrix): # takes up a matrix of characters, generates an empty grid of corresponding dimensions and fills the cells with the elements of the matrix
    m = len(matrix)
    n = len(matrix[0])
    # Create the grid
    output=grid(m,n)
    # Fill the grid (we replace blank spaces in the middle of the cells by specified character in M
    for i in range(m):
        for j in range(n):
            m_to_fill, n_to_fill = m2g(i,j)
            output[m_to_fill][n_to_fill] = str(matrix[i][j])
    return output

Alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def show_grid(grid, coordinates=True): # prints a grid | coordinates True will represent alpha-numeric coordinates to the side
    if coordinates == False:
        for row in grid:
            print("".join(row))
    else:
        # Row numeration (A-Z)
        nrow = (len(grid)-1)//2
        ncol = (len(grid[0])-1)//4
        for i in range (nrow):
            grid[2*i]=2*[" "]+grid[2*i]
            grid[2*i+1]=[Alphabet[i]]+[" "]+grid[2*i+1]
        grid[-1]=2*[" "]+grid[-1]
        # Column numeration (1-99)
        line=[" "," "," "]
        for j in range(ncol):
            if j < 10:
                line=line+[" "]+[str(j+1)]+[" "]+[" "]
            else:
                line=line+[str(j+1)]+[" "]+[" "]
        grid.insert(0,line)
        for row in grid:
            print("".join(row))

def set_bombs(m,n,b): # generates a mxn matrix with b bombs (●).
    field=[[" "]*n for _ in range(m)]
    bombs_set=0
    while bombs_set < b:
        m_bomb=random.choice(range(m))
        n_bomb=random.choice(range(n))
        if field[m_bomb][n_bomb]==" ":
            field[m_bomb][n_bomb]="\u25CF"
            bombs_set+=1
    for i in range(m):
        for j in range(n):
            if field[i][j]!="\u25CF":
                bombs_arround=0
                surrounding_cells=[[i-1,j-1],[i-1,j],[i-1,j+1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]]
                for cell in surrounding_cells:
                    if cell[0] in range(m) and cell[1] in range(n):
                        if field[cell[0]][cell[1]]=="\u25CF":
                            bombs_arround+=1
                if bombs_arround==0:
                    field[i][j]=" "
                else:
                    field[i][j]=str(bombs_arround)
    return field

def initial_map(matrix): # takes up the bomb matrix and generates the viewable version for the player
    output = [["\u2591" for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    return output

def flag(matrix,cell,progress):
    row=Alphabet.index(cell[0])
    col=int(cell[1:])-1
    if matrix[row][col]=="\u2591":
        matrix[row][col]="\u2588"
        progress[1]=progress[1]-1
    elif matrix[row][col]=="\u2588":
        matrix[row][col]="\u2591"
        progress[1] = progress[1] + 1
    else:
        print("This cell is already free")

def chord(matrix,cell,bombs,progress):
    # Check if conditions meet: cell is free and numbered, and a number of surrounding flags have been placed equal to the value of the number
    row = Alphabet.index(cell[0])
    col = int(cell[1:]) - 1
    if matrix[row][col].isnumeric(): # First check if cell is numbered
        surrounding_cells = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1], [row, col - 1], [row, col + 1],
                             [row + 1, col - 1],
                             [row + 1, col], [row + 1, col + 1]]
        flag_count=0
        for C in surrounding_cells: # Count the number of flags around the requested position for the chord
            if C[0] in range(len(matrix)) and C[1] in range(len(matrix[0])):
                if matrix[C[0]][C[1]] == "\u2588":
                    flag_count+=1
        if flag_count==int(matrix[row][col]): # If the number of flags matches the number in the cell
            for C in surrounding_cells:
                if C[0] in range(len(matrix)) and C[1] in range(len(matrix[0])):
                    if matrix[C[0]][C[1]] == "\u2591": # Then open unflagged cells
                        open(matrix,Alphabet[C[0]]+str(C[1]+1),bombs,progress)
        else:
            print("Invalid number of flags")
    else:
        "Cannot chord at this cell"


def open(matrix,cell,bombs,progress):
    row = Alphabet.index(cell[0])
    col = int(cell[1:]) - 1
    if matrix[row][col]=="\u2591" or matrix[row][col]=="\u2588": # If cell still not free
        matrix[row][col]=bombs[row][col] # Uncover the value of the cell
        if bombs[row][col]=="\u25CF": # If it is a bomb, highlight and show the rest of bombs. Keep correct flags and highlight wrong flags
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if bombs[i][j]=="\u25CF" and matrix[i][j]!="\u2588":
                        matrix[i][j]="\u25CF"
                    if bombs[i][j]!="\u25CF" and matrix[i][j]=="\u2588":
                        matrix[i][j]="X"
            matrix[row][col]="\u25CB"
            progress[0]=-1
        elif bombs[row][col]==" ": # If the uncovered cell is empty, open the ones around
            surrounding_cells = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1], [row, col - 1], [row, col + 1], [row + 1, col - 1],
                                 [row + 1, col], [row + 1, col + 1]]
            for C in surrounding_cells:
                if C[0] in range(len(matrix)) and C[1] in range(len(matrix[0])):
                    if matrix[C[0]][C[1]]=="\u2591":
                        open(matrix,Alphabet[C[0]]+str(C[1]+1),bombs,progress) # Note here that index coordinates are converted to human coordinates accepted by the open function
                    elif matrix[C[0]][C[1]]=="\u2588":
                        progress[1]=progress[1]+1
                        open(matrix, Alphabet[C[0]]+str(C[1]+1), bombs, progress)
    else:
        print("This cell is already free")

# ASK FOR INSTRUCTIONS
instructions=input("Do you want to see the instructions (y/N)? ")
if instructions=="y":
    print("\nMINESWEEPER by dbulnesr:\n\nFirst of all you will be asked to provide the settings for the game: number of rows, columns and bombs in the field.\nUnopened positions will be identified by \u2591, flags with \u2588 and opened cells will display a number corresponding to the number of surrounding bombs.\n\nEach turn, you can choose one of three actions:\n\t·Open: an unopened cell is opened and its value is revealed.\n\t·Flag: an unopened cell is marked with a flag, signaling for an underlying bomb.\n\t·Chord: opens the surrounding cells of an opened cells provided it has the corresponding amount of flags placed around.\n\nTo specify your action, type the name of the action followed by the cell to perform the action on.\nFor example:\nopen a1\nflag c5\nchord j12\n")
    input("Type Enter to continue")


# DETERMINE GAME SETTINGS
m_input = int(input("Provide number of rows: "))
n_input = int(input("Provide number of columns: "))
b_input = int(input("Provide number of bombs (max: "+str(m_input*n_input)+"): "))

# INITIALIZE
game_progress=[0,b_input] # 0: -1 if lost 0 if unfinished 1 if won; 1: remaining bombs
bomb_map=set_bombs(m_input,n_input,b_input)
current_state=initial_map(bomb_map)

# GO
show_grid(fill_grid(current_state))
print("Remaining bombs: "+str(game_progress[1]))
while game_progress[0]==0:
    decision=input("What do you want to do (flag/open)? ")
    if len(decision.split(" ")) == 2:
        action, cell = decision.split(" ")
        cell = cell[0].upper() + cell[1:]
        if cell[0] in Alphabet[0:(len(current_state))] and cell[1:].isnumeric()==True:
            if int(cell[1:]) in range(1,1+len(current_state[0])):
                if action == "open":
                    open(current_state, cell, bomb_map, game_progress)
                    show_grid(fill_grid(current_state))
                    if game_progress[0]==-1:
                        print("YOU LOST")

                    # Check if map has been successfully cleared
                    unfree_cells = 0
                    for i in range(len(current_state)):
                        for j in range(len(current_state[0])):
                            if current_state[i][j] == "\u2588" or current_state[i][j] == "\u2591":
                                unfree_cells += 1
                    if unfree_cells == b_input:
                        game_progress[0] = 1
                        print("YOU WON")
                    # If game still not finished, print remaining bombs
                    if game_progress[0]==0:
                        print("Remaining bombs: " + str(game_progress[1]))
                elif action == "flag":
                    flag(current_state, cell, game_progress)
                    show_grid(fill_grid(current_state))
                    print("Remaining bombs: " + str(game_progress[1]))
                elif action == "chord":
                    chord(current_state,cell,bomb_map,game_progress)
                    show_grid(fill_grid(current_state))
                    if game_progress[0]==-1:
                        print("YOU LOST")
                    # Check if map has been successfully cleared
                    unfree_cells = 0
                    for i in range(len(current_state)):
                        for j in range(len(current_state[0])):
                            if current_state[i][j] == "\u2588" or current_state[i][j] == "\u2591":
                                unfree_cells += 1
                    if unfree_cells == b_input:
                        game_progress[0] = 1
                        print("YOU WON")
                    # If game still not finished, print remaining bombs
                    if game_progress[0]==0:
                        print("Remaining bombs: " + str(game_progress[1]))

                else:
                    print("Invalid action")
            else:
                print("Invalid action")
        else:
            print("Invalid action")
    else:
        print("Invalid action")

