'''
    This script takes a csv file from the given filepath,
    reads the values, and reformats them for use in 
    Machine Learning.

    Author: jzaunegger
'''

# Import Dependencies
import os, csv
import numpy as np

filename = "wet_sensor"

filepath = os.path.join("../../dataset/logs/", filename + ".csv")


# Process the file
if(os.path.exists(filepath)):

    labels = []
    data = []

    # Checking if the file exsists
    print("Formatting file from:", filepath)
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lineCount = 0

        for row in csv_reader:

            # Calculate the CSV Labels
            if lineCount == 0:
                for entry in row:
                    labels.append(entry)
                lineCount += 1

            else:
                temp = []
                for i in range(0, len(row)):
                    if i == 0:
                        time = row[i]
                        time = time[10:].strip()
                        temp.append(time)

                    else:
                        temp.append(row[i])
                data.append(temp)

else:
    print("The given filepath does not exsist.")

# Export the formatted file
outputPath = os.path.join(os.getcwd(), "output/" + filename + ".csv")

if(os.path.exists(outputPath)):
    print("Overwriting File: ", outputPath)
    newFile = open(outputPath, "w")

    for entry in data:
        line = ""
        for item in entry:
            line += item + ", "

        newFile.write(line + "\n")
    newFile.close()

else:
    print(os.getcwd())
    print("Creating File: ", outputPath)
    newFile = open(outputPath, "x")

    for entry in data:
        line = ""
        for item in entry:
            line += item + ", "

        newFile.write(line + "\n")
    newFile.close()

print("Sucessfully Formatted Data, with a shape of", np.array(data).shape)

