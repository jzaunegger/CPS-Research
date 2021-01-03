# Import Dependencies
import matplotlib.pyplot as plt 
from datetime import datetime
import csv, os

class Dataset:
    def __init__(self, name):
        self.name = name

        self.data = []
        self.sensors = [
            Sensor("Sensor-1"),
            Sensor("Sensor-2"),
            Sensor("Sensor-3"),
            Sensor("Sensor-4"),
            Sensor("Sensor-5"),
            Sensor("Sensor-6"),
            Sensor("Sensor-7"),
            Sensor("Sensor-8"),
            Sensor("Sensor-9"),
            Sensor("Sensor-10")
        ]

    def add_raw_entry(self, entry):
        self.data.append(entry)

    def format_dataset(self):
        for i in range(0, len(self.data), 9):
            if i + 9 < len(self.data):
                self.sensors[0].addEntry(self.data[i])
                self.sensors[1].addEntry(self.data[i+1])
                self.sensors[2].addEntry(self.data[i+2])
                self.sensors[3].addEntry(self.data[i+3])
                self.sensors[4].addEntry(self.data[i+4])
                self.sensors[5].addEntry(self.data[i+5])
                self.sensors[6].addEntry(self.data[i+6])
                self.sensors[7].addEntry(self.data[i+7])
                self.sensors[8].addEntry(self.data[i+8])
                self.sensors[9].addEntry(self.data[i+9])

    def convertDates(self):
        for i in range(len(self.sensors)):
            for j in range(len(self.sensors[i].dates)):
                val = self.sensors[i].dates[j]

                month = val[0:2]
                day = val[3:5]
                year = val[6:]

                vals = [int(month), int(day), int(year)]
                self.sensors[i].dates[j] = vals

    def plotGraph(self, x_vals, x_label, y_vals, y_label):

        # Determine the x min and x max 
        x_min, x_max = 1000, 0
        for val1 in x_vals:
            if val1 < x_min:
                x_min = val1
            if val1 > x_max:
                x_max = val1

        y_min, y_max = 1000, 0
        for val2 in y_vals:
            if val2 < y_min:
                y_min = val2
            if val2 > y_max:
                y_max = val2

        plt.plot(x_vals, y_vals)
        plt.axis([x_min, x_max, y_min, y_max])
        plt.xlabel = x_label
        plt.ylabel = y_label
        plt.show()

    def log_data(self):
        print("----------------------------------------------------------------------")
        print("Dataset {} contains {} sensors.".format(self.name, len(self.sensors)))
        print("----------------------------------------------------------------------")
        for sensor in self.sensors:
            print("{:9s} contains {} dates, {} times, {} ids, and {} values.".format( sensor.name, len(sensor.dates), len(sensor.times), len(sensor.ids), len(sensor.values)))
        print("----------------------------------------------------------------------")
        print("This dataset contains {} entries.".format(len(self.data)))
        print("----------------------------------------------------------------------")

class Sensor:
    def __init__(self, name):
        self.name = name
        self.entries = []
        self.dates = []
        self.times = []
        self.ids = []
        self.values = []

    def addEntry(self, entry):
        new_date = entry[0]
        new_time = entry[1]
        new_id = entry[2]
        new_value = entry[3]

        self.entries.append(entry)
        self.dates.append(new_date)
        self.times.append(new_time)
        self.ids.append(new_id)
        self.values.append(new_value)

file_path = os.path.join(os.getcwd(), 'raw-dataset', 'bad_connection.csv')
data = []
labels = []

ds = Dataset("CPS-Dataset")

with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    counter = 0
    sub_count = 0

    for row in csv_reader:
        if counter == 0:
            labels.append(row)
        
        else:
            entry_date = row[0][0:10]
            entry_time = row[0][11:].lstrip()
            entry_id = row[1]
            entry_value = row[2]
            ds.add_raw_entry([entry_date, entry_time, entry_id, entry_time])
        counter += 1

ds.format_dataset()
ds.log_data()
ds.convertDates()
#ds.plotGraph( ds.sensors[0].times, "Time", ds.sensors[0].values, "Sensor Values")