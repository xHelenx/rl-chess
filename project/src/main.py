
import random

import chess
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from Agent import Agent
from AgentCollection import AgentCollection
from ChessEnvironment import ChessEnvironment
from constants import *
from Experiment import Experiment
from ObservationSpacePositionPerPiece import ObservationSpacePositionPerPiece
from plotting import absolute_to_relative_movement, plot_frequency_distribution
from SampleConverter import SampleConverter
from tqdm import tqdm

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
def transform_dataset(agent:Agent, dataset:list):
    obsModeller = ObservationSpacePositionPerPiece()
    y = []
    X = []
    for [state, action, _ ] in dataset:
            #PREPARING DATASET FOR BATCH TRAINING
            board = chess.Board(state) #fen converts board into game state 
            #get legal move as relative vector        
            valid_actions = []
            probabilities = []
            
            for move in board.legal_moves: 
                #identify all moves that the current agent could do by look at the current position of the agent 
                rel_move = absolute_to_relative_movement(move.from_square, move.to_square)
                if move.from_square == action[0] and rel_move in agent.action_space : 
                    valid_actions += [rel_move]
                    probabilities += agent.hist[7+rel_move[0],7+rel_move[1]]
            if valid_actions != []: 

                #obtain target value using APF
                random_value = random.randint(0,sum(probabilities))
                summed_probs  = 0
                i = 0 
                for i in range(len(probabilities)):
                    summed_probs += probabilities[i]
                    if summed_probs > random_value:
                        break 
            
                action = valid_actions[i] 
                y += [agent.action_space.index(action)]
                X += [(obsModeller.get_observation_space(board))]
    return (np.array(X),np.array(y))

    
def plot_metrics(history):
    # Plot training & validation loss values
    fig = plt.figure(figsize=(12,4))  # Adjust the figure size as needed
    plt.subplot(1, 2, 1)  # Create the first subplot

    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Validation'], loc='upper right')
    #for step in range(0,EPISODES_CNN*ROUNDS, BATCH_SIZE):  # Starting from 5, up to 20, with a step of 5
    ##    plt.axvline(x=step, color='gray', linestyle='--', alpha=0.5)


    # Plot training & validation accuracy values
    plt.subplot(1, 2, 2)  # Create the second subplot
    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(['Train', 'Validation'], loc='lower right')
    
    #for step in range(0,EPISODES_CNN*ROUNDS, BATCH_SIZE):  # Starting from 5, up to 20, with a step of 5
    ##    plt.axvline(x=step, color='gray', linestyle='--', alpha=0.5)

    plt.show()
    
def plot_histograms(agent:Agent): 
    ## PLOT OLD 
    
    fig = plt.figure()
    fig.set_size_inches(12,12)
    ax = fig.add_subplot(1,2,1, projection='3d')
    
    x = []
    y = []
    for [_,(start,dest),_] in agent.trainAPF: 
        (start,dest) = absolute_to_relative_movement(start,dest)
        x += [start]
        y += [dest]
        
    
    hist, xedges, yedges = np.histogram2d(x, y, bins=15, range=[[-7, 7], [-7, 7]])
    # Construct arrays for the anchor positions 
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    # Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.7 * np.ones_like(zpos) #Breite der Säulen 
    dz = hist.ravel()

    #ax.elev = 45 #height camera  
    #ax.azim = 90 #rotation y axis
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    #print(sum(sum(hist)))
    #ax.set_title(chess.piece_name(PIECE))
    ax.set_xlabel("Relative movement x-axis")
    ax.set_ylabel("Relative movement y-axis")
    ax.set_zlabel("Frequence")
  
    
    #####PLOT NEW 
    (X_test, _) = transform_dataset(agent,agent.test)
    predictions = agent.cnn.predict(X_test)
    predictions = tf.argmax(predictions, axis=-1)
    x_move = []
    y_move = []

    ax = fig.add_subplot(1,2,2, projection='3d')
    for pred in predictions.numpy(): 
        x_move += [agent.action_space[pred][0]]
        y_move += [agent.action_space[pred][1]]
    hist, xedges, yedges = np.histogram2d(x_move, y_move, bins=15, range=[[-7, 7], [-7, 7]])
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    # Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.7 * np.ones_like(zpos) #Breite der Säulen 
    dz = hist.ravel() #ax.elev = 45 #height camera  
    #ax.azim = 90 #rotation y axis
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    #print(sum(sum(hist)))
    #ax.set_title(chess.piece_name(PIECE))
    ax.set_xlabel("Relative movement x-axis")
    ax.set_ylabel("Relative movement y-axis")
    ax.set_zlabel("Frequence")
    
    plt.show()

   

def train_net(agent:Agent): 
    # Initialize an empty dictionary to store aggregated history data
    aggregated_history = {
    'loss': [],
    'val_loss': [],
    'accuracy': [],
    'val_accuracy': [] }

    for _ in range(ROUNDS): 
        (X_train, y_train) = transform_dataset(agent,agent.trainNet)
        (X_test, y_test) = transform_dataset(agent,agent.test)
        #print(agent.cnn.predict(tf.expand_dims(obsModeller.get_observation_space(board),axis=0)))
        history = agent.cnn.fit(X_train,y_train, epochs=EPISODES_CNN, validation_data=(X_test, y_test))
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
    
    history = train_net(agentCollection.getAgentAtStartingPosition(chess.H8))
    plot_metrics(history)
    plot_histograms(agentCollection.getAgentAtStartingPosition(chess.H8))   
    
    #print("--> Starting cooperative learning phase <-- ")
    #train_coop() 
    print("--> Training completed <-- ")
    
        
