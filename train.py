import json
from re import A
from torch._C import TracingState

from torch.autograd import backward
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)


all_words = [] #all words for training data

tags = [] #collecting different patterns and which diffente texts they have

xy = [] #will both hold patterns and texts


for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)

    #Looping over all differents patterns
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w) #extend because 'w' is an array and we don't wanna put an array of array
        xy.append((w, tag)) #know pattern and corresponding tag/text


ignore_words = ['?', '!', '.', ','] #exclude punctuation characters
all_words = [stem(w) for w in all_words if w not in ignore_words] #stems and exclude the ignore_words
all_words = sorted(set(all_words)) #sorting words and for unique words and kinda remove duplicates elements
tags = sorted(set(tags)) #unique labels


X_train = [] #bag of words
y_train = [] #tags/associated numbers for each tag

for (pattern_sentece, tag) in xy:
    
    bag = bag_of_words(pattern_sentece, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) #CrossEntropyLoss

#Converting to numpy array 
X_train = np.array(X_train) #Training data
y_train = np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    #dataset[idx] --for later access to dataset via index
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


#HyperParameters = Used to control the learning process
batch_size = 8
hidden_size = 8 #you can change if you want
output_size = len(tags) #number of different classes or text(tags) we have
input_size = len(X_train[0]) #number of the lenght of which bag of words that we created. The bag of words has the same length of the all words array so you can use any one of them to set the lenght of the input size
learning_rate = 0.001
num_epochs = 1000 #try differents ones


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0) #windows users can get an error if you set  the num_works = 2, so putting = 0 resolves that


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

#loss and optimizer
criterion = nn.CrossEntropyLoss() #training pipeline
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        #labels = labels.to(device) this gives a Traceback error so we need to cast the data to Long as in labels = labels.to(dtype=torch.long)
        labels = labels.to(dtype=torch.long)

        #forwards
        outputs = model(words)
        loss = criterion(outputs, labels)

        #backward and optimizer step
        optimizer.zero_grad() #empty the grand first
        loss.backward() #calculate the back propagation
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}') #prints every 100 steps

print(f'final loss, loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size" : input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth" 
torch.save(data, FILE)


print(f'Training complete. File saved to {FILE}')