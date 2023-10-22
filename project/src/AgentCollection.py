from Agent import Agent
import chess 
class AgentCollection: 
    def __init__(self) -> None:
        self.allAgents = []
        
    def addAgent(self, agent:Agent): 
        self.allAgents += [agent]
        
    def removeAgent(self, agent:Agent): 
        self.allAgents -= [agent]
    
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
    
    def getMovableAgents(self,board): 
        current_pos = [x.from_square for x in board.legal_moves] #get all starting pos
        #print(current_pos)
        result = list(dict.fromkeys(current_pos))
        #print(result)
        agents = []
        for pos in result: 
            agents += [self.getAgentAtPosition(pos)]
        return agents 
    
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
            
    def update_agents_pos(self, action, is_white=True, board:chess.Board=None): 
        '''
        updates position in agent data structure
        action = (abs_int, abs_int)
        ''' 
        #check if other agent has been captured in destination and note that 
        agent= self.getAgentAtPosition(action[1])
        if agent != None:
            agent.current_position = -1 
            agent.alive = False       
        #update position of piece, that is moved 
        agent = self.getAgentAtPosition(action[0])
        if agent == None: 
            print("action: ", action,  "options ", board.legal_moves )                         
            boardsvg = chess.svg.board(board=board)
            outputfile = open('image.svg', "w")
            outputfile.write(boardsvg)
            outputfile.close()
            print(is_white)
            print(action)
        agent.current_position = action[1]     
        
    def reset_agents_position(self): 
        for agent in self.allAgents: 
            agent.current_position = agent.starting_position
            agent.alive = True