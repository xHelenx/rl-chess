import chess
import numpy as np
from ObservationSpaceModeller import ObservationSpaceModeller 

class ObservationSpacePositionPerPiece(ObservationSpaceModeller): 
    def __init__(self): 
        super() 
        self.obs_size = 64
        
        
    def get_observation_space(self, board):
        '''
            position of each agent, if agent is removed -> -1 
            
            everything + 6 
            'P': 1,     # White Pawn
            'p': -1,    # Black Pawn
            'N': 2,     # White Knight
            'n': -2,    # Black Knight
            'B': 3,     # White Bishop
            'b': -3,    # Black Bishop
            'R': 4,     # White Rook
            'r': -4,    # Black Rook
            'Q': 5,     # White Queen
            'q': -5,    # Black Queen
            'K': 6,     # White King
            'k': -6     # Black King
        
        '''
        int_board = [0] * 64
        for color in [chess.WHITE, chess.BLACK]: 
            for position in chess.scan_reversed(board.occupied_co[color]):  # Check if white
                int_board[position] = board.piece_type_at(position) + 6 
        return np.array(int_board).reshape(8,8,1)
    