### BIKE COUNTERS ###

This repository is related to this dataset: http://data.ottawa.ca/dataset/bicycle-trip-counters-automated

##### Cleaning the dataset #####
The dataset found on open data is in a variety of formats. In order to simplify the dataset you can use the 
clean_data.py script. Simply:

- create a directory in this directory called 'input_data', 
- place all the .xls and .xlsx files from the dataset in that directory, 
- install the associated python packages for clean_data.py,
- call 'python clean_counter_data.py' or run the script with your own favorite method, 
- assuming everything went well, the results should be returned in the form of a file named 'ottawa_bike_counters.csv'.

The csv file can also be found at https://www.kaggle.com/m7homson/ottawa-bike-counters/home

Have fun visualizing!
