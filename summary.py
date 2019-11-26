import csv, statistics

#read file
with open('compare.csv', 'r') as f:
  reader = csv.reader(f)
  my_list = list(reader)
#transpose the list
t_list = list(map(list, zip(*my_list)))

fieldnames = ['variable','mean','median']
with open('summary.csv',mode ='w') as summary_file:
    summary_writer = csv.DictWriter(summary_file, fieldnames = fieldnames)
    summary_writer.writeheader()
    for list in t_list:
        col = list[0]
        value = [float(i) for i in list[1:]]
        mean = statistics.mean(value)
        median = statistics.median(value)
        summary_writer.writerow({'variable':col, 'mean': mean, 'median': median})
