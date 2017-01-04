"""
A simple introduction to Keras Neural Networks using a MLP and the pima indians data set, this is a modified version of the tutorial found here:
http://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

TO DO :
- split the dataset into train, test, validate
- cross validation??? or plot NN performance over time
- find other ways to evaluate model performance
"""
# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import numpy as np
import urllib

# fix random seed for reproducibility
np.random.seed(0)

#===================================================================
# load data set from url
#===================================================================
# URL for the Pima Indians Diabetes dataset (UCI Machine Learning Repository)
url = "http://goo.gl/j0Rvxq"
# download the file
raw_data = urllib.urlopen(url)
# load the CSV file as a numpy matrix
dataset = np.loadtxt(raw_data, delimiter=",")
print(dataset.shape)


#===================================================================
# Split the dataset
#===================================================================
# this is typically where I would train, test, validate Split
# but lets wait as this is still our first steps with NN in Keras
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]


#===================================================================
# Build the Neural Network
#===================================================================
# create model
model = Sequential()
model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
history = model.fit(X, Y, validation_split=0.33, nb_epoch=500, batch_size=10, verbose=0)


#===================================================================
# first attempt to view model performance
#===================================================================
# evaluate the model (without print to screen)
# scores = history.model.evaluate(X, Y,verbose=0)
# print("%s: %.2f%%" % (history.model.metrics_names[1], scores[1]*100))


#===================================================================
# Plot the History of Model Training
#===================================================================
#http://machinelearningmastery.com/display-deep-learning-model-training-history-in-keras/
# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
