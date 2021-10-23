import nltk
import numpy as np
#nltk.download('punkt') --package with pre train tokenize
from nltk.stem.porter import PorterStemmer

#creating the stemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    
    """
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog =   [ 0,      1,     0,    1,     0,      0,      0]

    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32) #creates an array with the same lenght of the all_words but with zeros and then 
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0 #if the word is in the tokenized_sentence the bag take a 1 in the index(idx)

    return bag


