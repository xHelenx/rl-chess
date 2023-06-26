import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam



class DQN:
    def __init__(self, state_size:int, action_size:int, hidden_size=16, optimizer="Adam"):
        self.state_size = state_size
        self.action_size = action_size
        self.model = Sequential()
        self.model.add(Dense(hidden_size, activation="relu", input_dim=self.state_size))
        self.model.add(Dense(hidden_size, activation="relu"))
        self.model.add(Dense(self.action_size, activation="linear"))
        self.model.compile(loss="mse", optimizer=optimizer)
        
    def __call__(self,s):
        '''
        input: s = state 
        output: a = vector of probability per action
        '''
        s = np.reshape(s, [1, self.state_size])
        a = self.model.predict(s)
        a = np.reshape(a,[self.action_size])
        return a