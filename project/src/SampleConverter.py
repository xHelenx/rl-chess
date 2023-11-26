import chess
import chess.svg
from AgentCollection import AgentCollection 

class SampleConverter:
    """The SampleConverter is used to preprocess the data and create 
    the samples for later training.
    """
    
    def __init__(self, agentCollection:AgentCollection) -> None:
        """Initializes the SampleConverter

        Args:
            agentCollection (AgentCollection): all agents considered in later training
        """
        self.agentCollection = agentCollection
        self.board = None 
        self.total_games = 0
        self.current_game = 0
    
        
    def read_dataset(self, file:str): 
        """Reads and processes the dataset. Therefore each agents receives all samples of their 
        actions in the form [state, (x,y), next_state]

        Args:
            file:str: File containing the games, following the algebraic notation for chess
        """
        with open(file, "rt") as myfile: 
            for game in myfile:  
                self.current_game += 1 
                self.board = chess.Board()
                game = game.partition("### ")[2]
                if not "O-" in game: 
                    is_last_move = False 
                    self.total_games += 1 
                    self.board.reset()
                    self.agentCollection.reset_agents_position()
                    game = game.split(" ")
                    game = [item for item in game if "." in item]
                    for current_move in game:  
                        #calculate which piece moved from where to where     
                        agent = self.get_moving_piece(current_move) 
                        
                        if agent == None : 
                            #print(self.current_game)
                            break
                        else: 
                            start = chess.square_name(agent.current_position)
                            
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
                            
                            self.agentCollection.update_agents_pos((chess.parse_square(start), chess.parse_square(dest))) 
                            board_move = chess.Move.from_uci(move)
                            self.board.push(board_move)
                            
                            next_state = self.board.fen() 
                                
                            
                            #TODO: add other ways to end a game - currently not necessary
                            #if self.board.is_checkmate or self.board.is_stalemate() or self.board.is_insufficient_material(): 
                            #    is_last_move = True 
                            
                            agent.dataset += [[state, (chess.parse_square(start), chess.parse_square(dest)), next_state]]
                           
                            if is_last_move: 
                                break  
                        
            
    #def get_action(self,move:str) -> tuple:    
    #        
    #    x_steps = ord(move[2]) - ord(move[0])
    #    y_steps = ord(move[3]) - ord(move[1])
    #    return (x_steps, y_steps)     
        
        
    def is_white(self, move:str) -> bool:
        """Returns, whether the current move is performed by the white team

        Args:
            move (str): Move in standard algebraic notation

        Returns:
            bool:  whether the current move is performed by the white team
        """
        return "W" in move.partition(".")[0]
    
    def get_piece_type(self, step:str) -> chess.PieceType:  #partioned move -> step is second part
        """Returns the piece type of the current step

        Args:
            step (str): step representing the information about which piece is moved in the current move (e.g. Be4 is step, W12.Be4 is move)

        Returns:
            chess.PieceType: piece type that moved in the current step
        """
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
    
    def get_destination_pos(self, step:str) -> str: 
        """Calculates the destination position based on the step in standard algebraic notation

        Args:
            step (str): string of movement e.g. Be2, gxe2

        Returns:
            str: string of destination e.g. A2
        """
        dest = ""
        
        #kleiner BS - e.g. (e2)
        if len(step) >= 2 and step[0].islower() and step[1].isnumeric():
            dest =  step[0]+step[1]            
        #groß BS - skip e.g. (Be2)
        elif step[0].isupper() and step[1].islower() and step[2].isnumeric():
            dest =  step[1]+step[2]
        #x skip e.g. (Bxe2)
        elif len(step) >= 4 and step[0].isupper() and step[1] == "x" and \
            step[2].islower() and step[3].isnumeric(): 
            dest =  step[2]+step[3]
        #bs vor x e.g. (gxe2)
        elif len(step) >= 4 and step[0].islower() and step[1] == "x" and \
            step[2].islower() and step[3].isnumeric(): 
            dest =  step[2]+step[3]
        #bs vor x e.g. (Bgxe2)
        elif len(step) >= 5 and step[0].isupper() and step[1].islower() and \
        step[2] == "x" and step[3].islower() and step[4].isnumeric(): 
            dest =  step[3]+step[4]
        #two options of pieces, use letter e.g. (Rfd8)
        elif len(step) >= 4 and step[0].isupper() and step[1].islower() and \
        step[2].islower() and step[3].isnumeric(): 
            dest =  step[2]+step[3]
        # on same letter, so use number e.g. (N1d2)
        elif len(step) >= 4 and step[0].isupper() and step[1].isnumeric() and \
        step[2].islower() and step[3].isnumeric():
            dest = step[2] + step[3]
        return dest 
    
    
    def is_ambiguous_piece(self, step:str) -> list:
        """Checks, whether the position could be reached my multiple pieces of the same piece type 

        Args:
            step (str):  string of movement e.g. Be2, gxe2

        Returns:
            list[bool,string]: bool indicates whether piece is ambigious, string shows the possible movement e.g. "a1a2"
        """
        
        #bs vor x e.g. (Bgxe2)/ Bge2
        if len(step) >= 4 and step[0].isupper() and step[1].islower() and  step[1] != "x" and \
        step[2].islower(): 
            return (True, step[1])
        #bs vor x e.g. (gxe2)
        elif len(step) >= 3 and step[0].islower() and step[1].islower(): 
            return (True,step[0])
        #e.g. Rac8 (beide Türme könnten zu c8 sich bewegen)
        elif len(step) >= 4 and step[0].isupper() and step[1].islower() and \
        step[1] != "x" and step[2].islower() and step[3].isnumeric(): 
            return(True, step[1])
        #TODO beide gleichen bs an position stattdessen dann ziffer 
        else: 
            return (False, None)
        
    def get_moving_piece(self, step:str) -> tuple: 
        """Calculates which piece was moved depending on the current move in standard algebraic notation

        Args:
            step (str): string of movement e.g. Be2, gxe2

        Returns:
            Agent: moved agent using the current step
        """

        is_white = self.is_white(step)
        step = step.partition(".")[2]
        piece_type = self.get_piece_type(step[0])
        dest = ""
        
        for agent in self.agentCollection.getAgentsAlive(is_white): 
            start = chess.square_name(agent.current_position)
            dest = self.get_destination_pos(step)
            (is_ambiguous, x_val) = self.is_ambiguous_piece(step)
             
            if start != dest and is_white == agent.color and piece_type == agent.piece_type: 
                possible_move = start + dest
                legal_moves = list(self.board.legal_moves) # Move.from_uci('g1h3')
                if is_ambiguous:  
                    if possible_move[0] == x_val and chess.Move.from_uci(possible_move) in legal_moves: 
                        return agent 
                    
                elif len(possible_move) == 4 and chess.Move.from_uci(possible_move) in legal_moves:
                    return agent 
        #boardsvg = chess.svg.board(board=self.board, fill={chess.parse_square(start):"#d4d669", chess.parse_square(dest):"#69d695"})
        #outputfile = open('image.svg', "w")
        #outputfile.write(boardsvg)
        #outputfile.close()                 
        return None

       
        
            
