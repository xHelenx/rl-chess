import chess
import matplotlib.pyplot as plt
import numpy as np
from SampleConverter import SampleConverter

def plot_frequency_distribution(agents:list):
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
  