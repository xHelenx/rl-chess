class   Experiment: 
    def __init__(self, episodes,hidden_size, max_steps) -> None:
        
        self.hidden_size = hidden_size
        self.episodes = episodes
        self.max_steps = max_steps