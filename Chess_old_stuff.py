import Chess_functions as chessf

# Defining function that determines potential moves, pc indicating pretty_coordinate, uc being ugly "
def move_finder(piece_type, pc):
    potential_moves = []
    uc = chessf.ugly_coordinator(pc)

    if piece_type == "Rook":
        for i in range(1, 9):
            potential_moves.append([i, uc[1]])
            potential_moves.append([uc[0], i])
    elif piece_type == "Knight":
        for j in [2, -2]:
            for k in [1, -1]:
               # only add squares that are actually on the board
               if [uc[0] + j, uc[1] + k] in chessf.board_squares:
                   potential_moves.append([uc[0] + j, uc[1] + k])
               if [uc[0] + k, uc[1] + j] in chessf.board_squares:
                   potential_moves.append([uc[0] + k, uc[1] + j])
    elif piece_type == "Bishop":
        for i in range(-7, 8):
            if [uc[0] +i, uc[1] + i] in chessf.board_squares:
                potential_moves.append([uc[0] +i, uc[1] + i])       # diagonals
            if [uc[0] +i, uc[1] - i] in chessf.board_squares:
                potential_moves.append([uc[0] +i, uc[1] - i])       # counter diagonals
    elif piece_type == "Queen":
        potential_moves = move_finder("Rook", pc) + move_finder("Bishop", pc)
    elif piece_type == "King":
        for i in [-1, 1]:
            potential_moves.append([uc[0] +i, uc[1] - i])       # diagonals
            potential_moves.append([uc[0] +i, uc[1] + i])       # counter diagonals
            potential_moves.append([uc[0] +i, uc[1]])           # horizontal
            potential_moves.append([uc[0], uc[1] + i])          # vertical

        for j in potential_moves:                               # filter for squares on the board
            if j not in chessf.board_squares:
                potential_moves.remove(j)

    potential_moves = [m for m in potential_moves if m != uc]
    return potential_moves

# Defining function to find all legal moves, depending on the position

def legal_move_finder(piece_type, pc,  color, white_position, black_position):
    potential_moves = move_finder(piece_type, pc)
    blocking_friendly_position = {}
    blocking_enemy_position = {}
    uc = chessf.ugly_coordinator(pc)
    legal_moves = potential_moves
    illegal_moves = []
    white_coordinates = list(white_position.values())
    white_pieces = list(white_position.keys())
    black_coordinates = list(black_position.values())
    black_pieces = list(black_position.keys())

    if color == "White":
        blocking_friendly_coordinates = [f for f in potential_moves if f in white_coordinates]

        for piece in white_pieces:
            if white_position[piece] in blocking_friendly_coordinates:
                blocking_friendly_position[piece] = white_position[piece]

        blocking_enemy_coordinates = [h for h in potential_moves if h in black_coordinates]

        for piece in black_pieces:
            if black_position[piece] in blocking_enemy_coordinates:
                blocking_enemy_position[piece] = black_position[piece]

    if color == "Black":
        blocking_friendly_coordinates = [f for f in potential_moves if f in black_coordinates]

        for piece in black_pieces:
            if black_position[piece] in blocking_friendly_coordinates:
                blocking_friendly_position[piece] = black_position[piece]

        blocking_enemy_coordinates = [h for h in potential_moves if h in white_coordinates]

        for piece in white_pieces:
            if white_position[piece] in blocking_enemy_coordinates:
                blocking_enemy_position[piece] = white_position[piece]

    if piece_type == "Rook":
        for friend in list(blocking_friendly_position.values()):
            if friend[0] == uc[0] and friend[1] > uc[1]:      # if blocking coordinate is on the same file
                for f in range(friend[1], 9):
                    if [friend[0], f] in legal_moves:
                        legal_moves.remove([friend[0], f])
            if friend[0] == uc[0] and friend[1] < uc[1]:
                for f in range(1, friend[1] +1):
                    if [friend[0], f] in legal_moves:
                        legal_moves.remove([friend[0], f])
            if friend[0] > uc[0] and friend[1] == uc[1]:        # if blocking coordinate is on the same rank
                for f in range(friend[0], 9):
                    if [f, friend[1]] in legal_moves:
                        legal_moves.remove([f, friend[1]])
            if friend[0] < uc[0] and friend[1] == uc[1]:
                for f in range(1, friend[0] +1):
                    if [f, friend[1]] in legal_moves:
                        legal_moves.remove([f, friend[1]])

        for non_friend in list(blocking_enemy_position.values()):
            if non_friend[0] == uc[0] and non_friend[1] > uc[1]:      # if blocking coordinate is on the same file
                for f in range(non_friend[1]+1, 9):
                    if [non_friend[0], f] in legal_moves:
                        legal_moves.remove([non_friend[0], f])
            if non_friend[0] == uc[0] and non_friend[1] < uc[1]:
                for f in range(1, non_friend[1]):
                    if [non_friend[0], f] in legal_moves:
                        legal_moves.remove([non_friend[0], f])
            if non_friend[0] > uc[0] and non_friend[1] == uc[1]:        # if blocking coordinate is on the same rank
                for f in range(non_friend[0]+1, 9):
                    if [f, non_friend[1]] in legal_moves:
                        legal_moves.remove([f, non_friend[1]])
            if non_friend[0] < uc[0] and non_friend[1] == uc[1]:
                for f in range(1, non_friend[0]):
                    if [f, non_friend[1]] in legal_moves:
                        legal_moves.remove([f, non_friend[1]])

    return legal_moves

# # Check checker
# # if color == "White":
# #     if self.white_position["wK"] in black_scope:
# #         check_indicator = True
# # if color == "Black":
# #     if self.black_position["bK"] in white_scope:
# #         check_indicator = True
#
# if check_indicator:
#     if piece_type != "king":
#         return print(f"{color} hangs...   the king! \n (move your king bozo)")

# if color == "white":
#     o_pc = chessf.pretty_coordinator(friendly_position['wK'])
#     potential_moves = chessf.move_finder(piece_type, o_pc, position_coordinates)
#     for pmove in potential_moves:
#         if pmove in black_scope or pmove in friendly_position.values():
#             potential_moves.remove(pmove)
#             danger_squares.append(pmove)
# if color == "Black":
#     o_pc = chessf.pretty_coordinator(friendly_position['bK'])
#     potential_moves = chessf.move_finder(piece_type, o_pc, position_coordinates)
#     for pmove in potential_moves:
#         if pmove in white_scope or pmove in friendly_position.values():
#             potential_moves.remove(pmove)
#             danger_squares.append(pmove)
# if uc not in potential_moves and uc in danger_squares:
#     return print(f"{color}\'s king is trying to commit suicide, someone stop him!")
# if uc not in potential_moves:
#     return print("In chess, the king can not teleport")

# potential_saves = chessf.move_counter(enemy_position, position_coordinates_updated, anti_color)
# valid_saves = potential_saves
# for potential_save in potential_saves:
#     position_coordinates_hypo = position_coordinates_updated
#     position_coordinates_hypo.append(potential_save)
#     scope_list_hypo = chessf.scope_counter(friendly_position_updated, position_coordinates_hypo, color)
#     if enemy_position[enemy_king] in scope_list_hypo:
#         valid_saves.remove(potential_save)


# if color == "White":
#     self.white_position[piece] = uc
#     scope_list = chessf.scope_counter(self.white_position, position_coordinates, color)
#     check_count = scope_list.count(self.black_position["bK"])
#     if check_count > 0:
#         position_coordinates = list(self.white_position.values()) + list(self.black_position.values())
#         op_king = chessf.pretty_coordinator(enemy_position['bK'])
#         potential_moves_op_king = chessf.move_finder('king', op_king, position_coordinates)
#         for pmove in potential_moves_op_king:
#             if pmove in scope_list:
#                 potential_moves_op_king.remove(pmove)
#         if not potential_moves_op_king:
#             self.game_status = "White won"
#             print(f"Checkmate! White won")

# if color == "Black":
#     self.black_position[piece] = uc
#     scope_list = chessf.scope_counter(self.black_position, position_coordinates, color)
#     check_count = scope_list.count(self.white_position["wK"])
#     if check_count > 0:
#         position_coordinates = list(self.white_position.values()) + list(self.black_position.values())
#         op_king = chessf.pretty_coordinator(enemy_position['wK'])
#         potential_moves_op_king = chessf.move_finder('king', op_king, position_coordinates)
#         for pmove in potential_moves_op_king:
#             if pmove in scope_list:
#                 potential_moves_op_king.remove(pmove)
#         if not potential_moves_op_king:
#             self.game_status = "Black won"
#             print(f"Checkmate! Black won")
#     if check_count == 1 and self.game_status == "Ongoing":
#         print("Check!")
#     if check_count == 2 and self.game_status == "Ongoing":
#         print("Double Check!")
#     if check_count > 2 and self.game_status == "Ongoing":
#         print("Check! Check! Check!")
