if __name__ == '__main__':
    import Chess_functions as chessf
# setting up a starting position for a chess game by combining white and black position

white_starting_position = {"wR_1" : [1,1], "wN_1" : [2,1], "wB_1" : [3,1], "wQ" : [4,1], "wK" : [5,1],
            "wB_2" : [6,1], "wN_2" : [7,1], "wR_2" : [8,1]}
black_starting_position = {"bR_1" : [1,8], "bN_1" : [2,8],"bB_1" : [3,8], "bQ" : [4,8], "bK" : [5,8],
                  "bB_2" : [6,8], "bN_2" : [7,8], "bR_2" : [8,8]}

for i in range(1, 9):
    white_starting_position[f"wP_{i}"] = [i, 2]
    black_starting_position[f"bP_{i}"] = [i, 7]

starting_position = white_starting_position | black_starting_position

# Introducing a piece dictionary

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

def valid_square(pc):
    if pc[0] in chessf.alphabet and pc[1] in range(1, 9):
        return True
    else:
        return False

def piece_type_abbreviation(piece_type):
    if piece_type == "rook":
        return "R"
    if piece_type == "knight":
        return "N"
    if piece_type == "bishop":
        return "B"
    if piece_type == "queen":
        return "Q"
    if piece_type == "king":
        return "K"
    if piece_type == "pawn":
        return ""


def move_notary(piece_type, captures, potential_pieces, o_pc, pc, check_count, checkmate_indicator, en_passant_indicator):
    check = ""
    capture = ""
    checkmate = ""
    piece_type_abbrev = piece_type_abbreviation(piece_type)
    piece_index = ""
    en_passant = ""
    if potential_pieces == 2:
        piece_index = o_pc[0]
    if captures:
        capture = "x"
    if piece_type == "pawn" and captures:
        piece_index = o_pc[0]
    if piece_type == "pawn" and not captures:
        piece_index = ""

    if check_count > 0 and checkmate_indicator == False:
        check = "+"
    if checkmate_indicator:
        checkmate = "#"
    if en_passant_indicator:
        en_passant = "  e.p."
    if piece_type == 'O-O':
        return 'O-O'
    if piece_type == 'O-O-O':
        return 'O-O-O'
    else:
        return f"{piece_type_abbrev}{piece_index}{capture}{pc}{check}{checkmate}{en_passant}"




