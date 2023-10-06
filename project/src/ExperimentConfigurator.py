import itertools
from Experiment import Experiment

class ExperimentConfigurator: 
    def __init__(self): 
        self.episodes = [10]
        self.hidden_size = [32]
        self.max_steps = [50]
        
        self.parameter = [self.episodes, self.hidden_size, self.max_steps]
        
    def createExperimentsGrid(self):
        '''
            Creates a List of Experiments to perform a grid search 
            of defined parameters  
        '''
        for i in itertools.product(*self.parameter): 
            self.list_of_experiments.append(Experiment(episodes=i[0], hidden_size=[1], max_steps=[2]))