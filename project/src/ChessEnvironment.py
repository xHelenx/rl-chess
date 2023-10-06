import random

import chess
import sys
import chess.svg
import constants
import numpy as np
from Agent import Agent
from AgentCollection import AgentCollection
from CNN import CNN 
from DQN import DQN
from Experiment import Experiment
from ObservationSpaceModeller import ObservationSpaceModeller
from ObservationSpacePositionPerPiece import ObservationSpacePositionPerPiece
import time
from plotting import absolute_to_relative_movement

NO_ACTION = (0,0)

class ChessEnvironment: 
    def __init__(self, agents:AgentCollection, min_appear:float, experiment_conf:Experiment) -> None:
        ''' 
        
        '''
        self.agentCollection = agents
        self.board = chess.Board()    
        self.min_appear = min_appear
        self.current_step = 0
        self.experiment_conf = experiment_conf        
        
        self.observation_space_modeller: ObservationSpaceModeller = ObservationSpacePositionPerPiece()

        #setup action spaces, q-net and q-net-targets
        for agent in self.agentCollection.allAgents: 
            [agent.hist, agent.action_space] = self.__get_action_space(agent)
            q_net = DQN(self.observation_space_modeller.obs_size,len(agent.action_space))
            agent.q_net = q_net
            q_net_target = DQN(self.observation_space_modeller.obs_size,len(agent.action_space))
            q_net_target.model.set_weights(q_net.model.get_weights())
            agent.q_net_target = q_net_target
            agent.cnn = CNN(constants.HIDDEN_SIZE, len(agent.action_space)).model        
       
    def __get_action_space(self, agent):
        x = []
        y = []
        for [_,(start,dest),_] in agent.trainAPF: 
            (start,dest) = absolute_to_relative_movement(start,dest)
            x += [start]
            y += [dest]
         
        #convert all x,y tuple to histogram and take all actions above min_appear into action space
        hist, _, _ = np.histogram2d(x, y, bins=15, range=[[-7, 7], [-7, 7]])
        
        action_space = []
        #print(hist)
        for x in range(0,len(hist)): 
            for y in range(0,len(hist[0])): 
                if hist[x][y] >= self.min_appear:
                    action_space += [(-7+x,-7+y)] #(-3,-3) als Verschiebung des Nullpunkts
        return [hist,action_space]
 
    #def update_agents_pos(self, board, action): 
    #    '''
    #    updates position in agent data structure
    #    ''' 
    #    #check if other agent has been captured in destination and note that 
    #    piece = self.board.piece_at(action[1])
        #if removed set pos to -1, and set alive to false
    #    if piece != None: 
    #        agent = self.agentCollection.getAgentAtPosition(action[1])
    #        agent.current_position = -1 
    #        agent.alive = False       
        
        #update position of piece, that is moved 
        #piece = chess.Board().piece_at(action[0])
    #    agent = self.agentCollection.getAgentAtPosition(action[0])
    #    agent.current_position = action[1] 
        
        
    def reset(self): 
        #reset position of agents
        for agent in self.agentCollection.allAgents: 
            agent.alive = True 
            agent.current_position = agent.starting_position
        
        #reset game     
        self.board.reset()
        #reset number of steps, used to determine whos turn it is
        self.current_step = 0
      
    def _get_possible_actions_for_agent(self, moves:list, position:int): 
        '''        
        returns list possible actions at current positions, 
            action = [(from_square, to_square)...] #(int,int)
        '''
        actions = []
        for move in moves: 
            if position == move.from_square:  
                actions += [(move.from_square, move.to_square)]
        return actions 
    
    def step(self, epsilon) -> tuple: 
        done = False 
        info = ""
        self.current_step += 1  
        if self.current_step > self.experiment_conf.max_steps:
            done = True 
            next_state = self.observation_space_modeller.get_observation_space(self.board) 
            reward = self.get_reward(NO_ACTION, done) 
            return (next_state, reward, done, info) 

            
        #determine whos turn it is
        is_white = self.current_step % 2 == 1  #white turn      
        
        #get all possible agents (alive)
        alive_agents = self.agentCollection.getAgentsAlive(is_white)
        action_preselection = []
        action = None 
        state =  self.observation_space_modeller.get_observation_space(self.board)  
        
        for agent in alive_agents: 
            
            #generate one possible action per agent 
            #mask all invalid actions 
            possible_actions = self._get_possible_actions_for_agent(self.board.legal_moves, agent.current_position) 
            if len(possible_actions) > 0:  
                random_value = np.random.rand() #0-1 
                if epsilon > random_value: #random action
                    action_preselection += [(random.choice(possible_actions))]
                else: 
                    foundValidAction = False
                    output = agent.q_net(state).copy()
                    while not foundValidAction and not max(output) == float("-inf"): 
                        #chess rules may allow one piece to move, but the action space does not include the action
                        action_id = np.argmax(output)
                        rel_action = agent.action_space[action_id]
                        print(rel_action, agent.current_position)
                        action = self.relative_move_to_absolute(rel_action, agent.current_position)
                        print(action)
                        if action in possible_actions: 
                            action_preselection += [action]
                            foundValidAction = True 
                        else: 
                            output[action_id] = float("-inf") #mask impossible action
                            
        #possible that a move is in list of possible action but not in action space - unlucky obut ok ?
        
        #at least one piece has to be moveable
        if len(action_preselection) > 0: 
            #select a global action    
            random_value = np.random.rand() #0-1 
            if epsilon > random_value: #random action
                action = random.choice(action_preselection)
            else:
                #TODO: add global dqn?
                action = random.choice(action_preselection)
                #TODO statistic which piece is preferred?

            #perform move on board + update dataset
            #print(self.agentCollection.getAgentAtPosition(action[0]).color, chess.square_name(action[0]),chess.square_name(action[1]))
            self.agentsCollection.update_agents_pos(action) 
            board_move = chess.Move.from_uci(chess.square_name(action[0])+chess.square_name(action[1]))
            self.board.push(board_move)
        else: 
            done = True #none of the alive pieces is able to move -> lost game 
            
        #determine state, reward, done flag
        next_state = self.observation_space_modeller.get_observation_space(self.board) 
        #TODO define more termination criteria
        if self.is_king_dead(not is_white):
            done = True      
        reward = self.get_reward(action, done) 
        
        boardsvg = chess.svg.board(board=self.board, fill={action[0]:"#d4d669", action[1]:"#69d695"})
        outputfile = open('image.svg', "w")
        outputfile.write(boardsvg)
        outputfile.close()
        time.sleep(2)
        
        return (next_state, reward, done, info) 

    def relative_move_to_absolute(self, action, starting_position): 
        '''
            converts move from numerical to string version
        '''
        end_position = starting_position + action[0] + 8 * action[1]
        return (starting_position, end_position)
        
    def is_king_dead(self,color):         
        return not self.agentCollection.getKing(color).alive
    
    def get_reward(self, action, done): 
        if self.current_step > self.experiment_conf.max_steps: 
            return 0 
        elif done: 
            return 1 #current team won so give reward, TODO: how negative reward to other team? both teams should get update when game ends but not when other person moves??
        else: 
            return 0 
    