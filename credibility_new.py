#credibitily
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
  if result != []:
      return(max(result))
  else:
      return(0)

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
xls = pd.ExcelFile('rules_data_codifying_build.xlsx')
sheet_names = xls.sheet_names
coders = ['OWEN', 'STEPHEN', 'caitlyn', 'WEISMAN', 'chris','WANG', 'Irizarry', 'DEA']
Master = xls.parse(0)
columns = Master.to_dict('split')['columns']
Master = Master.to_dict('index')

#read each sheet
full_dict = {}
x = 1
for x, sheet_name in enumerate(sheet_names, start=1):
  if sheet_name.startswith('statements_r_build_') and sheet_name.split('_')[3] in coders:
    sheet = xls.parse( x )
    full_dict[sheet_name] =  sheet.to_dict('index')
    print(sheet_name)


dic_size = len(full_dict['statements_r_build_OWEN'])
fieldnames_in = ['text_type']
fieldnames_out = ['agreement','model_improvement','text']
#ABDICO = ['Attribute', 'Deontic', 'aIm', 'oBject', 'Or Else', 'Condition']
# build output
for coder in coders:
    outputname = 'credibility_' + coder + '.csv'
    with open(outputname,mode ='w') as credibility_file:
        credibility_writer = csv.DictWriter(credibility_file, fieldnames = fieldnames_out)
        credibility_writer.writeheader()
        for i in range(0,dic_size):
            row = {}
            row['text']= full_dict['statements_r_build_'+coder][i]['text']
            for item in fieldnames_in:
                answers = []
                others = []
                for coderx in coders:
                    #print( coder, i, item )
                    #print( len(full_dict['statements_'+coder]) )
                    answer = full_dict['statements_r_build_'+coderx][i][item]
                    if type(answer) != type(np.nan):
                        answers.append(answer)
                        if coderx != coder:
                            others.append(answer)
                is_empty = all([ (type(answer) == type(np.nan) ) for answer in answers ])
                others_empty = all([ (type(answer) == type(np.nan) ) for answer in others ])
                if is_empty:
                    continue
                print(answers)
                if others_empty:
                        row[item]= 0
                else:
                        row['agreement']= others.count(full_dict['statements_r_build_'+coder][i][item])/len(coders)
                        row['model_improvement']= maxagreement(others)/len(others) - maxagreement(answers)/len(coders)
            credibility_writer.writerow(row)
