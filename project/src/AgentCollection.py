from Agent import Agent
import chess 
class AgentCollection: 
    """
    The AgentCollection is the data structure for all the agents that 
    are trained. It offers the functionality of obtaining different agents 
    depending on specific properties.
    """
    
    def __init__(self) -> None:
        """
        Sets up the AgentCollection. This is used as the datastructure 
        for all agents. This way they can be retrieved and manipulated depending 
        on different information like color or type 
        
        """
        self.allAgents = []
        
    def addAgent(self, agent:Agent): 
        """Adds an agent to the collection

        Args:
            agent (Agent): agent to be added
        """
        self.allAgents += [agent]
        
    def removeAgent(self, agent:Agent): 
        """removes an agent from the collection

        Args:
            agent (Agent): agent to be removed
        """
        self.allAgents -= [agent]
    
    def getAgentsByColor(self, color:bool) -> list[Agent]: 
        """Obtains all agent of a specific color

        Args:
            color (bool): color to filter agents by [WHITE=true,BLACK=false]

        Returns:
            list[Agent]: all agents of the specified color
        """
        filteredAgents = []
        for agent in self.allAgents: 
            if agent.color == color: 
                filteredAgents += [agent]
        return filteredAgents
    
    def getAgentsAlive(self, color:bool) -> list[Agent]: 
        """Returns all agents of a specific color, that are still part 
        of the game 

        Args:
            color (bool): color to filter agents by [WHITE=true,BLACK=false]

        Returns:
            list[Agent]: all alive agents of the specified color
        """
        filteredAgents = []
        for agent in self.allAgents: 
            if agent.color == color and agent.alive: 
                filteredAgents += [agent]
        return filteredAgents  
    
    def getMovableAgents(self,board:chess.Board) -> list[Agent]: 
        """Returns all agents, that have to option to move (according 
        to standard chess rules) depending on the current board setting

        Args:
            board (chess.Board): current chess setup

        Returns:
            list[Agent]: all agents, that can move
        """
        current_pos = [x.from_square for x in board.legal_moves] #get all starting pos
        #print(current_pos)
        result = list(dict.fromkeys(current_pos))
        #print(result)
        agents = []
        for pos in result: 
            agents += [self.getAgentAtPosition(pos)]
        return agents 
    
    def getAgentAtPosition(self, current_position:chess.Square) -> Agent: 
        """Returns Agent at a specific position, defined through the square (e.g. 0 -> A1)

        Args:
            current_position (chess.Square): Square to obtain agent from

        Returns:
            Agent: returns agent, that occupies square currently, else none
        """
        for agent in self.allAgents: 
            if agent.current_position == current_position: 
                return agent    
        return None
    
    def getAgentAtStartingPosition(self, starting_position:chess.Square) -> Agent: 
        """Returns agent with a specific starting positions, this resembles 
        the unique identifier of each agent

        Args:
            starting_position (chess.Square):  Starting square to obtain agent from

        Returns:
            Agent: Agent, that starts at the starting position, else none 
        """
        for agent in self.allAgents: 
            if agent.starting_position == starting_position: 
                return agent        
        return None
       
    #def getAgent(self, color:bool, piece_type:chess.PieceType, current_position: chess.Square) -> Agent: 
    #
    #    for agent in self.allAgents: 
    #        if agent.color == color and agent.piece_type == piece_type and \
    #        agent.current_position == current_position: 
    #            return agent 
            
    def getKing(self, color:bool) -> Agent: 
        """Returns king of the specified color

        Args:
            color (bool): color to obtain the king from

        Returns:
            Agent: King, of the asked color
        """
        for agent in self.allAgents: 
            if agent.color == color and agent.piece_type == chess.KING: 
                return agent 
            
    def update_agents_pos(self, action): 
        """ Updates the agents current position in the internal data structure

        Args:
            action (_type_): chosen action, encoded as (abs_int, abs_int)
        """
        #check if other agent has been captured in destination and note that 
        agent= self.getAgentAtPosition(action[1])
        if agent != None:
            agent.current_position = -1 
            agent.alive = False       
        #update position of piece, that is moved 
        agent = self.getAgentAtPosition(action[0])
        agent.current_position = action[1]     
        
    def reset_agents_position(self): 
        """Resets the agents position to its starting positions and 
        sets it back to being alive 
        """
        for agent in self.allAgents: 
            agent.current_position = agent.starting_position
            agent.alive = True