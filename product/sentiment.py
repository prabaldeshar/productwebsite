numDimensions = 300
maxSeqLength = 250
batchSize = 24
lstmUnits = 128
numClasses = 2
iterations = 100000

import numpy as np

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
saver.restore(sess, tf.train.latest_checkpoint('D:/Sentiment/models1'))

import re
strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

def getSentenceMatrix(sentence):
    #arr = np.zeros([batchSize, maxSeqLength])
    sentenceMatrix = np.zeros([batchSize,maxSeqLength], dtype='int32')
    cleanedSentence = cleanSentences(sentence)
    split = cleanedSentence.split()
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
