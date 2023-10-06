from Agent import Agent
import chess 
class AgentCollection: 
    def __init__(self) -> None:
        self.allAgents = []
        
    def addAgent(self, agent:Agent): 
        self.allAgents += [agent]
    
    def getAgentsByColor(self, color:bool): 
        filteredAgents = []
        for agent in self.allAgents: 
            if agent.color == color: 
                filteredAgents += [agent]
        return filteredAgents
    
    def getAgentsAlive(self, color): 
        filteredAgents = []
        for agent in self.allAgents: 
            if agent.color == color and agent.alive: 
                filteredAgents += [agent]
        return filteredAgents  
    
    def getAgentAtPosition(self, current_position:chess.Square): 
        for agent in self.allAgents: 
            if agent.current_position == current_position: 
                return agent    
        return None
    
    def getAgentAtStartingPosition(self, starting_position:chess.Square): 
        for agent in self.allAgents: 
            if agent.starting_position == starting_position: 
                return agent        
        return None
       
    def getAgent(self, color:bool, piece_type:chess.PieceType, current_position: chess.Square): 
        for agent in self.allAgents: 
            if agent.color == color and agent.piece_type == piece_type and \
            agent.current_position == current_position: 
                return agent 
            
    def getKing(self, color): 
        for agent in self.allAgents: 
            if agent.color == color and agent.piece_type == chess.KING: 
                return agent 
            
    def update_agents_pos(self, action): 
        '''
        updates position in agent data structure
        ''' 
        #check if other agent has been captured in destination and note that 
        agent= self.getAgentAtPosition(action[1])
        if agent != None:
            agent.current_position = -1 
            agent.alive = False       
            
        #update position of piece, that is moved 
        agent = self.getAgentAtPosition(action[0])
        agent.current_position = action[1]     
        
    def reset_agents_position(self): 
        for agent in self.allAgents: 
            agent.current_position = agent.starting_position
            agent.alive = True