import chess
from CNN import CNN
from constants import HIDDEN_SIZE


class Agent: 

    def __init__(self, color: bool, piece_type: chess.PieceType,
                 starting_position: chess.Square) -> None:
        
        self.color = color 
        self.piece_type = piece_type 
        self.starting_position = starting_position 
        self.current_position = starting_position
        
        self.alive = True 
        
        self.dataset = []
        self.trainAPF = []
        self.trainNet = []
        self.test = []
        self.q_net = None 
        self.q_net_target = None 
        self.action_space = [] 
        self.cnn = None 
        self.validSuggestions = []
        self.invalidSuggestions = []
            
        
    def reset_training(self, rounds:int): 
        self.cnn = CNN(HIDDEN_SIZE, len(self.action_space)).model 
        self.validSuggestions = rounds * [0]
        self.invalidSuggestions = rounds * [0]
        
    def set_suggestions_list(self,rounds:int): 
        self.validSuggestions = rounds * [0]
        self.invalidSuggestions = rounds * [0]