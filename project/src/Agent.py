import chess
from CNN import CNN
from constants import HIDDEN_SIZE


class Agent: 
    """
    The agent represents a single chess piece. It includes 
    the information about the chess piece as well as the 
    network and action spaces learned during the training. 
    """

    def __init__(self, color: bool, piece_type: chess.PieceType,
                 starting_position: chess.Square, rounds:int=0) -> None:
        """
        Initializes a single agent representing a chess piece. 

        Args:
            color (bool): color of chess piece [WHITE, BLACK]
            piece_type (chess.PieceType): type of chess piece [PAWN, QUEEN...]
            starting_position (chess.Square): starting position of agent [chess.A1...]
            rounds (int): amount of training rounds 
        """
        
        
        self.color = color 
        self.piece_type = piece_type 
        self.starting_position = starting_position 
        self.current_position = starting_position
        self.validSuggestions = rounds * [0]
        self.invalidSuggestions = rounds * [0]
        
        self.alive = True 
        self.action_space = [] 
        self.cnn = None 
        self.dataset = []
        self.trainAPF = []
        self.trainNet = []
        self.test = []
        
        ##for later coordination
        #self.q_net = None 
        #self.q_net_target = None 
            
    
    def reset_training(self, rounds:int): 
        """Removes learnings from the network and the collected statistics 

        Args:
            rounds (int): _description_
        """
        self.cnn = CNN(HIDDEN_SIZE, len(self.action_space)).model 
        self.validSuggestions = rounds * [0]
        self.invalidSuggestions = rounds * [0]
        
    #def set_suggestions_list(self,rounds:int): 
    #    self.validSuggestions = rounds * [0]
    #    self.invalidSuggestions = rounds * [0]