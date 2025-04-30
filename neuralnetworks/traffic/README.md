# Traffic Sign Recognition

As part of this assignment, I initially started with one layer of Convolution and Pooling, followed up with a Dense Layer with 128 units. I didn't add a droput layer at first, when I trained the model, the accuracy was pretty high.

I also experimented with a second convolution and pooling layer and also added a dropout layer with a rate of 0.5. With the dropout, I noticed that the accuracy was lower in 10 epochs and it took longer to reach a high accuracy. I tried adding multiple convolution and pooling layers, but the results remained fairly the same.