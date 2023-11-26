class   Experiment: 
    """This class offers the setup of experiments. 
    """
    def __init__(self, episodes,hidden_size, max_steps) -> None:
        
        self.hidden_size = hidden_size
        self.episodes = episodes