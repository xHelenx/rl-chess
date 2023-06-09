import chess 
#King - K 
#Queen - Q
#Rook - R (Turm)
#Bishop - B (Läufer)
#Knight - N (Springer)
#Pawn - none
#captured - x 
#captured by pawn -> specifiy which -> dx.. (von d Reihe)
#wenn uneindeutig welches der e.g. Springer - noch bs 
#wenn sogar gleicher bs -> stattdessen zahl 
#check - +
#checkmate - #

#white wins - 1-0, black wins .- 0-1, draw - 1/2-1/2

#castling kindside/castling queenside 

#<id>.<type><opt:spec><opt:x/+/#><endpos>
#
#<white>-<black>
ID_POS = 0
ID_SAMPLES = 1 

class SampleConverter:
    def __init__(self) -> None:
        black_pieces = {
            chess.ROOK:{    chess.A8: [chess.A8, []],  #Rook R
                            chess.H8: [chess.H8, []]}, #Rook L
            chess.KNIGHT:{  chess.B8: [chess.B8, []],  #Knight R
                            chess.G8: [chess.G8, []]}, #Knight L 
            chess.BISHOP:{  chess.C8: [chess.C8, []],  #Bishop L
                            chess.F8: [chess.F8, []]}, #Bishop R
            chess.KING:{    chess.D8: [chess.D8, []]}, #King  
            chess.QUEEN:{   chess.E8: [chess.E8, []]}, #Queen
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
            chess.KING:{    chess.D1: [chess.D1, []]}, #King  
            chess.QUEEN:{   chess.E1: [chess.E1, []]},  #Queen
            chess.PAWN:{    chess.A2: [chess.A2, []],  #Pawn 1
                            chess.B2: [chess.B2, []],  #Pawn 2
                            chess.C2: [chess.C2, []],  #Pawn 3
                            chess.D2: [chess.D2, []],  #Pawn 4
                            chess.E2: [chess.E2, []],  #Pawn 5
                            chess.F2: [chess.F7, []],  #Pawn 6 
                            chess.G2: [chess.G2, []],  #Pawn 7
                            chess.H2: [chess.H2, []]}}  #Pawn 8
        self.dataset = {chess.WHITE : white_pieces, chess.BLACK: black_pieces}
        #print(self.dataset)
        self.board = None 
        
    def read_dataset(self, file): 
        with open(file, "rt") as myfile: 
            for line in myfile:  
                self.board = chess.Board()
                if not "O-" in line: 
                    line = line.partition("### ")[2]
                    line = line.split(" ")
                    line = [item for item in line if "." in item]
                    print(line)
                    for current_move in line:     
                        print("MOVE:", current_move, "MOVE END")
                        moved_piece = self.get_moved_piece(current_move) 
                        print(moved_piece)
                    break
            
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
    
    def get_moved_piece(self, move:str): 
        is_white = self.is_white(move)
        move = move.partition(".")[2]
        moved_piece = None
        piece_type = self.get_piece_type(move[0])
        dest = ""
        
        for piece in self.dataset[is_white]: 
            for original_startpos in self.dataset[is_white][piece_type]:
                start = self.dataset[is_white][piece_type][original_startpos][0]
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
                    dest =  move[1]+move[3]
                # on same letter, so use number e.g. (N1d2)
                elif len(move) >= 4 and move[0].isupper() and move[1].isnumeric() and \
                move[2].islower() and move[3].isnumeric():
                    dest = move[2] + move[3]
                            
                possible_move = chess.square_name(start) + dest
                legal_moves = list(self.board.legal_moves) # Move.from_uci('g1h3')
                print(chess.Move.from_uci(possible_move))
                print(legal_moves)
                print(chess.Move.from_uci(possible_move) in legal_moves)
                print(chess.piece_symbol(piece_type))
                print(piece)
                #print(chess.piece_symbol(piece))
                if chess.Move.from_uci(possible_move) in legal_moves and piece_type == piece:
                    moved_piece = self.dataset[is_white][piece_type][original_startpos][0]
                    return moved_piece 
        raise ValueError("No piece performed move")
            
    
    '''
    import chess 
#King - K 
#Queen - Q
#Rook - R (Turm)
#Bishop - B (Läufer)
#Knight - N (Springer)
#Pawn - none
#captured - x 
#captured by pawn -> specifiy which -> dx.. (von d Reihe)
#wenn uneindeutig welches der e.g. Springer - noch bs 
#wenn sogar gleicher bs -> stattdessen zahl 
#check - +
#checkmate - #

#white wins - 1-0, black wins .- 0-1, draw - 1/2-1/2

#castling kindside/castling queenside 

#<id>.<type><opt:spec><opt:x/+/#><endpos>
#
#<white>-<black>
ID_POS = 0
ID_SAMPLES = 1 

class SampleConverter:
    def __init__(self) -> None:
        black_pieces = {
            chess.ROOK:{    chess.A8: [chess.A8, []],  #Rook R
                            chess.H8: [chess.H8, []]}, #Rook L
            chess.KNIGHT:{  chess.B8: [chess.B8, []],  #Knight R
                            chess.G8: [chess.G8, []]}, #Knight L 
            chess.BISHOP:{  chess.C8: [chess.C8, []],  #Bishop L
                            chess.F8: [chess.F8, []]}, #Bishop R
            chess.KING:{    chess.D8: [chess.D8, []]}, #King  
            chess.QUEEN:{   chess.E8: [chess.E8, []]}, #Queen
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
            chess.KING:{    chess.D1: [chess.D1, []]}, #King  
            chess.QUEEN:{   chess.E1: [chess.E1, []]},  #Queen
            chess.PAWN:{    chess.A2: [chess.A2, []],  #Pawn 1
                            chess.B2: [chess.B2, []],  #Pawn 2
                            chess.C2: [chess.C2, []],  #Pawn 3
                            chess.D2: [chess.D2, []],  #Pawn 4
                            chess.E2: [chess.E2, []],  #Pawn 5
                            chess.F2: [chess.F7, []],  #Pawn 6 
                            chess.G2: [chess.G2, []],  #Pawn 7
                            chess.H2: [chess.H2, []]}}  #Pawn 8
        
        self.dataset = {chess.WHITE : white_pieces, chess.BLACK: black_pieces}
        #print(self.dataset)
        
    def read_dataset(self, file): 
        with open(file, "rt") as myfile: 
            for line in myfile: 
                #TODO start a new game here 
                #keep track of the moves and options 
                board = chess.Board()
                line = line.partition("### ")[2]
                line = line.split(" ")
                line = [item for item in line if "." in item]
                for current_move in line:     
                    print("MOVE:", current_move, "MOVE END")
                    possible_pieces = []
                    
                    #TODO: Rochade (könig o. Dame) erstmal ignorieren
                    if not "O" in current_move: 
                        possible_pieces = self.get_possible_pieces(current_move)
                    print("POSSIBLE OPTIONS", possible_pieces)
                break
            
    def is_white(self, move):
        return "W" in move.partition(".")[0]
    
    def get_possible_pieces(self, move): 
        is_white = self.is_white(move)
        move = move.partition(".")[2]
        piece_indicator = move[0]
        possible_pieces = []
        if is_white:
            if piece_indicator == "R": #Turm/Rook
                if not move[2].isnumeric():
                    chess.square_name(self.dataset[is_white][chess.ROOK][i])[0] 
                possible_pieces += [chess.A1]
                possible_pieces += [chess.H1]
            elif piece_indicator == "N": #Springer/Knight
                possible_pieces += [chess.B1]
                possible_pieces += [chess.G1]
            elif piece_indicator == "B": #Läufer/Bishop
                possible_pieces += [chess.C1]
                possible_pieces += [chess.F1]
            elif piece_indicator == "K": #König
                possible_pieces += [chess.D1]
            elif piece_indicator == "Q": #Queen
                possible_pieces += [chess.E1]
                
            elif piece_indicator.islower() and move[1].isnumeric():
                possible_pieces += [chess.parse_square(str(piece_indicator) + "2")]
            elif piece_indicator.islower() and move[1] == "x":
                for item in self.dataset[is_white][chess.PAWN]:
                    print("ITEM1", chess.square_name(item))
                    if chess.square_name(item)[0] == piece_indicator: 
                        possible_pieces += [item]
                        print(chess.square_name(item))
            else: 
                possible_pieces += [None]
        else: 
            if piece_indicator == "R": #Turm/Rook
                possible_pieces += [chess.A8]
                possible_pieces += [chess.H8]
            elif piece_indicator == "N": #Springer/Knight
                possible_pieces += [chess.B8]
                possible_pieces += [chess.G8]
            elif piece_indicator == "B": #Läufer/Bishop
                possible_pieces += [chess.C8]
                possible_pieces += [chess.F8]
            elif piece_indicator == "K": #König
                possible_pieces += [chess.D8]
            elif piece_indicator == "Q": #Queen
                possible_pieces += [chess.E8]
            elif piece_indicator.islower() and move[1].isnumeric():
                possible_pieces += [chess.parse_square(str(piece_indicator) + "7")]
            elif piece_indicator.islower() and move[1] == "x":
                for item in self.dataset[is_white][chess.PAWN]:
                    if chess.square_name(item)[0] == piece_indicator: 
                        possible_pieces += [item]
            else: 
                possible_pieces += [None]
        return possible_pieces
    
    '''