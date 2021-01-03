# CPS-Research
A home for the figures of the Data Mining for Anomaly Detection in Cyber-Physical Systems. Home to the projects research using Convolutional Neural Networks to perform anomaly dectection in cyber physical systems. This repository also holds the dataset used, as well as some other tools used to use and visualize the data. More information about the dataset will be provided below.

## Installation
Create a virtual environment and install the dependencies using the requirements.txt file. Here is the installation procedure if you would like to build a copy of the system using the data yourself. Installation in this case is assumed for Linux users, it is also assumed you are using python3 and it is already installed.

```bash
    # Clone the github repository
    git clone https://github.com/jzaunegger/CPS-Research

    # Navigate into the repository
    cd CPS-Reseach    

    # Create venv
    python3 -m venv venv

    # Source venv
    source venv/bin/activate

    # Install Requirements
    pip install -r requirements.txt

    # Run Python Projects Here

    # Leave the venv
    deactivate
```

## Usage
In the dev folder there are several Python scripts meant to be used for this project. This section outlines the function of each script.
* Convert-Image-To-Pickle.py
    * This script will read the generated images from a folder, and save that data as a pickle object.

* Convert-To-Images.py
    * Read the formatted data, and convert the data to images using the values to represent RGB values.

* Format-Dataset.py
    * Read the dataset from various csv files, each contain an entry for the timestamp, sensor id, and sensor value. The timestamp is then converted to the amount of UTC seconds. This data is then saved to a new folder.

* HelperFunctions.py
    * A variety of functions used by the other scripts.

* Visualize-Images.py
    * Function to read the images, and create a sample image showcasing the appearance of the formatted images.

## Dataset
The included dataset comes from Pedro Merino Laso, David Brosset, and John Puentes in "Dataset of anomalies and malicious acts in a cyber-physical system", released in October of 2017. This dataset is temporal series collected from a series of tanks that regulate the amount of liquid between the two. The data is collected from the sensors in the pumps as well as other sensors that measure the volume of water in the tanks. 

Here is a link to the dataset where I found it at.
[CPS Dataset](https://www.sciencedirect.com/science/article/pii/S2352340917303402?via%3Dihub)