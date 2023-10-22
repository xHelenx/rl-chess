import random
import chess
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from ObservationSpacePositionPerPiece import ObservationSpacePositionPerPiece
from Agent import Agent
from AgentCollection import AgentCollection

def is_action_valid(agent:Agent, action, state:str, prediction:int): 
    board = chess.Board(state)
    pred_move =  agent.action_space[prediction]
    dest_pos = action[0] + pred_move[0] + 8 * pred_move[1]

    for move in board.legal_moves: 
        if action[0] == move.from_square and dest_pos == move.to_square: 
            return True 
    return False 
    
def plot_APF(agents:list):
#(dataset, colors:list, piece, starting_positions:list): 
    '''
    colors = [WHITE] oder [WHITE,BLACK]
    '''

    fig = plt.figure()
    fig.set_size_inches(12,12)
    ax = fig.add_subplot(projection='3d')

    x = []
    y = []
    
    for agent in agents: 
        print(agent.trainAPF[0])
        for [_,(start,dest),_] in agent.trainAPF: 
            (start,dest) = absolute_to_relative_movement(start,dest)
            x += [start]
            y += [dest]
           
    
    hist, xedges, yedges = np.histogram2d(x, y, bins=15, range=[[-7, 7], [-7, 7]])
    print(hist)
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
    plt.show()
    
def absolute_to_relative_movement(start,dest): 
    ''' integer to relative '''
    start = chess.square_name(start)
    dest = chess.square_name(dest)
    
    x = ord(dest[0]) - ord(start[0])
    y = ord(dest[1]) - ord(start[1])
    
    return (x,y)

def relative_to_absolute_movement(x,y, current_position): 
    return (current_position, current_position + x + 8*y)
    
  
def transform_dataset(agent:Agent, dataset:list):
    obsModeller = ObservationSpacePositionPerPiece()
    y = []
    X = []
    states = []
    actions = []
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
                
                actions += [action] 
                action = valid_actions[i] 
                y += [agent.action_space.index(action)]
                X += [(obsModeller.get_observation_space(board))]
                states += [state]
                
    return (np.array(X),np.array(y), states, actions)

    
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
    (X_test, _, states, actions) = transform_dataset(agent,agent.test)
    predictions = agent.cnn.predict(X_test)
    predictions = tf.argmax(predictions, axis=-1)
    
    validPrediction = 0
    invalidPrediction = 0
    for i in range(len(X_test)):
        is_valid = is_action_valid(agent, actions[i], states[i], predictions[i])
        if is_valid:
            validPrediction += 1 
        else:
            invalidPrediction += 1
    totalSuggestions = validPrediction + invalidPrediction
    print(str(agent.starting_position), " made ", str(validPrediction), " correct out of ", totalSuggestions, "total suggestions")
    
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
    

def plot_errors(agentCollection:AgentCollection): 
    for agent in agentCollection.allAgents:
        plt.plot(relations = [x / y for x, y in zip(agent.validSuggestions, agent.invalidSuggestions)])

    # Customize the plot (labels, title, legend, etc. as needed)
    plt.xlabel('Time Steps')
    plt.ylabel('Error Percentage')
    plt.title('Error Percentage Over Time for Multiple Agents')
    plt.legend(['Agent 1', 'Agent 2', ...])  # Add legend labels for each agent

    # Show the plot or save it to a file
    plt.show()
    
def plot_errors_individually(agents: list[Agent]): 
    plot_x = []
    plot_y = []
    for agent in agents:    
        x = []
        y = []
        for i in range(len(agent.validSuggestions)): 
            x += [i+1]
            if agent.invalidSuggestions[i] > 0 or agent.validSuggestions[i] > 0:
                y += [agent.invalidSuggestions[i] / (agent.invalidSuggestions[i] + agent.validSuggestions[i])]
            else: 
                y += [None] #we dont take value, because the agent didnt take a decision in this game 
            x_filtered = [x_val for x_val, y_val in zip(x, y) if y_val is not None]
            y_filtered = [y_val for y_val in y if y_val is not None]    
            plot_x += [x_filtered]
            plot_y += [y_filtered]
    for x,y in zip(plot_x, plot_y):
        plt.plot(x,y)
        
    # Customize the plot (labels, title, legend, etc. as needed)
    plt.xlabel('Training Rounds')
    plt.ylabel('Error Percentage')
    #plt.legend(agent_names)  # Add legend labels for each agent
    plt.xticks(range(1,len(agent.validSuggestions)+1, 1))
    # Show the plot or save it to a file
    plt.show()

def plot_errors_grouped(agents: list[Agent]): 
    x = []
    y = []
    for i in range(len(agents[0].validSuggestions)): 
        summed_valid = 0 
        summed_invalid = 0 
        for agent in agents:
            if agent.invalidSuggestions[i] > 0 or agent.validSuggestions[i] > 0:
                summed_valid += agent.validSuggestions[i]
                summed_invalid += agent.invalidSuggestions[i]
        if summed_valid > 0: 
            x += [i+1]
            y += [summed_invalid/(summed_valid+summed_invalid)]

    plt.plot(x,y)
    # Customize the plot (labels, title, legend, etc. as needed)
    plt.xlabel('Training Rounds')
    plt.ylabel('Error Percentage')
    #plt.xticks(range(1,len(y)+1, 1))
    # Show the plot or save it to a file
    plt.show()

    
def plot_errors_scatter(agents: list[Agent]): 
    x = []
    y = []
    for agent in agents:
        for i in range(len(agent.validSuggestions)): 
            x  += [i+1]
            y  += [agent.invalidSuggestions[i]]
            
    plt.scatter(x, y, marker='o', color='blue', alpha=0.5)      
    #plt.xticks(range(1,len(agent.validSuggestions)+1, 1)) 
    # Customize the plot (labels, title, legend, etc. as needed)
    plt.xlabel('Training Rounds')
    plt.ylabel('invalid Suggestions')

    # Show the plot or save it to a file
    plt.show()