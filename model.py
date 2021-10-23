import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    #Feed Foward Neural Net which gets the bag of words, one layer fully connected which contains the number of different patterns as the input (input_size), then 2 hidden layers (hidden_size) and the output size must be the number of different classes (num_classes) and finally applying the "softmax" we get probability for each classes 
    
    #input_size and num_classes must be fixed, but you can change the hidden_size with you want 
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU() #activation function for in between

    def forward(self, x):
        out = self.l1(x) 
        out = self.relu(out) 
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        #no activation (relu) and no softmax because we applied the entropyloss that have this already set
        return out

