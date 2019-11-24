import pandas as pd
import numpy as np
import csv

#unique transformed in python
def unique(list):
    x = np.array(list)
    return(np.unique(x))

#upper bound function
def upper_bound(answers):
  answers_by_word = []
  for answer in answers:
    answer = str(answer)
    answers_by_word.extend( unique( answer.split(" ") ) )
  temp = set(answers_by_word)
  result = []
  for i in temp:
    result.append(answers_by_word.count(i))
  if result == []:
      return(0)
  else:
      return(max(result)/len(answers))

def agreement(answers):
  result = []
  temp = set(answers)
  for i in temp:
    result.append(answers.count(i))
  return(max(result)/len(answers))

#read document
xls = pd.ExcelFile('rules_data_codifying.xlsx')
coders = xls.sheet_names[1:11]
Master = xls.parse(0)
columns = Master.to_dict('split')['columns']

#read each sheet
full_dict = {}
x = 1
for coder in coders:
  sheet = xls.parse(x)
  full_dict[coder] =  sheet.to_dict('index')
  x = x + 1

dic_size = len(full_dict['Statements_Arti'])
fieldnames = ['Text Type', 'Institution Type', 'Rule/Norm/Strategy', 'Level of Analysis', 'Attribute', 'Deontic', 'aIm', 'oBject', 'Or Else', 'Condition']
ABDICO = ['Attribute', 'Deontic', 'aIm', 'oBject', 'Or Else', 'Condition']
with open('compare.csv',mode ='w') as compare_file:
    compare_writer = csv.DictWriter(compare_file, fieldnames = fieldnames)
    compare_writer.writeheader()
    for i in range(0,dic_size):
        row = {}
        for item in fieldnames:
            answers = []
            for coder in coders:
                answers.append(full_dict[coder][i][item])
            if item in ABDICO:
                row[item]= upper_bound(answers)
            else:
                row[item]= agreement(answers)
        compare_writer.writerow(row)

