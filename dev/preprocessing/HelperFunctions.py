import os, sys, csv
from datetime import datetime

def convertDateTime(timestamp):
    formatted_date = timestamp[0:10]
    formatted_time = timestamp[11:]

    date = [ int(formatted_date[0:2]), int(formatted_date[3:5]), int(formatted_date[6:]) ]
    time = [  int(formatted_time[0:2]), int(formatted_time[3:5]), int(formatted_time[6:8]) ]

    past_date = datetime(
        year = date[2],
        month = date[0], 
        day = date[1],
        hour = time[0],
        minute=  time[1],
        second = time[2]
    )

    current_utc = datetime.utcnow()

    diff = current_utc - past_date
    return diff


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

        
        output_folder = os.path.join(os.getcwd(), output_folder)
        outfile_name = os.path.join(output_folder, file_name + '.csv')

        # Write out the file data
        with open(outfile_name, mode='w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')

            for entry in file_data:
                utc_diff = convertDateTime(entry[0])
                sensor_id = entry[1]
                sensor_val = entry[2]
                new_line = [str(utc_diff), sensor_id , sensor_val]

                csv_writer.writerow(new_line)
        
        print("Processed {} lines, and formatted the data.".format(line_count))
        print("Saved data to", output_folder)
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