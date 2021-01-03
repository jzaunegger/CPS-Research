import os, sys, csv
from CPS import *

ds = Dataset('CPS')
ds.read_files(os.path.join(os.getcwd(), 'raw-dataset'))
ds.format_dataset(10)

#ds.log_dataset()

#ds.export_dataset(ds, os.path.join(os.getcwd(), 'CPS-Dataset'))
ds.convert_to_images(20)
ds.save_images(os.path.join(os.getcwd(), 'CPS-Dataset'))
ds.log_image_dataset()

#print(ds.categories)
#print(len(ds.categories[0].raw_entries))
#print(len(ds.categories[0].formatted_values))