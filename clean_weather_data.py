import os
import csv

INPUT_DATA_DIR = 'weather'

def fix_header(headr):
    for re in ['/', ' ', '(', ')', '°C']:
        headr = headr.replace(re, '')
    return headr

data = []
for file_name in os.listdir(INPUT_DATA_DIR):
    with open(os.path.join(INPUT_DATA_DIR, file_name), 'r') as f:
        reader = csv.reader(f)
        headers = None
        for row in reader:
            if row and row[0] == 'Date/Time':
                headers = row
                continue
            if headers:
                if len(row) != len(headers):
                    raise Exception('shit')
                else:
                    data.append({fix_header(label): sample for label, sample in zip(headers, row)})

keys = {}
for obj in data:
    for key in obj.keys():
        keyc = key
        if keyc in keys:
            keys[keyc] += 1
        else:
            keys[keyc] = 1


data = sorted(data, key=lambda x: x['DateTime'])

### Publish ###
with open('ottawa_weather.csv', 'w+') as output_file:
    keys = list(keys.keys())
    keys.remove('DateTime')
    keys = ['DateTime'] + sorted(keys)
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data) 

