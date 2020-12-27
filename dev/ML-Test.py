'''
    This is a test of a basic DCNN Architecture to work with the CPS Dataset.
    This data is a series of csv files that are converted to images, by 
    taking each reading over time, and using them to represent various, colors 
    in the images. This image data is then saved to a pickle object to be loaded over and
    over again in various training examples.

    Author: jzaunegger
'''

# Import Dependencies
import os, pickle, sys
from HelperFunctions import *
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

# Initalize Parameters
pickle_path = os.path.join(os.getcwd(), 'pickle-data', 'CPS-Image-Data.obj')
num_epochs = 30
validation_split = 0.6
input_shape = (20, 10, 3)

pickle_data = load_pickle_object(pickle_path)
image_labels = pickle_data['image-labels']
image_data = pickle_data['image-data']

# Log Information about the dataset
analyze_object(pickle_data)
label_table = labelLookup(pickle_data)

# Split the dataset and destructure
split_data = splitData(pickle_data, label_table, validation_split)
train_data = split_data['train-data']
train_labels = split_data['train-labels']
test_data = split_data['test-data']
test_labels = split_data['test-labels']

preview_images, preview_labels = gatherPreviewImages(pickle_data)

plt.figure(figsize=(10, 50))
for i in range( len(preview_images)):
    plt.subplot(15, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(preview_images[i])
    plt.xlabel(preview_labels[i], labelpad=10)
plt.show()


# Create a basic CNN, Build the model
model = models.Sequential()
model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, (2, 2), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(len(image_labels)))

# Log the model summry
model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(
    train_data,
    train_labels,
    epochs=num_epochs, 
    validation_data=(test_data, test_labels)
    )

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(num_epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

test_loss, test_acc = model.evaluate(test_data, test_labels, verbose=2)


print("-------------------------------------------------------------------------------")
print("Test Accuracy: {}".format(test_acc))
print("Test Loss: {}".format(test_loss))
print("-------------------------------------------------------------------------------")