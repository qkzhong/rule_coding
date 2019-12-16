import pandas as pd
import numpy as np
import csv
#import coding_helper


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
def posagreement(answers,text,n):
  beginlist = []
  endlist = []
  for answer in answers:
    answer = str(answer)
    beginlist.append(text.find(answer))
    endlist.append(text.find(answer)+ len(answer.split()) - 1)
  return((maxagreement(beginlist)+ maxagreement(beginlist))/(2*n))

### SCRIPT
#read document
xls = pd.ExcelFile('rules_data_codifying.xlsx')
sheet_names = xls.sheet_names
coders = ['Arti', 'B', 'Qiankun', 'William', 'FREY', 'Caitlyn', 'MichaelA']
Master = xls.parse(0)
columns = Master.to_dict('split')['columns']
Master = Master.to_dict('index')

#read each sheet
full_dict = {}
x = 1
for x, sheet_name in enumerate(sheet_names, start=1):
  if sheet_name.startswith('statements_') and sheet_name.split('_')[1] in coders:
    sheet = xls.parse( x )
    full_dict[sheet_name] =  sheet.to_dict('index')

dic_size = len(full_dict['statements_Arti'])
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
                #print( coder, i, item )
                #print( len(full_dict['statements_'+coder]) )
                answer = full_dict['statements_'+coder][i][item]
                if type(answer) != type(np.nan):
                    answers.append(answer)
            is_empty = all([ (type(answer) == type(np.nan) ) for answer in answers ])
            if is_empty:
                continue
            if item == "Text Type":
                print(answers)
            #print(answers)
            if item in ABDICO:
                row[item+'_hi']= upper_bound(answers)
                row[item+'_lo']= maxagreement(answers)/len(answers)
                row[item+'_position'] = posagreement(answers, Master[i]['Institutional Statement'], len(coders))
            else:
                row[item]= maxagreement(answers)/len(answers)
        compare_writer.writerow(row)
