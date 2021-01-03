# Import Dependencies
import matplotlib.pyplot as plt 
import csv, os

class Sensor:
    def __init__(self, name):
        self.name = name
        self.entries = []
        self.times = []
        self.ids = []
        self.values = []

    def addEntry(self, entry):
        new_time = entry[0]
        new_id = entry[1]
        new_value = entry[2]

        self.entries.append(entry)
        self.times.append(new_time)
        self.ids.append(new_id)
        self.values.append(new_value)

    def findBounds(self, values):
        minimum = min(values)
        maximum = max(values)
        return minimum, maximum

    def graphValues(self):
        plt.plot(self.times, self.values)

        x_min, x_max = self.findBounds(self.times)
        y_min, y_max = self.findBounds(self.values)
        plt.axis([x_min, x_max, y_min, y_max])
        plt.xlabel('Time')
        plt.ylabel('Sensor Values')
        plt.show()

file_path = os.path.join(os.getcwd(), 'formatted-data', 'bad_connection.csv')
data = []

with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        data.append(row)

print("Read {} lines from the file {}".format(len(data), file_path))

values = {
    "sensor-1": Sensor("Sensor-1"),
    "sensor-2": Sensor("Sensor-1"),
    "sensor-3": Sensor("Sensor-1"),
    "sensor-4": Sensor("Sensor-1"),
    "sensor-5": Sensor("Sensor-1"),
    "sensor-6": Sensor("Sensor-1"),
    "sensor-7": Sensor("Sensor-1"),
    "sensor-8": Sensor("Sensor-1"),
    "sensor-9": Sensor("Sensor-1"),
    "sensor-10": Sensor("Sensor-1"),
}

# Process the data
for i in range(0, len(data), 10):

    if i + 9 < len(data):
        values["sensor-1"].addEntry(data[i])
        values["sensor-2"].addEntry(data[i+1])
        values["sensor-3"].addEntry(data[i+2])
        values["sensor-4"].addEntry(data[i+3])
        values["sensor-5"].addEntry(data[i+4])
        values["sensor-6"].addEntry(data[i+5])
        values["sensor-7"].addEntry(data[i+6])
        values["sensor-8"].addEntry(data[i+7])
        values["sensor-9"].addEntry(data[i+8])
        values["sensor-10"].addEntry(data[i+9])

values["sensor-1"].graphValues()
