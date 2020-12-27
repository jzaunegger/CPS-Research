# Import Dependencies
import os, sys, csv
from HelperFunctions import *

# Initalize System Parameters
input_folder = 'raw-dataset'
output_folder = 'formatted-data'


# Check if the folder exists
input_path = os.path.join(os.getcwd(), input_folder)
if os.path.exists(input_path):
    print(" ")
    print("Formatting the data in folder:", input_path)
    print("-------------------------------------------------------------------------------")

    subfiles = os.listdir(input_path)

    for subfile in subfiles:
        if subfile.endswith('.csv'):
            file_name = subfile.replace('.csv', '')
            file_path = os.path.join(input_path, subfile)
            formatFile(file_path, output_folder, file_name)

    print("-------------------------------------------------------------------------------")
    print("Sucessfully formatted", len(subfiles), "files.")
    print(" ")

else:
    print(" ")
    print("System Error:")
    print("-------------------------------------------------------------------------------")
    print("The given folder does not exist. Please make sure the input folder is in the")
    print("same working directory as this script. This system will only read-in csv files.")
    print(" ")
    sys.exit()