import math

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential


class CNN: 
    """Convolutional Neuronal Network
    """

    def __init__(self, hidden_size:int, output_size:int) -> None:
        """Creates a Convolutional Neuronal Network

        Args:
            hidden_size (int): Amount of neurons in hidden layer
            output_size (int): Amount of outputs
        """
        # Create a Sequential model
        self.model = Sequential()
    
        # Add convolutional layers
        self.model = Sequential() 
        self.model.add(Conv2D(1, (2,2), activation='relu', input_shape=(8,8,1)))
        self.model.add(MaxPooling2D((2, 2)))

        self.model.add(Conv2D(4, (2,2), activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(hidden_size, activation="relu"))
        self.model.add(Dense(output_size, activation="linear"))
        # Compile the model
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

        # Display the model summary
        #self.model.summary()  


#def loss_proximity(y_target, y_pred):
#    return math.exp((y_target[0] - y_pred[0]) + (y_target[1] - y_pred[1]),2)