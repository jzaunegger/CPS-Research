import os, sys, csv, json, datetime, shutil
from PIL import Image, ImageDraw, ImageFont

def checkPath(path):
    # Check if path exists
    if os.path.exists(path):

        # Remove any previously exsisting subfiles
        if len(os.listdir(path)) > 0:
            for item in os.listdir(path):
                temp = os.path.join(path, item)
                if os.path.isdir(temp):
                    shutil.rmtree(temp)
                elif os.path.isfile(temp):
                     os.remove(temp)

    # Create folder
    else:
        os.mkdir(path)

class Dataset:
    # Constructor Function
    def __init__(self, name):
        self.categories = []
        self.input_file_paths = []
        self.input_folder_path = ''
        self.out_folder = ''
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

    def visualize_samples(self, out_folder):
        checkPath(out_folder)
        self.out_folder = out_folder
        for cat in self.categories:
            cat.visualize_samples(self.out_folder)

    def plot_categories(self, out_folder):
        base_out_folder = os.path.join(out_folder, 'data-plots')
        checkPath(base_out_folder)
        self.out_folder = out_folder
        for cat in self.categories:
            cat.plot_category(base_out_folder)

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

    def draw_grid(self):
        base_image = Image.new('RGB', (2400, 1200), (255, 255, 255))
        base_draw = ImageDraw.Draw(base_image)
        head = ImageFont.truetype(font=os.path.join(os.getcwd(), 'DejaVuSans.ttf'), size=40)

        plot_name = self.name.replace("_", ' ')
        plot_name = plot_name.capitalize()
        label_font = ImageFont.truetype(font=os.path.join(os.getcwd(), 'DejaVuSans.ttf'), size=32)

        base_draw.text((1200, 50), plot_name, font=head, fill=(0, 0, 0), anchor='mm', align='center')

        # Draw Y Axis
        y_axis = [(100, 100), (100, 1100)]
        base_draw.line(y_axis, fill=(0, 0, 0), width=4)

        # Draw Y Ticks
        x = 200
        for i in range(21):
            points = [(x, 100), (x, 1100)]
            base_draw.line(points, fill=(0, 0, 0), width=2)
            x += 100

        # Draw X Axis
        x_axis = [(100, 1100), (2200, 1100)]
        base_draw.line(x_axis, fill=(0, 0, 0), width=4)
        base_draw.text((1200, 1150), 'Time', font=label_font, fill=(0, 0, 0), anchor='mm')

        # Draw X Ticks
        y = 100
        for i in range(10):
            points = [(100, y), (2200, y)]
            base_draw.line(points, fill=(0, 0, 0), width=2)
            y += 100

        return base_image


    def fit_bounds(self, value, left_min, left_max, right_min, right_max):
        left_span = left_max - left_min
        right_span = right_max - right_min
        scale = float(right_span) / float(left_span)
        return right_min + (value - left_min) * scale


    def fit_entry(self, entry):
        x = self.fit_bounds(entry[0], 0, 1, 100, 2300)
        y = self.fit_bounds(entry[1], 0, 1, 100, 1100)
        return (int(x), int(y))

    def plot_category(self, out_folder):
        cat_out_folder = os.path.join(out_folder, self.name)
        checkPath(cat_out_folder)

        img_name = self.name + '-plot.png'
        img_path = os.path.join(cat_out_folder, img_name)
        
        base_image = Image.new('RGB', (2300, 1200), (255, 255, 255))
        base_draw = ImageDraw.Draw(base_image)

        plot_base = self.draw_grid()
        base_image.paste(plot_base, (0,0))

        # Process the data to be grouped by sensor
        data = self.normalized_img_vals

        segments = []
        for i in range(0, len(data), self.image_width):
            if i + self.image_width <= len(data):
                segments.append(data[i:i+(self.image_width)])

        sensor0 = []
        sensor1 = []
        sensor2 = []
        sensor3 = []
        sensor4 = []
        sensor5 = []
        sensor6 = []
        sensor7 = []
        sensor8 = []
        sensor9 = []

        counter = 1
        for i in range(len(segments)):
            if counter == 1:
                sensor0.append( self.fit_entry(segments[i][0]))
            elif counter == 2:
                sensor1.append(self.fit_entry(segments[i][1]))
            elif counter == 3:
                sensor2.append(self.fit_entry(segments[i][2]))
            elif counter == 4:
                sensor3.append(self.fit_entry(segments[i][3]))
            elif counter == 5:
                sensor4.append(self.fit_entry(segments[i][4]))
            elif counter == 6:
                sensor5.append(self.fit_entry(segments[i][5]))
            elif counter == 7:
                sensor6.append(self.fit_entry(segments[i][6]))
            elif counter == 8:
                sensor7.append(self.fit_entry(segments[i][7]))
            elif counter == 9:
                sensor8.append(self.fit_entry(segments[i][8]))
            elif counter == 10:
                sensor9.append(self.fit_entry(segments[i][9]))

            counter += 1
            if counter > 10:
                counter = 1
        sensors = [sensor0, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9]
        sensor_colors = [ '#fff100', '#ff8c00', '#e81123', '#ec008c', '#68217a', '#00188f', '#00bcf2', '#00b294', '#009e49', '#bad80a' ]

        for i in range(len(sensors)):
            current_color = sensor_colors[i]
            base_draw.line(sensors[i], fill=current_color, width=1)





        base_image.save(img_path,'PNG')




    def visualize_samples(self, out_folder):
        self.visualization_folder = out_folder
        if self.image_output_folder == '':
            print('---------------------------------------------------------------------------------------------------------------------------------------------')
            print('Error: Cannot load images..')
            print('Error-Msg: Cannot load folder, because the images you are trying to visualize do not yet exist.')
            print('---------------------------------------------------------------------------------------------------------------------------------------------')
        else:
            # Check how many images exist
            sub_files = sorted(os.listdir(self.image_output_folder))
            cat_out_folder = os.path.join(self.visualization_folder, self.name)
            checkPath(cat_out_folder)

            if len(sub_files) > 5:
                base_size = (self.image_width * 2, self.image_height * 6)
                base_image = Image.new('RGB', base_size, (255, 255, 255))
                base_image_name = os.path.join(cat_out_folder, self.name + '-visualzation.png')
                
                sample_paths = sub_files[0:5]
                for i in range(len(sample_paths)):
                    x_pos = int(self.image_width / 2)
                    y_pos = int(self.image_height * i + (self.image_height/2))
                    img_path = os.path.join(self.image_output_folder, sample_paths[i])
                    current_img = Image.open(img_path)

                    base_image.paste(current_img, (x_pos, y_pos))
                
                base_image.save(base_image_name, 'PNG')

    
    # What the console prints the object as when called as a string
    def __str__(self):
        return '{:14s}'.format(self.name)