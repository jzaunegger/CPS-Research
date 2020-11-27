'''
    A basic 1D-CNN to analyze data.
    Built using Tensorflow

    Author: jzaunegger
'''
# Import Dependencies
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

# Load File Function
def loadCSV(filepath):
    data = []
    if(os.path.exists(filepath)):
        print("LOADING FILE:", filepath)
        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            lineCount = 0

            for row in csv_reader:
                if lineCount == 0:
                    lineCount += 1
                else:
                    rowEntry = np.array(row)
                    data.append(rowEntry)
                    lineCount += 1
    else:
        print("ERROR:", filepath, "DOES NOT EXSIST, WILL IGNORE.")

    currentFile = np.array(data)

    return currentFile

# Load Dataset
def loadDataset(paths):
    labels = []
    dataset = []
    shapes = []

    for i in range(0, len(paths)):
        currentPath = paths[i][0]
        currentData = loadCSV(currentPath)

        dataset.append(currentData)
        shapes.append(currentData.shape)
        labels.append(paths[i][1])

    return labels, dataset, shapes


# Turn Off GPU-Utilization 
# Useful if you have a AMD card where CUDA is not supported
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

paths = [
    ['../dataset/logs/normal.csv', 'Normal'],
    ['../dataset/logs/spoofing.csv', 'Spoofing'],
    ['../dataset/logs/DoS_attack.csv', 'DoS Attack'],
    ['../dataset/logs/bad_connection.csv', 'Bad Connection'],
    ['../dataset/logs/plastic_bag.csv', 'Plastic Bag'],
    ['../dataset/logs/wet_sensor.csv', 'Wet Sensor'],
    ['../dataset/logs/poly_2.csv', 'Poly 2'],
    ['../dataset/logs/poly_7.csv', 'Poly 7'],
    ['../dataset/logs/hits_1.csv', 'Hits 1'],
    ['../dataset/logs/hits_2.csv', 'Hits 2'],
    ['../dataset/logs/hits_3.csv', 'Hits 3'],
    ['../dataset/logs/high_blocked.csv', 'High Blocked'],
    ['../dataset/logs/second_blocked.csv', 'Second Blocked'],
    ['../dataset/logs/blocked_1.csv', 'Blocked 1'],
    ['../dataset/logs/blocked_2.csv', 'Blocked 2']
]

# Import Data from a CSV File
# path = '../dataset/logs/normal.csv'
# loadCSV(path)


labels, dataset, shapes = loadDataset(paths)


print("=======================================================")
# Compute the largest shape
largestShape = 0

for shape in shapes:
    val = shape[0]

    if(largestShape < val):
        largestShape = val

print("The largest shape is", largestShape)

totalEntries = 0
newEntries = 0

# Add Extra Rows
for values in dataset:

    valuesSize = len(values)
    totalEntries += valuesSize

    newValues = []

    if(valuesSize < largestShape):

        difference = largestShape - valuesSize
        newEntries += difference

        newVals = []
        for i in range(0, difference):
            vals = np.array(['0', '0', '0'])
            newVals.append(vals)
        
        newValues = np.append(values, np.array(newVals), axis=0)
    
    print(newValues)
    values = newValues
    print(values)

print(totalEntries, "Pre-exsisting Entries")
print(newEntries, "New Entries")
print(totalEntries + newEntries, "Total Entries")
print("=======================================================")

# Check Values are all the same size
for values in dataset:
    print(len(values))