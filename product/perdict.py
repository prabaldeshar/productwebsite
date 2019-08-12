numDimensions = 50
maxSeqLength = 250
batchSize = 32
lstmUnits = 128
numClasses = 2
iterations = 130000

import numpy as np
import pandas as pd
import string
import re
import csv
import tensorflow as tf
from functools import partial
import nltk
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import tensorflow as tf


wordsList = np.load('D:/Sentiment/Glove/wordsList.npy')
print('Loaded the word list!')

wordsList = wordsList.tolist()
wordsList = [word.decode('UTF-8') for word in wordsList]
#variab = wordsList[:5]
wordVectors = np.load('D:/Sentiment/Glove/wordVectors.npy')
print('Loaded word Vectors')

# create garph
import tensorflow as tf

labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])

data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
data = tf.nn.embedding_lookup(wordVectors,input_data)

lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.25)
value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)

correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))

# load in the network
sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, tf.train.latest_checkpoint('D:/Sentiment/Glove/model1'))

contraction_patterns = [(r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'willn\'t', 'will not'), (r'doesn\'t', 'does not'),
                        (r'i\'m', 'i am'), (r'don\'t', 'do not'), (r'didn\'t', 'did not'), (r'mayn\'t', 'may not'),
                        (r'mightn\'t', 'might not'), (r'haven\'t', 'have not'),(r'hadn\'t', 'had not'),(r'hasn\'t', 'has not'),
                        (r'ain\'t', 'is not'), (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'),
                         (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'s', '\g<1> is'), (r'(\w+)\'re', '\g<1> are'), (r'(\w+)\'d', '\g<1> would'), (r'&', 'and'), (r'dammit', 'damn it'), (r'dont', 'do not'), (r'wont', 'will not') ]
def replaceContraction(text):
    patterns = [(re.compile(regex), repl) for (regex, repl) in contraction_patterns]
    for (pattern, repl) in patterns:
        (text, count) = re.subn(pattern, repl, text)
    return text

def replaceURL(text):
    """ Replaces url address with "url" """
    # text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','url',text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    return text

def removeHashtagInFrontOfWord(text):
    """ Removes hastag in front of a word """
    text = re.sub(r'#([^\s]+)', r'\1', text)
    return text

def removeEmoticons(text):
    """ Removes emoticons from text """
    text = re.sub(':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:', '', text)
    return text

""" Creates a dictionary with slangs and their equivalents and replaces them """
with open('D:/Sentiment/slang.txt', encoding='utf8', errors='ignore') as file:
    slang_map = dict(map(str.strip, line.partition('\t')[::2])
    for line in file if line.strip())

slang_words = sorted(slang_map, key=len, reverse=True) # longest first for regex
regex = re.compile(r"\b({})\b".format("|".join(map(re.escape, slang_words))))
replaceSlang = partial(regex.sub, lambda m: slang_map[m.group(1)])

strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

def getSentenceMatrix(sentence):
    #arr = np.zeros([batchSize, maxSeqLength])
    sentenceMatrix = np.zeros([batch_size,maxSeqLength], dtype='int32')
    sentence = sentence.translate(string.punctuation)
    sentence = cleanSentences(sentence)
    sentence = removeEmoticons(sentence)
    sentence = replaceURL(sentence)
    sentence = replaceSlang(sentence)
    sentence = removeHashtagInFrontOfWord(sentence)
    sentence = replaceContraction(sentence)
    split = sentence.split()
    print(split)
    for indexCounter,word in enumerate(split):
        try:
            sentenceMatrix[0,indexCounter] = wordsList.index(word)
        except ValueError:
            sentenceMatrix[0,indexCounter] = 399999 #Vector for unkown words
    return sentenceMatrix


#inputText ="The phone is good"
#inputMatrix = getSentenceMatrix(inputText)

def makepredictions(input_text):
    inputMatrix = getSentenceMatrix(input_text)
    print(input_text)
    predictedSentiment = sess.run(prediction, {input_data: inputMatrix})[0]
    # predictedSentiment[0] represents output score for positive sentiment
    # predictedSentiment[1] represents output score for negative sentiment
    print(predictedSentiment[0])
    print(predictedSentiment[1])
    if (predictedSentiment[0] > predictedSentiment[1]):
        return (1) #for positive
    else:
        return (0) # for negative
