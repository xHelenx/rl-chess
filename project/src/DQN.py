import numpy as np
from tensorflow import keras   
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Activation
from tensorflow.keras.optimizers import Adam



class DQN:
    """Deep Q-Network
    """
    def __init__(self, action_size:int, hidden_size=16, optimizer="Adam"):
        """Creates a Deep-Q-Network, that uses a 8x8 input state for predicting the action to be executed.

        Args:
            action_size (int): Amount of actions (output)
            hidden_size (int, optional): Number of neurons in hidden layer. Defaults to 16.
            optimizer (str, optional): Optimizer of NN. Defaults to "Adam".
        """
        self.action_size = action_size
        
        self.model = Sequential() 
        self.model.add(Conv2D(1, (2,2), activation='relu', input_shape=(8,8,1)))
        self.model.add(Conv2D(4, (2,2), activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(hidden_size, activation="relu"))
        self.model.add(Dense(self.action_size, activation="linear"))
        
        
    def __call__(self,state):
        """
        Network returns a probability of each action depending on input (state)
        Args:
            state: current input for network, here the state of the game
        

        Returns:
            list: probability per action
        """
        state = np.reshape(state, [1, 8, 8, 1])
        a = self.model(state)
        a = np.reshape(a,[self.action_size]) 
        return a