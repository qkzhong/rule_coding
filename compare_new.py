import pandas as pd
import numpy as np
import csv
import statistics
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
xls = pd.ExcelFile('rules_data_codifying_build_week2.xlsx')
sheet_names = xls.sheet_names
coders = ['OWEN', 'STEPHEN', 'caitlyn', 'WEISMAN', 'chris','WANG', 'Irizarry', 'DEA','SAHNI','NAOMI','FERNANDEZ']
Master = xls.parse(0)
columns = Master.to_dict('split')['columns']
Master = Master.to_dict('index')

#read each sheet
full_dict = {}
x = 0
for x, sheet_name in enumerate(sheet_names, start=0):
  if sheet_name.startswith('statements_r_build_') and sheet_name.split('_')[3] in coders:
    sheet = xls.parse( x )
    full_dict[sheet_name] =  sheet.to_dict('index')
    print(sheet_name)

dic_size = len(full_dict['statements_r_build_OWEN'])
fieldnames_in = ['text_type']
fieldnames_out = ['text_type_IRR','text_type_diversity','text']

IRR = []
Diversity = []

# build output
with open('compare_new_week2.csv',mode ='w') as compare_file:
    compare_writer = csv.DictWriter(compare_file, fieldnames = fieldnames_out)
    compare_writer.writeheader()
    for i in range(100,199): #loop through rows
        row = {}
        for item in fieldnames_in:
            answers = []
            for coder in coders:
                #print( coder, i, item )
                #print( len(full_dict['statements_'+coder]) )
                answer = full_dict['statements_r_build_'+coder][i][item]
                if type(answer) != type(np.nan):
                    answers.append(answer)
            is_empty = all([ (type(answer) == type(np.nan) ) for answer in answers ])
            if is_empty:
                continue
            #print(answers)
        row[item + '_IRR']= maxagreement(answers)/len(answers)
        IRR.append(row[item + '_IRR'])
        row[item + '_diversity'] = len(set(answers))
        Diversity.append(row[item + '_diversity'])
        row['text']= full_dict['statements_r_build_'+coder][i]['text']
        compare_writer.writerow(row)
print("Mean of IRR is: ", statistics.mean(IRR))
print("Median of IRR is: ", statistics.median(IRR))
print("Mean of Diveristy is: ", statistics.mean(Diversity))
print("Median of Diveristy is: ", statistics.median(Diversity))
