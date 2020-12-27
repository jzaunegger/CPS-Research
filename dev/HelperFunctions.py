# Import Dependencies
import os, sys, csv, pickle
import numpy as np
from PIL import Image
from datetime import datetime

def convertValuesToRGB(values):
    new_vals = []
    current_timestamp = datetime.timestamp(datetime.now())
    
    for value in values:
        R = LinearMapping(0, int(current_timestamp), 0, 255, int(value[0]), True)
        G = LinearMapping(0, 10, 0, 255, int(value[1]), True)
        B = LinearMapping(0, 9999, 0, 255, int(value[2]), True)
        new_vals.append([R, G, B])

    return new_vals

def convertToEntries(values):
    entries = []
    for i in range(0, len(values), 10):
        rgb_vals = convertValuesToRGB(values[i:i+10])
        entries.append(rgb_vals)

    return entries

def convertToBatches(values, batch_size):
    batches = []

    for i in range(0, len(values), batch_size):
        if i + batch_size < len(values):
            batch = values[i:i+batch_size]
            batches.append(batch)
    
    return batches

def convertBatchToImage(batch, out_file_path):
    np_batch = np.array(batch)

    img = Image.fromarray(np_batch, 'RGB')
    img.save(out_file_path)


####################################################################################################
# Function that takes a time stamp, and returns the difference from the input time and the UNIX UTC
# standard time.
#
# Input Parameters:
####################################################################################################
# current_a     : The smallest value in the current value range
# current_b     : The largest value in the current value range
# target_c      : The smallest value in the target value range
# target_d      : The largest value in the target value range
# num           : The number to transform
# returnInt     : Boolean value to determine if the return value is a int or float
####################################################################################################
def convertDateTime(timestamp):
    formatted_date = timestamp[0:10]
    formatted_time = timestamp[11:]

    date = [ int(formatted_date[0:2]), int(formatted_date[3:5]), int(formatted_date[6:]) ]
    time = [  int(formatted_time[0:2]), int(formatted_time[3:5]), int(formatted_time[6:8]) ]

    past_date = datetime( year=date[2], month=date[0], day=date[1], hour=time[0], minute=time[1], second=time[2] )
    current_timestamp = datetime.timestamp(past_date)
    return int(current_timestamp)

####################################################################################################
# Function that will format a target value, and write the formatted values to a new file.
#
# Input Parameters:
####################################################################################################
# file_path         : The path to the csv file to format,
# output_folder     : The folder to save the output files in.
# file_name         : The name of the file to be saved.
####################################################################################################
def formatFile(file_path, output_folder, file_name):

    # Check if the output folder does not exist
    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)
        print(" ")
        print("Generated output folder:", output_folder)

    # Check if the input file exists
    if os.path.exists(file_path):
        labels = []
        file_data = []

        # Read in the file data
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    labels = row
                    line_count += 1
                else:
                    #convertDateTime(row[0])
                    file_data.append(row)
                    line_count += 1

        
        output_folder_path = os.path.join(os.getcwd(), output_folder)
        outfile_name = os.path.join(output_folder_path, file_name + '.csv')

        # Write out the file data
        with open(outfile_name, mode='w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')

            for entry in file_data:
                utc_diff = convertDateTime(entry[0])
                sensor_id = entry[1]
                sensor_val = entry[2]
                new_line = [str(utc_diff), sensor_id , sensor_val]

                csv_writer.writerow(new_line)
        
        print("Processed {} lines, and formatted the data for {}".format(line_count, file_name))
        print("Saved data to", output_folder_path)
        print(" ")
    
    # Throw error if the input file does not exist.
    else:
        print(" ")
        print("System Error:")
        print("-------------------------------------------------------------------------------")
        print("The given path to the file or the output folder does not exist.")
        print("same working directory as this script. This system will only read-in csv files.")
        print(" ")
        sys.exit()

####################################################################################################
# Function that transforms a given value, into a value within a given range.
#
# Input Parameters:
####################################################################################################
# current_a     : The smallest value in the current value range
# current_b     : The largest value in the current value range
# target_c      : The smallest value in the target value range
# target_d      : The largest value in the target value range
# num           : The number to transform
# returnInt     : Boolean value to determine if the return value is a int or float
####################################################################################################
def LinearMapping(current_a, current_b, target_c, target_d, num, returnInt):
    target = (target_d - target_c)
    current = (current_b - current_a)
    scale = target / current
    offset = -current_a * target / current + target_c
    val = num * scale + offset

    if returnInt:
        return int(val)
    else:
        val = float(val)
        return "{:.2f}".format(val)


# Function to remove underscores and capitalize the first letter of each word
def formatCategoryName(raw_name):
    words = raw_name.split('_')
    processed_words = []

    for word in words:
        if word[0].isdigit() == True:
            processed_words.append(word)
        else:
            processed_words.append(word.capitalize())

    new_name = ''
    for new_word in processed_words:
        new_name += new_word + ' '

    return new_name

def longestCatName(cats):
    maxLen = len(cats[0])
    for val in cats:
        if len(val) > maxLen:
            maxLen = val
    return maxLen

def load_pickle_object(path):
    if os.path.exists(path):
        data = pickle.load( open( path, "rb" ) )
        return data

    else:
        print(" ")
        print("System Error:")
        print("-------------------------------------------------------------------------------")
        print("Could not load the given pickle object from the file. Please enter a valid path.")
        print(" ")
        sys.exit()

def analyze_object(data):
    imgs = data['image-data']
    lbls = data['image-labels']

    counts = []
    total_count = 0

    for images in imgs:
        counter = 0
        for image in images:
            counter += 1

        counts.append(counter)
        total_count += counter

    
    print("Read {} images spanning {} categories.".format(total_count, len(lbls)))
    print("-------------------------------------------------------------------------------")
    print("{:20s} {:20s} {:20s} {:20s}".format("Category Name", "# Images", "Image Shape", "Data Percentage"))
    print("-------------------------------------------------------------------------------")
    for i in range(len(counts)):
        percentage = "{:10.4%}".format(counts[i] / total_count)

        print("{:20s} {:20s} {:20s} {:20s}".format( lbls[i][0], str(counts[i]), str(imgs[i][0].shape ), str(percentage))) 
    print("-------------------------------------------------------------------------------")

def labelLookup(data):
    unique_labels = []
    for group in data['image-labels']:
        for label in group:
            if(len(unique_labels) == 0):
                unique_labels.append(label)

            if label not in unique_labels:
                unique_labels.append(label)
    
    return unique_labels


def labelToInt(labels, label):
    
    for i in range( len(labels) ):
        if label == labels[i]:
            return i
    
    return None


def splitData(data, all_labels, train_split):
    imgs = data['image-data']
    lbls = data['image-labels']

    train_data = []
    test_data = []

    train_labels = []
    test_labels = []

    for i in range(len(imgs)):

        num_imgs = len(imgs[i])
        val_size = int( num_imgs * train_split)
        test_size = num_imgs - val_size

        for j in range(0, val_size):
            cat_val = labelToInt(all_labels, lbls[i][j])
            if cat_val != None:
                train_data.append(imgs[i][j])
                train_labels.append(cat_val)

        for k in range(val_size, num_imgs):
            cat_val = labelToInt(all_labels, lbls[i][k])
            if cat_val != None:
                test_data.append(imgs[i][k])
                test_labels.append(cat_val)

    new_data = {
        "train-data": np.array(train_data),
        "train-labels": np.array(train_labels),
        "test-data": np.array(test_data),
        "test-labels": np.array(test_labels)
    }

    return new_data

def gatherPreviewImages(pickle_data):

    preview_images = []
    preview_labels = []

    images = pickle_data['image-data']
    labels = pickle_data['image-labels']

    for i in range(len(images)):
        for j in range(5):
            preview_images.append(images[i][j])
            preview_labels.append(labels[i][j])

    
    return preview_images, preview_labels






