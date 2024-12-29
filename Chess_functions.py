# Coordinate translators


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']     # Used for translation coordinate system
def pretty_coordinator(ugly_coordinate):
    character = alphabet[ugly_coordinate[0]-1]
    return f"{character}{ugly_coordinate[1]}"

def ugly_coordinator(pretty_coordinate):
    number = alphabet.index(pretty_coordinate[0]) + 1
    return [number, int(pretty_coordinate[1])]


# Creating list with all potential squares for move_finder function
board_squares = []
for j in range(1, 9):
    for k in range(1, 9):
        board_squares.append([j, k])

board_pretty_coords = []
for i in board_squares:
    board_pretty_coords.append(pretty_coordinator(i))





# Scope finder returns the scope of every a certain piece. i.e. all possible squares it could move to up to
# the first blocking piece. Note that the square of the blocking piece is included and color specification is
# required for pawns. Input is as simplified as possible, taking only the coordinates of all pieces on the board,
# the piece type, its starting square and, for pawns, color.
def scope_finder(piece_type, pc,  position_coordinates, color="White"):
    sc_uc = ugly_coordinator(pc)

    moves = []

    if piece_type == "rook":
        for i in range(sc_uc[0]+1, 9):
            if [i , sc_uc[1]] not in position_coordinates:
                moves.append([i, sc_uc[1]])
            else:
                moves.append([i, sc_uc[1]])
                break
        for i in range(sc_uc[0]-1, 0, -1):
            if [i, sc_uc[1]] not in position_coordinates:
                moves.append([i, sc_uc[1]])
            else:
                moves.append([i, sc_uc[1]])
                break
        for i in range(sc_uc[1]+1, 9):
            if [sc_uc[0], i] not in position_coordinates:
                moves.append([sc_uc[0], i])
            else:
                moves.append([sc_uc[0], i])
                break
        for i in range(sc_uc[1]-1, 0, -1):
            if [sc_uc[0], i] not in position_coordinates:
                moves.append([sc_uc[0], i])
            else:
                moves.append([sc_uc[0], i])
                break

    if piece_type == "bishop":
        for i in range(1, 9 - sc_uc[0]):       
            right_main = [sc_uc[0] + i, sc_uc[1] + i]        
            if right_main in board_squares:
                if right_main not in position_coordinates:
                    moves.append(right_main)
                else:
                    moves.append(right_main)
                    break
        for i in range(1, 9 - sc_uc[0]):
             right_counter = [sc_uc[0] + i, sc_uc[1] - i]
             if right_counter in board_squares:
                if right_counter not in position_coordinates:
                    moves.append(right_counter)
                else:
                    moves.append(right_counter)
                    break
        for j in range(1, sc_uc[0]):
            left_main = [sc_uc[0]-j, sc_uc[1]-j]
            if left_main in board_squares:
                if left_main not in position_coordinates:
                    moves.append(left_main)
                else:
                    moves.append(left_main)
                    break
        for j in range(1, sc_uc[0]):
            left_counter = [sc_uc[0]-j, sc_uc[1]+j]
            if left_counter in board_squares:
                if left_counter not in position_coordinates:
                    moves.append(left_counter)
                else:
                    moves.append(left_counter)
                    break
    if piece_type == "knight":
        for i in [-2, 2]:
            for j in [-1, 1]:
                horizontal = [sc_uc[0] + i, sc_uc[1] + j]         # knight's move space is divided in 'horizontal' and 'vertical'
                if horizontal in board_squares:     # Note that any move on the board counts in case of knight
                   moves.append(horizontal)
                vertical = [sc_uc[0]+j, sc_uc[1]+i]
                if vertical in board_squares:
                    moves.append(vertical)
    if piece_type == "queen":
        moves = scope_finder("rook", pc, position_coordinates) + scope_finder("bishop", pc, position_coordinates)

    if piece_type == "king":
        for i in [-1, 1]:
            h = [sc_uc[0]+i, sc_uc[1]]        #horizontal
            v = [sc_uc[0], sc_uc[1]+i]        #vertical
            md = [sc_uc[0]+i, sc_uc[1]+i]     #main diagonal
            cd = [sc_uc[0]+i, sc_uc[1]-i]     #counter diagonal
            for j in [h, v, md, cd]:
                if j in board_squares:
                    moves.append(j)
    if piece_type == "pawn":
        if color == "White":
            for i in [-1, 1]:
                if [sc_uc[0]+i, sc_uc[1]+1] in board_squares:
                    moves.append([sc_uc[0]+i, sc_uc[1]+1])
        else:
            for i in [-1, 1]:
                if [sc_uc[0]+i, sc_uc[1]-1] in board_squares:
                     moves.append([sc_uc[0]+i, sc_uc[1]-1])

    return [m for m in moves if m != sc_uc]
# move_finder is the slightly altered version of scope_finder. Only difference being in how the pawn is treated.
# move_finder can be used to check if a given move is legal. Note that self captures are considered legal in this
# function.
def move_finder(piece_type, pc, position_coordinates, color="White"):
    if piece_type == "pawn":
        moves = []
        mv_uc = ugly_coordinator(pc)
        if color == "White":
            if mv_uc[1] == 2 and [mv_uc[0], 3] not in position_coordinates and [mv_uc[0], 4] not in position_coordinates:
                moves.append([mv_uc[0], 4])
            if [mv_uc[0], mv_uc[1]+1] not in position_coordinates:
                moves.append([mv_uc[0], mv_uc[1]+1])
            for i in [-1, 1]:
                if [mv_uc[0]+i, mv_uc[1]+1] in position_coordinates:
                    moves.append([mv_uc[0]+i, mv_uc[1]+1])
        else:
            if mv_uc[1] == 7 and [mv_uc[0], 6] not in position_coordinates and [mv_uc[0], 5] not in position_coordinates:
                moves.append([mv_uc[0], 5])
            if [mv_uc[0], mv_uc[1]-1] not in position_coordinates:
                moves.append([mv_uc[0], mv_uc[1]-1])
            for i in [-1, 1]:
                if [mv_uc[0]+i, mv_uc[1]-1] in position_coordinates:
                    moves.append([mv_uc[0]+i, mv_uc[1]-1])
        return [m for m in moves if m != mv_uc]
    
    else:
        return scope_finder(piece_type, pc, position_coordinates, color)


white_piece_dic = {"wR_1" : "rook", "wN_1" : "knight", "wB_1" : "bishop", "wQ" : "queen", "wK" : "king",
            "wB_2" : "bishop", "wN_2" : "knight", "wR_2" : "rook"}
for i in range(1, 9):
    white_piece_dic[f"wP_{i}"] = "pawn"

black_piece_dic = {"bR_1" : "rook", "bN_1" : "knight",
            "bB_1" : "bishop", "bQ" : "queen", "bK" : "king", "bB_2" : "bishop", "bN_2" : "knight",
            "bR_2" : "rook"}
for i in range(1, 9):
    black_piece_dic[f"bP_{i}"] = "pawn"

piece_type_dic = white_piece_dic | black_piece_dic

def scope_counter(color_position, position_coordinates, color):
    scope_list = []
    for piece in list(color_position.keys()):
            scope_counter_piece_type = piece_type_dic[piece]
            scope_counter_pc = pretty_coordinator(color_position[piece])
            scope_iteration = scope_finder(scope_counter_piece_type, scope_counter_pc, position_coordinates, color)
            scope_list += scope_iteration
    return scope_list

def move_counter(color_position, position_coordinates, color):
    move_counter_move_list = []
    for piece in color_position:
        move_counter_piece_type = piece_type_dic[piece]
        move_counter_pc = pretty_coordinator(color_position[piece])
        move_iteration = move_finder(move_counter_piece_type, move_counter_pc, position_coordinates, color)
        move_counter_move_list += move_iteration
    return move_counter_move_list