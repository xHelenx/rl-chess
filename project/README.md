# Overview 

## Installation and Setup: Using a Virtual Environment
First, clone the repository and then navigate to the `src` folder. Here you find a makefile that creates a virtual environment for you and installs the required packages for the python project (3.19.13). You can run the makefile like this. Be aware, that this make file is written for windows.

    make venv 

If you use mac, run the following command instead 

    make venvMac

This way a new virtual environment will be created and all the requirements will be installed. Now activate the virtual environment

    .\venv\Scripts\activate
or using Mac 

    source venv/bin/activate

After the download it might be necessary to add stockfish to your environment variables. 

## Installation and Setup: Global Setup 
If you decide not use a virtual environment, you can also get the required packages by executing the following command in the `src` 
directory directly. 

    pip install -r requirements.txt 

----

For a quickstart, you can now open the `example_notebook.ipynb`. This is the best entry point to the project, as it goes over the content step by step and explains how everything works. 


Read the following section to get an overview over the different folder and files. 

## Directory Overview
In the project folder you can find two folders, `src` and `dataset`. 
In the dataset folder some example datasets can be located. 
The data is obtained from [here](https://chess-research-project.readthedocs.io/en/latest/), preprocessed and split into the four files. Each file contains either 1000, 5000, 10000 or 100000 games. Each game follows the algebraic notation. 

The `src` folder contains all the classes relevant for the project. Each class is documented. 

There are 4 jupyter notebooks. The one relevant to understand the project is `example_notebook.ipynb`, that explains how everything works and gives an example to get started with individual experiments. The other three notebooks `test_botstatistics.ipynb`, `test_CNNmodel.ipynb` and `test_errorplots.ipynb` have been used during the experimentation phase for the paper and show different statistics. This means you can look through the different results and test-analysis, but not execute the notebook yourself. The functions of the most relevant plots have been summarized in `plotting.py` to be reusable and the most relevant results are documented in the paper. 

All other classes are used in the background of the example-notebook. They can also be started using `main.py`, but 
it easier to look into the results using the notebook. 

    📦project
    ┣ 📂dataset
    ┃ ┣ 📜03_sorted_1000.txt
    ┃ ┣ 📜03_sorted_5000.txt
    ┃ ┣ 📜03_sorted_10000.txt
    ┃ ┣ 📜03_sorted_100000.txt
    ┣ 📂src
    ┃ ┣ 📜Agent.py
    ┃ ┣ 📜AgentCollection.py
    ┃ ┣ 📜ChessEnvironment.py
    ┃ ┣ 📜CNN.py
    ┃ ┣ 📜constants.py
    ┃ ┣ 📜DQN.py
    ┃ ┣ 📜example_notebook.ipynb
    ┃ ┣ 📜ExperimentConfigurator.py
    ┃ ┣ 📜Experiment.py
    ┃ ┣ 📜main.py
    ┃ ┣ 📜ObservationSpaceModeller.py
    ┃ ┣ 📜ObservationSpacePositionPerPiece.py
    ┃ ┣ 📜plotting.py
    ┃ ┣ 📜SampleConverter.py
    ┃ ┣ 📜test_errorplots.ipynb
    ┃ ┣ 📜test_CNNmodel_plots.ipynb
    ┃ ┗ 📜test_botstatistics.ipynb
    ┗ 📜README.md

