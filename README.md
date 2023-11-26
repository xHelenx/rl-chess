# Deep Reinforcement Learning for Multi-Agent Systems on the Example of Chess 
---
Author: Helen Haase

Supervisor: Prof. Dr. Thomas Clemen

---
## Project Overview 
Cooperative multi-agent learning represents a formidable challenge within the realm of artificial intelligence research. This challenge becomes particularly evident in scenarios with high-dimensional environments where agents possess diverse capabilities and must adhere to specific rules while collaboratively learning from experts. Imitation learning emerges as a promising solution, allowing agents to acquire policies through the study of expert demonstrations in the absence of direct reward signals. 

This project aims to train a heterogenous group of agents to learn the individual action spaces as well as a starting behavior to cooperatively learn to together. The example of chess is chosen, as the action spaces varies and even agents with the same action space may behave differently depending on their position in the game and therefore the primary goal. The chess game is modelled using markov games. 

The following poster gives a short overview of the different steps. It is to say that before the group-decision making is being modelled, the individual agents have to be trained, which is the focus in this project. The idea relates to real world problems, where for example multiple robots cooperatively manufacture a product. Instead of teaching each robot very specific which actions it can perform and in which sequence the tasks should be executed by the different agents, it would simplify the process, if agents learned their capabilities themselves and also collaboratively decide which tasks is performed when and by whom. 

![DRL for MAS](readme_figs/Helen_Haase_FW2_Poster.png)

## Usage of the repository
To support the usage of the repository, an example notebook *example_notebook.ipynb*  is prepared and can be located in the src/ folder. Below the folder structure is shown. A few example datasets are added for testing. 

    
    📦project
    ┣ 📂dataset
    ┃ ┣ 📜03_sorted_100.txt
    ┃ ┣ 📜03_sorted_1000.txt
    ┃ ┣ 📜03_sorted_5000.txt
    ┃ ┣ 📜03_sorted_10000.txt
    ┗ 📂src
    ┃ ┣ 📜example_notebook.ipynb
    ┃ ┣ 📜main.py
    ┃ ┣ 📜constants.py
    ┃ ┣ 📜DQN.py
    ┃ ┣ 📜plotting.py
    ┃ ┣ 📜ObservationSpaceModeller.py
    ┃ ┣ 📜... 
    📦poster
    ┣ 📜Helen_Haase_FW2_Poster.pdf
    ┗ 📜...
  
