import chess
import numpy as np
from ObservationSpaceModeller import ObservationSpaceModeller 

class ObservationSpacePositionPerPiece(ObservationSpaceModeller): 
    """An exemaplary implementation of the ObservationSpaceModeller. 

    """
    def __init__(self): 
        super() 
        self.obs_size = 64
        
        
    def get_observation_space(self, board):
        """Returns the current observations space from the board, modelled as an 8x8 matrix with the following values:
            
            position of each agent, if agent is removed -> -1 
            
            'P': 7,     # White Pawn
            'p': 5,    # Black Pawn
            'N': 8,     # White Knight
            'n': 4,    # Black Knight
            'B': 9,     # White Bishop
            'b': 3,    # Black Bishop
            'R': 10,     # White Rook
            'r': 2,    # Black Rook
            'Q': 11,     # White Queen
            'q': 1,    # Black Queen
            'K': 12,     # White King
            'k': 0     # Black King
            
        Args:
            board (chess.Board): current game setting

        Returns:
            np.array: matrix reprentation of current state 
        """
        int_board = [0] * 64
        for color in [chess.WHITE, chess.BLACK]: 
            for position in chess.scan_reversed(board.occupied_co[color]):  # Check if white
                int_board[position] = board.piece_type_at(position) + 6 
        return np.array(int_board).reshape(8,8,1)
    