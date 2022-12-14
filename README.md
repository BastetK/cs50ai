I started from layer combination of one Convolutional layer, one Max-pooling layer and one hidden layer with dropout.
Next I consecuently tried to change parameters to choose what options gives the best result.

- Changing only number of nodes did not give much positive impact, but helped to add extra accuracy at last epochs
- bigger pool size for pooling layers is not working good with images of given size
- smaller size of filters for convolutional layers slightly increased performance

  Positive effects:

- Using combination of different activation functions
- Adding several convolution layers
