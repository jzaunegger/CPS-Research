# Import Dependencies
import os, sys, csv
import numpy as np
from HelperFunctions import *

# Initalize Parameters
input_folder = 'formatted-data'
output_folder = 'image-data'

# Check if input folder exists
input_path = os.path.join(os.getcwd(), input_folder)
if(os.path.exists(input_path)):
    print("Reading files from", input_path)
    total_image_count = 0

    # Read the subfiles and get the values of each file
    subfiles = os.listdir(input_path)
    for subfile in subfiles:
        file_path = os.path.join(input_folder, subfile)
        file_data = []
        
        # Check file is a csv
        if file_path.endswith('.csv'):
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                
                # Read each line
                for row in csv_reader:
                    file_data.append(row)


        # Process the full file into image format
        entries = convertToEntries(file_data)
        batches = convertToBatches(entries, 20)

        temp_path = os.path.join(os.getcwd(), output_folder)
        sub_folder_name = subfile.replace('.csv', '')
        temp_path = os.path.join(temp_path, sub_folder_name)
        
        # Check if output subfolder exists
        if(os.path.exists(temp_path) == False):
            os.mkdir(temp_path)
            print("Generated output folder for", sub_folder_name)


        counter = 0
        for batch in batches:
            if(counter < 10):
                filename = sub_folder_name + "0000" + str(counter) + '.png'
                out_file_name = os.path.join(temp_path, filename)
                convertBatchToImage(batch, out_file_name)

            elif(counter < 100):
                filename = sub_folder_name + "000" + str(counter) + '.png'
                out_file_name = os.path.join(temp_path, filename)
                convertBatchToImage(batch, out_file_name)

            elif(counter < 1000):
                filename = sub_folder_name + "00" + str(counter) + '.png'
                out_file_name = os.path.join(temp_path, filename)
                convertBatchToImage(batch, out_file_name)

            elif(counter < 10000):
                filename = sub_folder_name + "0" + str(counter) + '.png'
                out_file_name = os.path.join(temp_path, filename)
                convertBatchToImage(batch, out_file_name)
            counter += 1

        total_image_count += counter

        print("Exported", len(batches),"images to folder", temp_path)
        print(" ")
    
    print("Exported", total_image_count, "images in total.")


# Throw error if the input folder does not exist
else:
    print(" ")
    print("System Error:")
    print("-------------------------------------------------------------------------------")
    print("The given path to the file or the output folder does not exist.")
    print("same working directory as this script. This system will only read-in csv files.")
    print(" ")
    sys.exit()