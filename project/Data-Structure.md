# Data Structure and Processing

Each csv file is loaded into an array. Each entry has the shape(3,)

The Overall File Shapes are as follows:
* Bad Connection:
* Blocked 1: (2539, 3)
* Blocked 2: (1543, 3)
* DoS Attack: (3166, 3)
* High Blocked: (19300, 3)
* Hits 1: (3570, 3)
* Hits 2: (2910, 3)
* Hits 3: (3020, 3)
* Normal: (232870, 3)
* Plastic Bag: (, 3)
* Poly 2: (8641, 3)
* Poly 7: (7430, 3)
* Second Blocked: (57111, 3)
* Spoofing: (232870, 3)
* Wet Sensor: (1670, 3)

As we can see the normal dataset is the largest, followed by the plastic bag.
To combat the issue of having unequal sample sizes, we will add entries of 
['0', '0', '0'] 
into the datasets, so the input shape of each sample is the same size.
