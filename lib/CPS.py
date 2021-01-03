import os, sys, csv, json, datetime
from PIL import Image, ImageDraw

def checkPath(path):
    # Check if path exists
    if os.path.exists(path):

        # Remove any previously exsisting subfiles
        if len(os.listdir(path)) > 0:
            for item in os.listdir(path):
                
                os.remove(os.path.join(path, item))

    # Create folder
    else:
        os.mkdir(path)

class Dataset:
    # Constructor Function
    def __init__(self, name):
        self.categories = []
        self.input_file_paths = []
        self.input_folder_path = ''
        self.name = name

    def convert_to_object(self):
        pickle_cats = []
        for cat in self.categories:
            pickle_cats.append( cat.return_as_object() )

        obj = {
            'categories': pickle_cats,
            'input_file_paths': self.input_file_paths,
            'input_file_path': self.input_folder_path,
            'name': self.name
        }

        return obj

    def convert_to_images(self, image_height):
        for cat in self.categories:
            cat.convert_to_images(image_height)

    # Function to log a dataset
    def __repr__(self):
        return 'Dataset {}'.format(self.name)

    def log_dataset(self):
        print('---------------------------------------------------------------------------------------------------------------------------------------------')
        print('Dataset {} contains {} categories.'.format(self.name, len(self.categories)))
        print('---------------------------------------------------------------------------------------------------------------------------------------------')
        print('{:20s}{:20s}{:25s}{:15s}'.format('Category Name', '# Raw Entries', '# Formatted Entries', 'File Path'))
        print('---------------------------------------------------------------------------------------------------------------------------------------------')
        for i in range(len(self.categories)):
            print('{:20s}{:20s}{:25s}{:15s}'.format(self.categories[i].name, str(len(self.categories[i].raw_entries)), str(len(self.categories[i].formatted_values)), self.categories[i].filepath))
            
        print('---------------------------------------------------------------------------------------------------------------------------------------------')
        

    def log_image_dataset(self):
        total_image_count = 0
        for cat in self.categories:
            total_image_count += len(cat.image_data)


        print('---------------------------------------------------------------------------------------------------------------------------------------------')
        print('Image Datset Information')
        print('---------------------------')
        print('{:17s} {:13s} {:11s} {:11s} {:30s}'.format('Category Name', '# of Images', 'Dataset %', 'Image Size', 'Image Folder Path'))
        print('---------------------------------------------------------------------------------------------------------------------------------------------')
        for cat in self.categories:
            current_img_count = len(cat.image_data)
            img_percent_f = current_img_count / total_image_count
            img_percent = '{:0>6.2%}'.format(img_percent_f)
            img_size = str((cat.image_width, cat.image_height))
            print('{:17s} {:13s} {:11s} {:11s} {:30s}'.format( cat.name, str(current_img_count), img_percent, img_size, cat.image_output_folder ))

        print('---------------------------------------------------------------------------------------------------------------------------------------------')
    # Read the files from the given folder path
    def read_files(self, folder_path):
        if os.path.exists(folder_path):
            self.input_folder_path = folder_path
            sub_files = os.listdir(folder_path)
            
            for sub_file in sub_files:
                if sub_file.endswith('.csv'):
                    cat_name = sub_file.replace('.csv', '')
                    file_path = os.path.join(folder_path, sub_file)
                    self.input_file_paths.append(file_path)

                    # Create a new category
                    current_cat = Category(cat_name, file_path)
                    current_cat.read_file()
                    self.categories.append(current_cat)

        else:
            print('---------------------------------------------------------------------------------------------------------------------------------------------')
            print('Error: Cannot load folder.')
            print('Error-Msg: Cannot load folder, because the given folder path does not exist.')
            print('---------------------------------------------------------------------------------------------------------------------------------------------')

    # Format the dataset
    def format_dataset(self, batch_size):
        self.batch_size = batch_size
        for cat in self.categories:
            cat.format_data(self.batch_size)

    def save_images(self, folder_path):
        formatted_out = os.path.join(folder_path, 'image-dataset')
        checkPath(formatted_out)
        for cat in self.categories:
            cat.save_images(formatted_out)

    def save_as_json(self, json_name):
        obj = self.convert_to_object()

        json_out = os.path.join(json_name, 'CPS-Data.json')
        with open(json_out, 'w') as json_file:
            json.dump(obj, json_file, sort_keys=True, indent=2, separators=(',',':'))

    def export_dataset(self, data, out_folder):
        self.out_folder = out_folder
        if os.path.exists(self.out_folder) == False:
            os.mkdir(self.out_folder)

        else:
            # Process seperate formatted data
            formatted_out = os.path.join(out_folder, 'formatted-data')
            checkPath(formatted_out)

            # Save current dataset as json
            json_out = os.path.join(out_folder, 'json-data')
            checkPath(json_out)
            self.save_as_json(json_out)

            # Iterate through the categories
            for i in range(len(self.categories)):
                cat = self.categories[i]
                cat_name = cat.name
                cat_out_name = os.path.join(formatted_out, cat_name + '.csv')
                cat_vals = cat.formatted_values

                with open(cat_out_name, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)

                    for j in range(0, len(cat_vals)):
                        csv_writer.writerow(cat_vals[j])

# Class to create a Category
class Category:
    # Category constructor function
    def __init__(self, name, filepath):
        self.entry_labels = []
        self.entries = []
        self.dates = []
        self.filepath = filepath
        self.formatted_values = []
        self.formatted_labels = []
        self.ids = []
        self.image_data = []
        self.image_width = 10
        self.image_height = 10
        self.image_output_folder = ''
        self.name = name
        self.normalized_img_vals = []
        self.raw_entries = []
        self.raw_image_data = []
        self.times = []
        self.values = []

    def return_as_object(self):
        return {
            'entry-labels': self.entry_labels,
            'entries': self.entries,
            'dates': self.dates,
            'filepath': self.filepath,
            'formatted-values': self.formatted_values,
            'formatted-labels': self.formatted_labels,
            'ids': self.ids,
            'name': self.name,
            'raw-entries': self.raw_entries,
            'times': self.times,
            'values': self.values
        }

    # Read the raw file, and split the entries into dates, times, ids, and values.
    def read_file(self):
        with open(self.filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            count = 0

            self.formatted_labels = ['Date', 'Time', 'Sensor ID', 'Sensor Value']
            
            for row in csv_reader:
                if count == 0:
                    self.entry_labels = row
                else:
                    current_date = row[0][0:10]
                    current_time = row[0][11:].replace(' ', '')
                    current_id = row[1]
                    current_value = row[2]

                    self.raw_entries.append(row)
                    self.entries.append([current_date, current_time, current_id, current_value])
                    self.dates.append(current_date)
                    self.times.append(current_time)
                    self.ids.append(current_id)
                    self.values.append(current_value)
                count += 1

    def format_data(self, batch_size):
        self.batch_size = batch_size
        for i in range(0, len(self.entries)):
            self.formatted_values.append(self.entries[i])


    def raw_to_image_data(self):
        # Process raw data values 
        for entry in self.formatted_values:

            # Get base UTC Time
            base_time = datetime.datetime(year=1970, month=1, day=1)

            # Convert Date/Time
            entry_datetime = datetime.datetime(
                year = int(entry[0][7:]), 
                month = int(entry[0][0:2]),
                day = int(entry[0][3:5]),
                hour = int(entry[1][0:2]),
                minute = int(entry[1][3:5]),
                second = int(entry[1][6:8]),
                microsecond = int(entry[1][9:]),
                tzinfo=None
            )

            # Get the time relative to UTC standard time
            time_diff = (entry_datetime - base_time).total_seconds()
            
            # Convert Value
            self.raw_image_data.append([time_diff, entry[2], entry[3]])


    def normalize_value(self, value, min_val, max_val):
        return (int(value) - int(min_val)) / (int(max_val) - int(min_val))

    def constrict_image_data(self):
        min_time, max_time = self.raw_image_data[0][0], self.raw_image_data[0][0]
        min_id, max_id = self.raw_image_data[0][1], self.raw_image_data[0][1]
        min_val, max_val = self.raw_image_data[0][2], self.raw_image_data[0][2]

        for i in range(len(self.raw_image_data)):
            entry = self.raw_image_data[i]

            # Check Times
            if entry[0] < min_time: min_time = entry[0]
            if entry[0] > max_time: max_time = entry[0]

            # Check Ids
            if entry[1] < min_id: min_id = entry[1]
            if entry[1] > max_id: max_id = entry[1]

            # Check Values
            if entry[2] < min_val: min_val = entry[2]
            if entry[2] > max_val: max_val = entry[2]


        for i in range(len(self.raw_image_data)):
            entry = self.raw_image_data[i]
            nrm_time = self.normalize_value(entry[0], min_time, max_time)
            nrm_id = self.normalize_value(entry[1], min_id, max_id)
            nrm_val = self.normalize_value(entry[2], min_val, max_val)
            self.normalized_img_vals.append([nrm_time, nrm_id, nrm_val])

        
    def convert_nrm_to_rgb(self, entry):
        r = int( entry[0] * 255)
        g = int( entry[1] * 255)
        b = int( entry[2] * 255)
        return [r, g, b]


    def convert_to_images(self, image_height):
        self.image_height = image_height
        self.raw_to_image_data()
        self.constrict_image_data()

        widths = []

        # Trim extra values
        if len(self.normalized_img_vals) % self.image_width != 0:
            val = len(self.normalized_img_vals) % self.image_width
            for i in range(val):
                index = len(self.normalized_img_vals) -1
                self.normalized_img_vals.pop(index)

        # Divide Data into Image Widths
        for i in range(0, len(self.normalized_img_vals), self.image_width):
            if i + self.image_width <= len(self.normalized_img_vals):
                temp = []
                for j in range(i, i+ (self.image_width-1)):
                    temp.append(self.convert_nrm_to_rgb(self.normalized_img_vals[j]))
                widths.append(temp)

        # Divide image widths by heights to complete image data
        for k in range(0, len(widths), self.image_height):
            if k + self.image_height <= len(widths):
                self.image_data.append( widths[k:k+(self.image_height-1)] )

    def save_images(self, folder_path):
        self.image_output_folder = os.path.join(folder_path, self.name)
        checkPath(self.image_output_folder)

        for i in range(len(self.image_data)):
            current_data = self.image_data[i]

            img_num = '{:0>5}'.format(i)
            file_name = self.name + '-' + img_num + '.png'
            file_path = os.path.join(self.image_output_folder, file_name)
            img_size = (self.image_width, self.image_height)

            current_img = Image.new('RGB', img_size, (0, 0, 0))
            for col_index in range(len(current_data)):
                for row_index in range(len(current_data[col_index])):
                    current_rgb = current_data[col_index][row_index]
                    rgb_tuple = (current_rgb[0], current_rgb[1], current_rgb[2])
                    current_img.putpixel( (row_index, col_index), rgb_tuple)

            current_img.save(file_path, 'PNG')


    def visualize_samples(self):
        if self.image_output_folder == '':
            print('---------------------------------------------------------------------------------------------------------------------------------------------')
            print('Error: Cannot load images..')
            print('Error-Msg: Cannot load folder, because the images you are trying to visualize do not yet exist.')
            print('---------------------------------------------------------------------------------------------------------------------------------------------')

    
    # What the console prints the object as when called as a string
    def __str__(self):
        return '{:14s}'.format(self.name)