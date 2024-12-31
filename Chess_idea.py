
#TODO: involve stockfish
#TODO: find way to visualize the board in external application
#TODO: weird bug that after queen check in fools mate game, all pieces in white position get shuffled
#TODO: make sure every return statement is accompanied by turn reduction

import Chess_board_pieces as chessps
import Chess_functions as chessf






class ChessGame:
    # Position
    white_position = chessps.white_starting_position
    black_position = chessps.black_starting_position
    turn = 0     # turn indicates the turn of the piece that last moved
    game_moves_tracker = []     # list to store game moves in
    game_status = "Ongoing"
    launched_pawn_tracker = []
    captured_pieces = []
    castle_rights_dic = {'wK':False, 'wR_1':False, 'wR_2':False, 'bK':False, 'bR_1':False, 'bR_2':False}

    def reset(self):
        self.game_status = "Ongoing"
        self.white_position = chessps.white_starting_position
        self.black_position = chessps.black_starting_position
        self.turn = 0
        self.game_moves_tracker = []
        self.launched_pawn_tracker = []

    def position(self):
        return self.white_position | self.black_position

    def resign(self):
        if self.turn % 2 ==1:
            print("White won by resignation")
            self.game_status = "White won"
        else:
            print("Black won by resignation")
            self.game_status = "Black won"

    def move(self, piece_type, destination='none', origin='none'):
        if self.game_status != "Ongoing":
            return print(f"This game is over; {self.game_status}. Create another game, or reset")

        # Space for deriving simple values from initial input
        self.turn += 1
        check_indicator = False
        position_coordinates = list(self.white_position.values()) + list(self.black_position.values())
        black_scope = chessf.scope_counter(self.black_position, position_coordinates, "Black")
        white_scope = chessf.scope_counter(self.white_position, position_coordinates, "White")

        if self.turn % 2 == 1:     
            color = "White"
            anti_color = "Black"
            game_move = (self.turn +1)/2
            friendly_position = self.white_position
            enemy_position = self.black_position
            friendly_king = "wK"
            enemy_king = "bK"
            friendly_scope = white_scope
            enemy_scope = black_scope
        else:
            color = "Black"
            anti_color = "White"
            game_move = self.turn/2
            friendly_position = self.black_position
            enemy_position = self.white_position
            friendly_king = "bK"
            enemy_king = "wK"
            friendly_scope = black_scope
            enemy_scope = white_scope
        # Converting game_move values to integer
        game_move = int(game_move)



        # Priority statements
        if piece_type not in ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen', 'O-O', 'O-O-O']:
            self.turn -= 1
            return print("Unknown piece tries to enter the game...")
        if piece_type in ['O-O', 'O-O-O'] and destination != 'none':
            self.turn -= 1
            return print("What?")
        if piece_type in ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen'] and destination == 'none':
            self.turn -= 1
            return print('OK')
        if destination not in chessf.board_pretty_coords and destination != 'none':
            self.turn -= 1
            return print(f"{color}\'s {piece_type} ventures off the board...   Wait, is that a bishop?!")

        potential_pieces = []
        if piece_type not in ['O-O', 'O-O-O']:
            uc = chessf.ugly_coordinator(destination)
        else:
            uc = 'none'
        danger_squares = []
        friendly_fire_squares = []
        if piece_type == "king":
            potential_pieces.append('king')
            potential_moves = chessf.move_finder("king", chessf.pretty_coordinator(friendly_position[friendly_king]),
                                                 position_coordinates)
            piece = friendly_king
            o_pc = chessf.pretty_coordinator(friendly_position[friendly_king])
            for potential_move in potential_moves:
                if potential_move in enemy_scope:
                    danger_squares.append(potential_move)
                if potential_move in list(friendly_position.values()):
                    friendly_fire_squares.append(potential_move)
            if uc in friendly_fire_squares:
                self.turn -= 1
                return print("Friendly fire!")
            if uc in danger_squares:
                self.turn -= 1
                return print(f"{color}\'s king is trying to commit suicide, someone stop him!")
            if uc not in potential_moves:
                self.turn -= 1
                return print(f"{color}\'s king is trying to teleport?")

        en_passant_potential = False
        if piece_type not in ['king', 'O-O', 'O-O-O']:
            for ppiece in list(friendly_position.keys()):
                if chessps.piece_type_dic[ppiece] == piece_type:
                    potential_pieces.append(ppiece)
            if not potential_pieces:
                self.turn -= 1
                return print("Piece is nowhere to be found")
            potential_origins = []
            pieces_to_be_removed = []
            potential_origins_to_be_removed = []
            for ppiece in potential_pieces:
                iteration_pc = chessf.pretty_coordinator(friendly_position[ppiece])
                iteration_uc = chessf.ugly_coordinator(iteration_pc)
                potential_origins.append(iteration_pc)
                potential_piece_moves = chessf.move_finder(piece_type, iteration_pc, position_coordinates, color)
                if piece_type == 'pawn':
                    if self.turn >= 2:
                        if self.launched_pawn_tracker[self.turn - 2] != 'none':
                            lpawn_square = self.launched_pawn_tracker[self.turn - 2]
                            en_passant_squares = []
                            for i in [-1, 1]:
                                en_passant_squares.append([lpawn_square[0] + i, lpawn_square[1]])
                            if iteration_uc in en_passant_squares:
                                en_passant_potential = True
                                if anti_color == "White":
                                    en_passant_move = [lpawn_square[0], lpawn_square[1]-1]
                                else:
                                    en_passant_move = [lpawn_square[0], lpawn_square[1]+1]
                                potential_piece_moves.append(en_passant_move)
                if uc not in potential_piece_moves:
                    pieces_to_be_removed.append(ppiece)
                    potential_origins_to_be_removed.append(iteration_pc)
            for rpiece in pieces_to_be_removed:
                potential_pieces.remove(rpiece)
            for rorigin in potential_origins_to_be_removed:
                potential_origins.remove(rorigin)
            if not potential_pieces:
                self.turn -= 1
                return print(f"{color}\'s {piece_type} is trying to teleport!")
            if len(potential_pieces) == 1:
                piece = potential_pieces[0]
                o_pc = chessf.pretty_coordinator(friendly_position[piece])
            if len(potential_pieces) == 2:
                if origin == 'none':
                    self.turn -= 1
                    return print(f"Please specify the origin of the {piece_type} you wish to move.")
                if  origin not in potential_origins:
                    self.turn -= 1
                    return print("Please specify a valid origin square")
                for ppiece in potential_pieces:
                    if friendly_position[ppiece] == chessf.ugly_coordinator(origin):
                        piece = ppiece
                        o_pc = origin


        if uc in list(friendly_position.values()):
            self.turn -= 1
            return print("Friendly fire!")

        #Check checker
        if friendly_position[friendly_king] in enemy_scope:
            if piece_type in ['O-O', 'O-O-O']:
                self.turn -= 1
                return print("Unfortunately, checks can not be evaded by castling.")
            sim_friendly_position = friendly_position
            sim_friendly_position[piece] = uc
            sim_position_coordinates = list(enemy_position.values()) + list(sim_friendly_position.values())
            sim_enemy_scope = chessf.scope_counter(enemy_position, sim_position_coordinates, anti_color)
            if sim_friendly_position[friendly_king] in sim_enemy_scope:
                self.turn -= 1
                return print("You are in check, protect your king bozo")

        #Pinned piece checker
        if piece_type not in ['O-O', 'O-O-O']:
            pin_friendly_position = friendly_position
            pin_friendly_position[piece] = uc
            pin_enemy_position = {}
            for i in range(1, len(list(enemy_position.keys()))):
                pin_enemy_position[list(enemy_position.keys())[i]] = list(enemy_position.values())[i]
            enemy_pieces_to_be_removed = []

            if uc in list(enemy_position.values()):
                for enemy_piece in list(enemy_position.keys()):
                    if enemy_position[enemy_piece] == uc:
                        enemy_pieces_to_be_removed.append(enemy_piece)
                for rpiece in enemy_pieces_to_be_removed:
                    del pin_enemy_position[rpiece]
            pin_position_coordinates = list(pin_friendly_position.values())+list(pin_enemy_position.values())
            pin_enemy_scope = chessf.scope_counter(pin_enemy_position, pin_position_coordinates, anti_color)
            if pin_friendly_position[friendly_king] in pin_enemy_scope:
                self.turn -= 1
                return print(f"Is {color} getting outplayed? {color}\'s {piece_type} is pinned")

        capture_indicator = False
        en_passant_indicator = False
        if en_passant_potential:
            if uc == en_passant_move:
                en_passant_indicator = True
                capture_indicator = True
                for piece in list(enemy_position.keys()):
                    if enemy_position[piece] == lpawn_square:
                        if color == "White":
                            del self.black_position[piece]
                        else:
                            del self.white_position[piece]


        if uc in list(enemy_position.values()):
            capture_indicator = True
            for enemy_piece in list(enemy_position.keys()):
                if enemy_position[enemy_piece] == uc:
                    self.captured_pieces.append(enemy_piece)
                    if color == "White":
                        del self.black_position[enemy_piece]
                    if color == "Black":
                        del self.white_position[enemy_piece]

        if piece_type in ['O-O', 'O-O-O']:
            if color == "White" and piece_type == 'O-O':
                if self.castle_rights_dic['wK'] or self.castle_rights_dic['wR_2']:
                    return print("No castle rights")
                for square in [[6, 1], [7, 1]]:
                    if square in enemy_scope:
                        return print("Not allowed to castle through enemy scope")
                    if square in list(friendly_position.values()):
                        return print("Self destructing back rank?")
                # move valid
                friendly_position_updated = friendly_position
                friendly_position_updated['wK'] = [7, 1]
                friendly_position_updated['wR_2'] = [6, 1]
                self.castle_rights_dic['wK'] = True
                print(f"Move: {game_move}   White castles king side")
            if color == "White" and piece_type == 'O-O-O':
                if self.castle_rights_dic['wK'] or self.castle_rights_dic['wR_1']:
                    return print("No castle rights")
                for square in [[4, 1], [3, 1], [2, 1]]:
                    if square in enemy_scope:
                        return print("Not allowed to castle through enemy scope")
                    if square in list(friendly_position.values()):
                        return print("Self destructing back rank?")
                #move valid
                friendly_position_updated = friendly_position
                friendly_position_updated['wK'] = [3, 1]
                friendly_position_updated['wR_1'] = [4, 1]
                self.castle_rights_dic['wK'] = True
                print(f"Move: {game_move}   White castles queen side")
            if color == 'Black' and piece_type == 'O-O':
                if self.castle_rights_dic['bK'] or self.castle_rights_dic['bR_2']:
                    return print("No castle rights")
                for square in [[6, 8], [7, 8]]:
                    if square in enemy_scope:
                        return print("Not allowed to castle through enemy scope")
                    if square in list(friendly_position.values()):
                        return print("Self destructing back rank?")
                #move valid
                friendly_position_updated = friendly_position
                friendly_position_updated["bK"] = [7, 8]
                friendly_position_updated['bR_2'] = [6, 8]
                self.castle_rights_dic['bK'] = True
                print(f"Move: {game_move}   Black castles king side")
            if color == 'Black' and piece_type == 'O-O-O':
                if self.castle_rights_dic['bK'] or self.castle_rights_dic['bR_1']:
                    return print("No castle rights")
                for square in [[4, 8], [3, 8], [2, 8]]:
                    if square in enemy_scope:
                        return print("Not allowed to castle through enemy scope")
                    if square in list(friendly_position.values()):
                        return print("Self destructing back rank?")
                friendly_position_updated = friendly_position
                friendly_position_updated['bK'] = [3, 8]
                friendly_position_updated['bR_1'] = [4, 8]
                self.castle_rights_dic['bK'] = True
                print(f"Move: {game_move}   Black castles queen side")
            self.launched_pawn_tracker.append('none')
            # o_pc is assigned here to prevent errors in calling move_notary later on
            o_pc = 'none'

        # Code to be executed when move is valid
        if piece_type not in ['O-O', 'O-O-O']:
            print(f"Move: {game_move}   {color} moves {piece_type} to {destination}")
            friendly_position_updated = friendly_position
            friendly_position_updated[piece] = chessf.ugly_coordinator(destination)
        if color == "White":
            self.white_position = friendly_position_updated
        else:
            self.black_position = friendly_position_updated
        # Checkmate checker
        position_coordinates_updated = list(friendly_position_updated.values())+list(enemy_position.values())
        scope_list = chessf.scope_counter(friendly_position_updated, position_coordinates_updated, color)
        check_count = scope_list.count(enemy_position[enemy_king])
        enemy_king_saved = False
        check_mate_indicator = False
        if check_count > 0:
            king_moves = chessf.move_finder("king", chessf.pretty_coordinator(enemy_position[enemy_king]),
                                            position_coordinates_updated)
            valid_king_moves = king_moves
            king_moves_to_be_removed = []
            for king_move in king_moves:
                if king_move in scope_list or king_move in list(enemy_position.values()):
                    king_moves_to_be_removed.append(king_move)
            for rking_move in king_moves_to_be_removed:
                valid_king_moves.remove(rking_move)
            if not valid_king_moves:
                for enemy_piece in list(enemy_position.keys()):
                    if chessps.piece_type_dic[enemy_piece] == 'king':
                        continue
                    if enemy_king_saved:
                        break
                    iteration_piece_type = chessps.piece_type_dic[enemy_piece]
                    iteration_piece_moves = chessf.move_finder(iteration_piece_type,
                                                               chessf.pretty_coordinator(enemy_position[enemy_piece]),
                                                               position_coordinates_updated, anti_color)
                    for save in iteration_piece_moves:
                        if enemy_king_saved:
                            break
                        enemy_position_hypo = enemy_position
                        enemy_position_hypo[enemy_piece] = save
                        position_coordinates_hypo = list(friendly_position_updated.values()) + list(enemy_position_hypo.values())
                        scope_list_hypo = chessf.scope_counter(friendly_position_updated, position_coordinates_hypo, color)
                        if enemy_position_hypo[enemy_king] not in scope_list_hypo:
                            enemy_king_saved = True
                            break
            if not valid_king_moves and not enemy_king_saved:
                check_mate_indicator = True
                print(f"Checkmate! {color} won")
                self.game_status = f"{color} won"
        if check_count == 1 and self.game_status == "Ongoing":
            print("Check!")
        if check_count == 2 and self.game_status == "Ongoing":
            print("Double Check!")
        if check_count > 2 and self.game_status == "Ongoing":
            print("Check! Check! Check!")

        move_notation = chessps.move_notary(piece_type, capture_indicator, len(potential_pieces),
                                            o_pc, destination,
                                            check_count, check_mate_indicator, en_passant_indicator)
        self.game_moves_tracker.append(move_notation)
        if piece_type in ['O-O', 'O-O-O']:
            return

       #Some game stat trackers
        o_uc = chessf.ugly_coordinator(o_pc)
        if piece_type == 'pawn' and o_uc[1] -uc[1] in [-2, 2]:
            self.launched_pawn_tracker.append(uc)
        else:
            self.launched_pawn_tracker.append('none')

        for castle_right_piece in list(self.castle_rights_dic.keys()):
            if castle_right_piece == piece or castle_right_piece in self.captured_pieces:
                self.castle_rights_dic[castle_right_piece] = True


















