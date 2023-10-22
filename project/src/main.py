
import random

import chess
import matplotlib.pyplot as plt
from Agent import Agent
from AgentCollection import AgentCollection
from ChessEnvironment import ChessEnvironment
from constants import *
from Experiment import Experiment
from plotting import plot_errors, plot_errors_scatter, plot_histograms, plot_metrics, transform_dataset
from SampleConverter import SampleConverter
from tqdm import tqdm
from stockfish import Stockfish #add to python env variables

import matplotlib.pyplot as plt

def linear_eps_decay(i, num_eps, start=1, stop=0): 
    '''
        Linearily decline epsilon from start to stop
    '''
    return start - (i-1) * ((start - stop) / num_eps)
    
def train_coop(): 
    #TODO rewards for both teams individually? 
    
    total_steps = []
    total_rewards = []
    for ep in tqdm(range(1, experiment.episodes)):
        env.reset()
        done = False 
        while not done: 
            #update epsilon
            #one epsilon value for all agents and all have same random value? Or different? no 
            epsilon = linear_eps_decay(ep, experiment.episodes, EPSILON_START,EPSILON_STOP)
            #let agents perform a step and get update 
            (_, reward, done, _) = env.step(epsilon) 
            if done:
                total_rewards += [reward]
                total_steps += [env.current_step]           
                #TODO: update networks, local and (wenn implementiert) global 
                
    plt.plot(total_rewards)
    plt.plot(total_steps)
    plt.show()

'''
def batch_generator(X, y, batch_size):
    X = np.array(X)
    y = np.array(y)
    num_samples = len(X)
    
    while True:
        indices = np.arange(num_samples)
        np.random.shuffle(indices)
        for i in range(0, num_samples, batch_size):
            batch_indices = indices[i:i+batch_size]
            batch_X = X[batch_indices]
            batch_y = y[batch_indices]
            yield batch_X, batch_y
   ''' 
   


def train_net(agent:Agent, episodes_cnn): 
    # Initialize an empty dictionary to store aggregated history data
    aggregated_history = {
    'loss': [],
    'val_loss': [],
    'accuracy': [],
    'val_accuracy': [] }
  
    (X_train, y_train,_,_) = transform_dataset(agent,agent.trainNet)
    (X_test, y_test,_,_) = transform_dataset(agent,agent.test)
    #print(agent.cnn.predict(tf.expand_dims(obsModeller.get_observation_space(board),axis=0)))
    history = agent.cnn.fit(X_train,y_train, epochs=episodes_cnn, validation_data=(X_test, y_test), verbose=0)
    aggregated_history['loss'].extend(history.history['loss'])
    aggregated_history['val_loss'].extend(history.history['val_loss'])
    aggregated_history['accuracy'].extend(history.history['accuracy'])
    aggregated_history['val_accuracy'].extend(history.history['val_accuracy'])
    
    return aggregated_history


        #add X and targets value to list 
        #X_train += [obsModeller.get_observation_space(board)]
        #y_targets += [target]
    
    
    #train_data_generator = batch_generator(X_train,y_targets, BATCH_SIZE)
    # Use fit_generator to train the model
    #agent.cnn.fit_generator(generator=train_data_generator,
    #                    steps_per_epoch=len(X_train) // BATCH_SIZE,
    #                    epochs=EPISODES_CNN)
    

    #def evaluate_net(agent:Agent): 
    #    (X_test, y_test) = transform_dataset(agent.test)
    #    test_loss, test_accuracy = agent.cnn.evaluate(X_test, y_test)
    #    #print(agent.cnn.predict(tf.expand_dims(obsModeller.get_observation_space(board),axis=0)))
    #    agent.cnn.fit(np.array(X_train),np.array(y_train), epochs=EPISODES_CNN)
  

if __name__ == "__main__":
    
    agentCollection = AgentCollection()        
    agentCollection.addAgent(Agent(chess.WHITE, chess.ROOK, chess.A1)) #Rook R
    agentCollection.addAgent(Agent(chess.WHITE, chess.ROOK, chess.H1)) #Rook L
    agentCollection.addAgent(Agent(chess.WHITE, chess.KNIGHT, chess.B1))  #Knight R
    agentCollection.addAgent(Agent(chess.WHITE, chess.KNIGHT, chess.G1)) #Knight L 
    agentCollection.addAgent(Agent(chess.WHITE, chess.BISHOP, chess.C1))  #Bishop L
    agentCollection.addAgent(Agent(chess.WHITE, chess.BISHOP, chess.F1)) #Bishop R
    agentCollection.addAgent(Agent(chess.WHITE, chess.KING, chess.E1)) #King  
    agentCollection.addAgent(Agent(chess.WHITE, chess.QUEEN, chess.D1)) #Queen
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.A2))  #Pawn 1
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.B2))  #Pawn 2
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.C2))  #Pawn 3
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.D2))  #Pawn 4
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.E2))  #Pawn 5
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.F2))  #Pawn 6 
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.G2))  #Pawn 7
    agentCollection.addAgent(Agent(chess.WHITE, chess.PAWN, chess.H2)) #Pawn 8       
    
    agentCollection.addAgent(Agent(chess.BLACK, chess.ROOK, chess.A8))  #Rook R
    agentCollection.addAgent(Agent(chess.BLACK, chess.ROOK, chess.H8))  #Rook L
    agentCollection.addAgent(Agent(chess.BLACK, chess.KNIGHT, chess.B8)) #Knight R
    agentCollection.addAgent(Agent(chess.BLACK, chess.KNIGHT, chess.G8)) #Knight L 
    agentCollection.addAgent(Agent(chess.BLACK, chess.BISHOP, chess.C8)) #Bishop L
    agentCollection.addAgent(Agent(chess.BLACK, chess.BISHOP, chess.F8)) #Bishop R
    agentCollection.addAgent(Agent(chess.BLACK, chess.KING, chess.E8)) #King  
    agentCollection.addAgent(Agent(chess.BLACK, chess.QUEEN, chess.D8)) #Queen
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.A7)) #Pawn 1
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.B7)) #Pawn 2
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.C7)) #Pawn 3
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.D7)) #Pawn 4
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.E7)) #Pawn 5
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.F7)) #Pawn 6 
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.G7)) #Pawn 7
    agentCollection.addAgent(Agent(chess.BLACK, chess.PAWN, chess.H7)) #Pawn 8
        
    
    sampleConv = SampleConverter(agentCollection) 
    print("--> Starting to read dataset <-- ")
    sampleConv.read_dataset(PATH + FILE )    
    print("--> Read and learned from APF " + str(sampleConv.total_games) + " games <-- ")

    
    experiment = Experiment( episodes=EPISODES_COOP,hidden_size=HIDDEN_SIZE, max_steps=MAX_STEPS)
    print("--> Setting up ChessEnvironment <-- ")
    
    for agent in agentCollection.allAgents: 
        random.shuffle(agent.dataset)
        i = int(len(agent.dataset)/3)
        agent.trainAPF = agent.dataset[:i]
        agent.trainNet = agent.dataset[i:2*i]
        agent.test = agent.dataset[2*i:3*i]
        agent.dataset = [] #free space 
         
    #plot_frequency_distribution([agentCollection.getAgentAtStartingPosition(chess.B1)])
    
    env = ChessEnvironment(agentCollection, min_appear=1, experiment_conf=experiment)
    print("--> Finished setting up ChessEnvironment <-- ")
    
    print("--> Starting to transfer APF to CNN model <-- ")
    
    stockfish=Stockfish("stockfish-windows-x86-64-modern")
    stockfish.set_depth(10)
    stockfish.set_skill_level(5)
    white_agents = agentCollection.getAgentsByColor(True)
    ####TODO: atm only train white team
    for i in range(0,ROUNDS):
        for agent in white_agents: 
            print(agent.starting_position)
            train_net(agent, EPISODES_CNN)
        #env.play_coop(i)
        env.play_against_bot(i, stockfish)
        print("Round ", str(i), " completed")
    
    #plot_metrics(history)
    #plot_histograms(agentCollection.getAgentAtStartingPosition(chess.H8))   
    #print("--> Starting cooperative learning phase <-- ")
    #train_coop() 
    print("--> Training completed <-- ")
    plot_errors(white_agents)
    plot_errors_scatter(white_agents)
    print("--> Play Botgame <-- ")
   
    
    
        
