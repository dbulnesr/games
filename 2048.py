# 2048 by dbulnesr

import random
board = [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]
def start_game(board):
    new_tile(board)
    new_tile(board)

def new_tile(board):
    available_cells = find_available_cells(board)
    tile=random.choice(available_cells)
    board[tile[0]][tile[1]]=str(random.choice([2,2,2,2,2,2,2,2,2,4]))

def find_available_cells(board): # Returns a list, each a pair of indexes for empty cells
    av_cells = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                av_cells.append([i,j])
    return av_cells

def content_non_empty_cells(board,direction): # Gives the non-empty content of rows/columns of the board, in direction opposite to the input direction
    # Extract the corresponding rows/columns in the right direction
    lines = []
    if direction == "w":
        for i in range(4):
            col = []
            for j in range(4):
                col.append(board[j][i])
            lines.append(col)
    elif direction == "s":
        for i in range(4):
            col = []
            for j in reversed(range(4)):
                col.append(board[j][i])
            lines.append(col)
    elif direction == "a":
        for i in range(4):
            lines.append(board[i])
    elif direction == "d":
        for i in range(4):
            lines.append(board[i][::-1])
    # Give the non-null values of the rows/columns
    lines_non_empty = []
    for line in lines:
        line_non_empty = []
        for i in range(len(line)):
            if line[i] != " ":
                line_non_empty.append(line[i])
        lines_non_empty.append(line_non_empty)

    return lines_non_empty

def legal_moves(board): # Calculates legal moves and determines corresponding board output. Returns a list: [0]: legal moves (wasd), [1]: resulting board output
    legal=[[],[]]
    directions = ["w","s","a","d"]
    for d in directions: # Test legality of each move direction
        content=content_non_empty_cells(board,d)
        new_content = []
        for element in content:
            new_element = []
            counter=0
            while counter < len(element):
                if counter+1 < len(element):
                    if element[counter+1] == element[counter]:
                        new_element.append(str(2 * int(element[counter])))
                        counter += 2
                    else:
                        new_element.append(element[counter])
                        counter += 1
                else:
                    new_element.append(element[counter])
                    counter+=1
            new_content.append(new_element)
        result=resolve_board(new_content,d)
        if equal(board,result) == False:
            legal[0].append(d)
            legal[1].append(result)
    return legal

def equal(board1,board2):
    equals=True
    for i in range(len(board1)):
        for j in range(len(board1[0])):
            if board1[i][j]!=board2[i][j]:
                equals=False
                return equals
    return equals

def resolve_board(new_content,direction):
    # Add empty spaces to fill the grid
    result=[[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]
    for element in new_content:
        for i in range(4-len(element)):
            element.append(" ")
    # Fill depending on direction
    if direction == "w":
        for i in range(4):
            for j in range(4):
                result[i][j]=new_content[j][i]
    elif direction == "s":
        for i in range(4):
            for j in range(4):
                result[i][j]=new_content[j][::-1][i]
    elif direction == "a":
        for i in range(4):
            result[i]=new_content[i]
    elif direction == "d":
        for i in range(4):
            result[i]=new_content[i][::-1]
    return result

def is_a_win(board):
    for i in range (4):
        for j in range (4):
            if board[i][j]=="2048":
                return True
    return False

def display(M,max_size):
    m = len(M)
    n = len(M[0])
    grid = [] # Array to store the printing elements of the grid
    # Repeating units of the grid
    upper = ["\u252C"]+(max_size+2)*["\u2500"]
    inner = ["\u253C"]+(max_size+2)*["\u2500"]
    outer = ["\u2534"]+(max_size+2)*["\u2500"]
    middle = ["\u2502"]+(max_size+2)*[" "]
    # Generate grid
    grid.append(["\u250C"]+(max_size+2)*["\u2500"]+(n-1)*upper+["\u2510"])
    grid.append((n+1)*middle)
    for i in range(m-1):
        grid.append(["\u251C"]+(max_size+2)*["\u2500"]+(n-1)*inner+["\u2524"])
        grid.append((n+1)*middle)
    grid.append(["\u2514"]+(max_size+2)*["\u2500"]+(n-1)*outer+["\u2518"])

    # Fill the grid
    for i in range(m):
        for j in range(n):
            value=M[i][j]
            spaces_to_add = max_size-len(value)
            value=spaces_to_add*" "+value
            m_to_fill = 2*i+1
            n_to_fill = (3+max_size)*j+2
            for k in range(max_size):
                grid[m_to_fill][n_to_fill+k]=value[k]
    # Show grid
    for row in grid:
        print("".join(row))

# INITIALIZE
new_tile(board)
new_tile(board)
display(board,4)

finished=False
while finished==False:
    if is_a_win(board) == True:
        finished = True
        print("YOU WON")
    else:
        available_moves = legal_moves(board)
        if len(available_moves[0])==0:
            finished = True
            print("YOU LOST")
        else:
            move=input("wasd: ")
            if move in available_moves[0]:
                board=available_moves[1][available_moves[0].index(move)]
                new_tile(board)
                display(board,4)
            else:
                print("This is not a legal move because it does not change the board")

