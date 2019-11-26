import pandas as pd
import numpy as np
import csv

### HELPERS
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

#get the maximum agreement
def maxagreement(answers):
  result = []
  temp = set(answers)
  for i in temp:
    result.append(answers.count(i))
  return(max(result))

#max of the begining position and the ending position agreement divided by IS length
def posagreement(answers,text):
  beginlist = []
  endlist = []
  for answer in answers:
    answer = str(answer)
    beginlist.append(text.find(answer))
    endlist.append(text.find(answer)+ len(answer.split()) - 1)
  return((maxagreement(beginlist)+ maxagreement(beginlist))/(2*len(text.split())))

### SCRIPT
#read document
xls = pd.ExcelFile('rules_data_codifying.xlsx')
coders = xls.sheet_names[1:11]
Master = xls.parse(0)
columns = Master.to_dict('split')['columns']

#read each sheet
full_dict = {}
x = 1
for x, coder in enumerate(coders):
  sheet = xls.parse( x+1 )
  full_dict[coder] =  sheet.to_dict('index')

dic_size = len(full_dict['Statements_Arti'])
fieldnames_in = ['Text Type', 'Institution Type', 'Rule/Norm/Strategy', 'Level of Analysis',
                 'Attribute', 'Deontic', 'aIm', 'oBject', 'Or Else', 'Condition']
fieldnames_out = ['Text Type', 'Institution Type', 'Rule/Norm/Strategy', 'Level of Analysis',
                  'Attribute_lo', 'Attribute_hi', 'Attribute_position', 'Deontic_lo', 'Deontic_hi', 'Deontic_position',
                  'aIm_lo', 'aIm_hi', 'aIm_position', 'oBject_lo', 'oBject_hi', 'oBject_position', 'Or Else_lo', 'Or Else_hi',
                  'Or Else_position','Condition_lo', 'Condition_hi', 'Condition_position']
ABDICO = ['Attribute', 'Deontic', 'aIm', 'oBject', 'Or Else', 'Condition']
# build output
with open('compare.csv',mode ='w') as compare_file:
    compare_writer = csv.DictWriter(compare_file, fieldnames = fieldnames_out)
    compare_writer.writeheader()
    for i in range(0,dic_size):
        row = {}
        for item in fieldnames_in:
            answers = []
            for coder in coders:
                answers.append(full_dict[coder][i][item])
            if item in ABDICO:
                row[item+'_hi']= upper_bound(answers)
                row[item+'_lo']= maxagreement(answers)/len(answers)
                row[item+'_position'] = posagreement(answers, full_dict[coder][i]['Institutional Statement'])
            else:
                row[item]= maxagreement(answers)/len(answers)
        compare_writer.writerow(row)
