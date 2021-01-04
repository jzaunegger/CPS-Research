import os, sys, csv
from CPS import *

ds = Dataset('CPS')
ds.read_files(os.path.join(os.getcwd(), 'raw-dataset'))
ds.format_dataset(10)
ds.export_dataset(ds, os.path.join(os.getcwd(), 'CPS-Dataset'))
ds.convert_to_images(20)
ds.plot_categories(os.path.join(os.getcwd(), 'CPS-Dataset'))
ds.save_images(os.path.join(os.getcwd(), 'CPS-Dataset'))
ds.visualize_samples(os.path.join(os.getcwd(), 'CPS-Dataset', 'visualization-images'))
ds.log_image_dataset()