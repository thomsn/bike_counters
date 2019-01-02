import xlrd
import csv
import os
import datetime
import dateparser

INPUT_DATA_DIR = 'input_data'


location_corrections = {
    'ALEX': ['AlexS2', '1_ALEX', '1^ALEX'],
    'ORPY': ['2_ORPY', '2^ORPY', 'ORP_PoW3'],
    'COBY': ['ColByEL2', '3_COBY', '3^COBY', '3_COLBY'],
    'CRTZ':['4_CRTZ', '4^CRTZ', 'CNL RTZ_6892'],
    'LMET': ['5_LMET', '5^LMET'],
    'LLYN': ['6^LLYN', '6_LLYN'],
    'LBAY': ['7^LBAY', '7_LBAY'],
    'SOMO': ['8^SOMO', '8_SOMO'],
    'OYNG': ['9 OYNG', '9^OYNG', '9 OYNG 1'],
    'OGLD': ['10^OGLD'],
    'OBVW': ['11^OBVW', '11 OBVW'],
    'ADAWE BIKE': ['12a^ADAWE', 'ADAWE BIKE'],
    'ADAWE PED': ['ADAWE PED', '12b^ADAWE'],
    'PORTAGE': ['Portage Bridge', 'Portage'],
    'SOMO (westbound only)': ['8_SOMO (westbound only)'],
    'Date': ['Date']
}

location_correction_matrix = {}
for location in location_corrections:
    for incorrect_header in location_corrections[location]:
        location_correction_matrix[incorrect_header] = location

def correct_headers(header):
    header = header.strip()
    if header not in location_correction_matrix:
        raise Exception()

    return location_correction_matrix[header]

def process_line(headers, input_line):
    return {
        correct_headers(header): item for header, item in zip(headers, input_line) if
        '-' not in str(item)
        and 'Note' not in str(item)
        and str(item)
        and len(str(item)) < 40
        and 'Date' not in input_line
    }


data = []

for file_name in os.listdir(INPUT_DATA_DIR):
    wb = xlrd.open_workbook(os.path.join(INPUT_DATA_DIR, file_name))
    sh = wb._sheet_list[0]

    headers = None
    for rownum in range(sh.nrows):
        row_values = sh.row_values(rownum)
        if row_values[0] == 'Date':
            headers = row_values
        elif headers:
            maybe_line_data = process_line(headers, row_values)
            if maybe_line_data:
                data.append(maybe_line_data)

### FIXING DATE ###
for line in data:
    if '/' in str(line['Date']):
        line['Date'] = datetime.datetime.strptime(line['Date'], "%d/%m/%Y")
    elif type(line['Date']) == str and len(line['Date'].split(' ')) == 4:
        line['Date'] = dateparser.parse(line['Date'])
    else:
        line['Date'] = datetime.date(1900, 1, 1) + datetime.timedelta(int(line['Date']))
    date = str(line['Date'].isoformat())
    if 'T' in date:
        date = date.partition('T')[0]
    line['Date'] = date

### SORT BY DATE ###
data = sorted(data, key=lambda x: x['Date'])

keys = {}
for obj in data:
    for key in obj.keys():
        if key in keys:
            keys[key] += 1
        else:
            keys[key] = 1

### Publish ###
with open('ottawa_bike_counters.csv', 'w+') as output_file:
    keys = list(keys.keys())
    keys.remove('Date')
    keys = ['Date'] + sorted(keys)
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
