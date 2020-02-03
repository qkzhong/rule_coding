#credibitily
import pandas as pd
import numpy as np
import csv
import operator
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
def RSOH(answers):
  temp = set(answers)
  history = {}
  for i in temp:
    history[i]= answers.count(i)
  if history != {}:
    return(max(history.items(), key=operator.itemgetter(1)))
  else:
    return(0,0)

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
print(sheet_names)
coders = ['OWEN', 'STEPHEN', 'caitlyn', 'WEISMAN', 'chris','WANG', 'Irizarry', 'DEA','SAHNI','FERNANDEZ','NAOMI']
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
fieldnames_out = ['agreement','RSOH','text']
#ABDICO = ['Attribute', 'Deontic', 'aIm', 'oBject', 'Or Else', 'Condition']
credibility_sum = {'coder':[],
                   'item':[],
                   'agreement':[],
                   #'model_improvement':[],
                   'RSOH':[]}
# build output
for coder in coders:
    outputname = 'credibility_' + coder + '.csv'
    with open(outputname,mode ='w') as credibility_file:
        credibility_writer = csv.DictWriter(credibility_file, fieldnames = fieldnames_out)
        credibility_writer.writeheader()
        for i in range(0,199):
            row = {}
            row['text']= full_dict['statements_r_build_'+coder][i]['text']
            for item in fieldnames_in:
                answers = []
                others = []
                for coderx in coders:
                    answer = full_dict['statements_r_build_'+coderx][i][item]
                    if type(answer) != type(np.nan):
                        answers.append(answer)
                        if coderx != coder:
                            others.append(answer)
                is_empty = all([ (type(answer) == type(np.nan) ) for answer in answers ])
                others_empty = all([ (type(answer) == type(np.nan) ) for answer in others ])
                if is_empty:
                    continue
                if i == 3 and coder == 'STEPHEN':
                    print('answers', answers,len(answers), full_dict['statements_r_build_'+coder][i][item])
                    print('others',others, others.count(full_dict['statements_r_build_'+coder][i][item]))
                    print(others.count(full_dict['statements_r_build_'+coder][i][item])/len(others))
                    print(RSOH(answers), full_dict['statements_r_build_'+coder][i][item])
                if others_empty:
                        row['agreement']= 0
                        #row['model_improvement'] = 0
                        row['RSOH'] = 'NA'
                else:
                        row['agreement']= others.count(full_dict['statements_r_build_'+coder][i][item])/len(others)
                        #row['model_improvement']= RSOH(answers)[1]/len(coders) - RSOH(others)[1]/len(others)
                        row['RSOH'] = full_dict['statements_r_build_'+coder][i][item] == RSOH(answers)[0]
            #summary data
                credibility_sum['coder'].append(coder)
                credibility_sum['item'].append(item)
                credibility_sum['agreement'].append( others.count(full_dict['statements_r_build_'+coder][i][item])/len(others))
                credibility_sum['RSOH'].append(row['RSOH'])
            #write independent
                credibility_writer.writerow(row)

dfcred = pd.DataFrame(credibility_sum)
summary = dfcred.groupby('coder').aggregate({'agreement': ['mean','median'],
                            # 'model_improvement': ['mean','median'],
                             'RSOH':'sum'})
print(summary)
export_csv = summary.to_csv (r'credibility_summary_all.csv', index = True, header=True)
