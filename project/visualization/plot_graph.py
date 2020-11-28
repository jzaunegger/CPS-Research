'''
    This is a basic python script that reads in a csv file, 
    from the formatted style and plots a data to visualize the
    input data.

    Usage: run the command 'python3 plot_graph.py'
    Author: jzaunegger
'''

# Import Dependencies
import os, csv, sys
import matplotlib.pyplot as plt

# Import CSV File
filename = "normal"
filepath = os.path.join("../pre-processing/output", filename + ".csv")

# Process the Data
times = []
registers = []
values = []

if(os.path.exists(filepath)):
    print("Reading Data from:", filepath)
    with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            lineCount = 0

            for row in csv_reader:
                times.append(row[0])
                registers.append(row[1])
                values.append(row[2])
else:
    print("The given filepath", filepath, "does not exist.")
    sys.exit()

sampleSize = 20

# Create the Graph
plt.plot(times[0:sampleSize], values[0:sampleSize], 'r')
plt.ylabel("Register Values")
plt.xlabel("Time Value")
plt.show()

print("Graph Created.")

