import csv
import dateutil.parser

data2 = list(csv.reader(open('./ottawa_bike_counters.csv')))

data1 = list(csv.reader(open('ottawa_weather.csv')))

data_map = {line[0]: line[1:] for line in data1[1:]}


data2[0].extend(data1[0][1:])
for line in data2[1:]:
    if line[0] in data_map:
        line.extend(data_map[line[0]])
    else:
        print('removing', line[0])

data2[0].append('Weekday')
for line in data2[1:]:
    date = dateutil.parser.parse(line[0])
    line.append(str(date.weekday()))

with open('bike_n_weather.csv', 'w+') as f:
    for line in data2:
        f.write(','.join(line))
        f.write('\n')