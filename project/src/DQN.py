import numpy as np
from tensorflow import keras   
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Activation
from tensorflow.keras.optimizers import Adam



class DQN:
    def __init__(self, state_size:int, action_size:int, hidden_size=16, optimizer="Adam"):
        #TODO state_size not used, maybe remove or inherit 
        self.state_size = state_size
        self.action_size = action_size
        
        
        #TODO random values for network -> change to global and local version, by adding more images (one per local + 1 global)
        self.model = Sequential() 
        self.model.add(Conv2D(1, (2,2), activation='relu', input_shape=(8,8,1)))
        self.model.add(Conv2D(4, (2,2), activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(hidden_size, activation="relu"))
        self.model.add(Dense(self.action_size, activation="linear"))
        
        #self.model = Sequential()
        #self.model.add(Dense(hidden_size, activation="relu", input_dim=self.state_size))
        #self.model.add(Dense(hidden_size, activation="relu"))
        #self.model.add(Dense(self.action_size, activation="linear"))
        #self.model.compile(loss="mse", optimizer=optimizer)
        
        
    def __call__(self,s):
        '''
        input: s = state 
        output: a = vector of probability per action
        '''
        #self.model.summary() 
        
        s = np.reshape(s, [1, 8, 8, 1])
        a = self.model(s)
        a = np.reshape(a,[self.action_size]) #check action size?! 
        return a