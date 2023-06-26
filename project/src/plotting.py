import matplotlib.pyplot as plt
import numpy as np
from SampleConverter import SampleConverter

def plot_frequency_distribution(dataset, colors:list, piece, starting_positions:list): 
    '''
    colors = [WHITE] oder [WHITE,BLACK]
    '''

    fig = plt.figure()
    fig.set_size_inches(12,12)
    ax = fig.add_subplot(projection='3d')

    x = []
    y = []

    for is_white in colors:
        for i in starting_positions:
            if i in dataset[is_white][piece]:
                for j in range(0,len(dataset[is_white][piece][i][1])):
                    x+= [dataset[is_white][piece][i][1][j][0][0]]
                    y+= [dataset[is_white][piece][i][1][j][0][1]]   
    hist, xedges, yedges = np.histogram2d(x, y, bins=14, range=[[-7, 7], [-7, 7]])

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