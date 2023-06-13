import chess 

class SampleConverter:
    def __init__(self) -> None:
        black_pieces = {
            chess.ROOK:{    chess.A8: [chess.A8, []],  #Rook R
                            chess.H8: [chess.H8, []]}, #Rook L
            chess.KNIGHT:{  chess.B8: [chess.B8, []],  #Knight R
                            chess.G8: [chess.G8, []]}, #Knight L 
            chess.BISHOP:{  chess.C8: [chess.C8, []],  #Bishop L
                            chess.F8: [chess.F8, []]}, #Bishop R
            chess.KING:{    chess.E8: [chess.E8, []]}, #King  
            chess.QUEEN:{   chess.D8: [chess.D8, []]}, #Queen
            chess.PAWN:{    chess.A7: [chess.A7, []],  #Pawn 1
                            chess.B7: [chess.B7, []],  #Pawn 2
                            chess.C7: [chess.C7, []],  #Pawn 3
                            chess.D7: [chess.D7, []],  #Pawn 4
                            chess.E7: [chess.E7, []],  #Pawn 5
                            chess.F7: [chess.F7, []],  #Pawn 6 
                            chess.G7: [chess.G7, []],  #Pawn 7
                            chess.H7: [chess.H7, []]}}  #Pawn 8
        white_pieces = {
            chess.ROOK:{    chess.A1: [chess.A1, []],  #Rook R
                            chess.H1: [chess.H1, []]}, #Rook L
            chess.KNIGHT:{  chess.B1: [chess.B1, []],  #Knight R
                            chess.G1: [chess.G1, []]}, #Knight L 
            chess.BISHOP:{  chess.C1: [chess.C1, []],  #Bishop L
                            chess.F1: [chess.F1, []]}, #Bishop R
            chess.KING:{    chess.E1: [chess.E1, []]}, #King  
            chess.QUEEN:{   chess.D1: [chess.D1, []]},  #Queen
            chess.PAWN:{    chess.A2: [chess.A2, []],  #Pawn 1
                            chess.B2: [chess.B2, []],  #Pawn 2
                            chess.C2: [chess.C2, []],  #Pawn 3
                            chess.D2: [chess.D2, []],  #Pawn 4
                            chess.E2: [chess.E2, []],  #Pawn 5
                            chess.F2: [chess.F7, []],  #Pawn 6 
                            chess.G2: [chess.G2, []],  #Pawn 7
                            chess.H2: [chess.H2, []]}}  #Pawn 8
        self.dataset = {chess.WHITE : white_pieces, chess.BLACK: black_pieces}
        self.board = None 
        self.total_games = 0
    def reset_starting_positions(self): 
        for is_white in [True, False]: 
            for piece_type in [chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.KING, chess.QUEEN, chess.PAWN]: 
                for original_startpos in self.dataset[is_white][piece_type]: 
                    self.dataset[is_white][piece_type][original_startpos][0] = original_startpos
        
    def read_dataset(self, file, visualize=False): 
        with open(file, "rt") as myfile: 
            for game in myfile:  
                self.board = chess.Board()
                game = game.partition("### ")[2]
                if not "O-" in game: 
                    is_last_move = False 
                    self.total_games += 1 
                    self.board.reset()
                    self.reset_starting_positions() 
                    #print(self.dataset)
                    #print("-------------")
                    #print("NEXT GAME: ")
                    #display(self.board)
                    game = game.split(" ")
                    game = [item for item in game if "." in item]
                    #print(game)
                    for current_move in game:    
                        #print("MOVE:", current_move)
                        #calculate which piece moved from where to where     
                        (start, is_white, piece_type, original_start) = self.get_moving_piece(current_move) 
                        if start == None: 
                            print(game)
                            break 
                        #get current move, dest and what piece is at that pos 
                        current_move = current_move.partition(".")[2]
                        dest = self.get_destination_pos(current_move)
                        piece_at_dest = self.board.piece_type_at(chess.parse_square(dest))
                        
                        move = start+dest
                        
                        #check if king was captured to end game 
                        if piece_at_dest != None and piece_at_dest == chess.KING: 
                            is_last_move = True 
                            
                        state = self.board.fen() 
                        #perform move on board + update dataset
                        board_move = chess.Move.from_uci(start + dest)
                        self.board.push(board_move)
                        next_state = self.board.fen() 
                        
                        #TODO: add other ways to end a game 
                        #if self.board.is_checkmate or self.board.is_stalemate() or self.board.is_insufficient_material(): 
                        #    is_last_move = True 
                        
                        #display(self.board)
                        self.dataset[is_white][piece_type][original_start][0] = chess.parse_square(dest)
                        self.add_sample(is_white, piece_type, original_start,start+dest,state,next_state)
                           
                        if is_last_move: 
                            break  
            
    def get_action(self,move:str) -> tuple:        
        x_steps = ord(move[2]) - ord(move[0])
        y_steps = ord(move[3]) - ord(move[1])
        return (x_steps, y_steps)     
        
        
    def add_sample(self, is_white, piece_type, original_start,move,state,next_state): 
        
        action = self.get_action(move)
        self.dataset[is_white][piece_type][original_start][1] += [(action, state, next_state)]
    
    def is_white(self, move:str):
        return "W" in move.partition(".")[0]
    
    def get_piece_type(self, step:str):  #partioned move -> step is second part
        if step[0].isupper(): 
            if step[0] == "B": 
                return chess.BISHOP
            elif step[0] == "K": 
                return chess.KING
            elif step[0] == "R": 
                return chess.ROOK
            elif step[0] == "N":
                return chess.KNIGHT
            elif step[0] == "Q": 
                return chess.QUEEN
        else: #is there another condition? 
            return chess.PAWN 
    
    def get_destination_pos(self, move:str) -> str: 
        '''
        move = str hinter dem Punkt 
        '''
        dest = ""
        
        #kleiner BS - e.g. (e2)
        if len(move) >= 2 and move[0].islower() and move[1].isnumeric():
            dest =  move[0]+move[1]            
        #groß BS - skip e.g. (Be2)
        elif move[0].isupper() and move[1].islower() and move[2].isnumeric():
            dest =  move[1]+move[2]
        #x skip e.g. (Bxe2)
        elif len(move) >= 4 and move[0].isupper() and move[1] == "x" and \
            move[2].islower() and move[3].isnumeric(): 
            dest =  move[2]+move[3]
        #bs vor x e.g. (gxe2)
        elif len(move) >= 4 and move[0].islower() and move[1] == "x" and \
            move[2].islower() and move[3].isnumeric(): 
            dest =  move[2]+move[3]
        #bs vor x e.g. (Bgxe2)
        elif len(move) >= 5 and move[0].isupper() and move[1].islower() and \
        move[2] == "x" and move[3].islower() and move[4].isnumeric(): 
            dest =  move[3]+move[4]
        #two options of pieces, use letter e.g. (Rfd8)
        elif len(move) >= 4 and move[0].isupper() and move[1].islower() and \
        move[2].islower() and move[3].isnumeric(): 
            dest =  move[2]+move[3]
        # on same letter, so use number e.g. (N1d2)
        elif len(move) >= 4 and move[0].isupper() and move[1].isnumeric() and \
        move[2].islower() and move[3].isnumeric():
            dest = move[2] + move[3]
        return dest 
    
    
    def is_ambiguous_piece(self, move:str):
        '''
        checks if the position could be reacehd my multiple pieces of the same piece type 
        '''
        #bs vor x e.g. (Bgxe2)/ Bge2
        if len(move) >= 4 and move[0].isupper() and move[1].islower() and  move[1] != "x" and \
        move[2].islower(): 
            return (True, move[1])
        #bs vor x e.g. (gxe2)
        elif len(move) >= 3 and move[0].islower() and move[1].islower(): 
            return (True,move[0])
        #e.g. Rac8 (beide Türme könnten zu c8 sich bewegen)
        elif len(move) >= 4 and move[0].isupper() and move[1].islower() and \
        move[1] != "x" and move[2].islower() and move[3].isnumeric(): 
            return(True, move[1])
        #TODO beide gleichen bs an position stattdessen dann ziffer 
        else: 
            return (False, None)
        
    def get_moving_piece(self, move:str) -> tuple: 
        is_white = self.is_white(move)
        move = move.partition(".")[2]
        piece_type = self.get_piece_type(move[0])
        dest = ""

        #for piece in self.dataset[is_white]: 
        for original_startpos in self.dataset[is_white][piece_type]:
            start = chess.square_name(self.dataset[is_white][piece_type][original_startpos][0])
            dest = self.get_destination_pos(move)  
            (is_ambigious, x_val) = self.is_ambiguous_piece(move)
            #print(is_ambigious,x_val)
            #print("Kombo:", start, dest )
            if start != dest: 
                possible_move = start + dest
                legal_moves = list(self.board.pseudo_legal_moves) # Move.from_uci('g1h3')
                #print(chess.Move.from_uci(possible_move))
                #print(legal_moves)
                #print(chess.piece_name(piece_type))
                #print(start, dest)
                
                if is_ambigious:  
                    
                    if possible_move[0] == x_val and chess.Move.from_uci(possible_move) in legal_moves: 
                        return (start,is_white, piece_type,original_startpos) 
                    
                elif chess.Move.from_uci(possible_move) in legal_moves:
                    return (start,is_white, piece_type,original_startpos)
             
        print(is_white, move)
        print(chess.Move.from_uci(possible_move))
        print(legal_moves)
        print(chess.piece_name(piece_type))
        print(start, dest)     
        display(self.board)          
        return (None,None,None,None)
    
    
        
            
