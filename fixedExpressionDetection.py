

import csv
import pandas as pd


cols=["Fixed Expression","Simpler Word"]
fe_Dataset=pd.read_csv('FixedExpressionDataSet.csv', header=None, names=cols)
fixedExpression_list=fe_Dataset['Fixed Expression']
simplerWord_list=fe_Dataset['Simpler Word']


def check_FE_list(CleanSentences):
    for i in range(len(fixedExpression_list)):
        if fixedExpression_list[i] in str(CleanSentences):
            CleanSentences=CleanSentences.replace(fixedExpression_list[i],simplerWord_list[i])
    return CleanSentences

def writefile(content,filename):
    with open(filename, 'w', newline='',encoding='utf-8') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerows(content)


def detectFE(readFile,writeFile):
    result=[]    
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:            
            result.append([check_FE_list(row[0])])  #append the result
    
    writefile(result,writeFile)


#detectFE('output_data/test_sentence_1.txt','output_data/test_sentence_1.txt')



