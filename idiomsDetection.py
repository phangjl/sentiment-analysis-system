import csv
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")

def lemma_all_items(doc):
    
     lemma_list = []
     
     lemma_list = [token.lemma_.strip().lower() for token in doc if token.is_digit==False and token.lemma_ != '-PRON-' and token.is_alpha == True ] 
#     for token in doc:
#        lemma_list.append(token.lemma_)
        
     updated_items = ' '.join(lemma_list)
     return updated_items


def convert_all_idioms():
    lemma_idiom_list = []
    for i in range(len(idiomsdataset)):
       lemma_idiom_list.append(lemma_all_items(nlp(idiomsdataset['idioms'][i])))
    return lemma_idiom_list


def check_idiom_list(sentence):
    
    for i in range (len(lemma_idiom_list)):     
        if lemma_idiom_list[i] in sentence:
            sentence = sentence.replace(lemma_idiom_list[i],idioms_sentiment_list[i])
            print(sentence)
    return sentence

def writefile(content,filename):
    with open(filename, 'w', newline='',encoding='utf-8') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerows(content)





cols=["idioms","sentiment"]
idiomsdataset = pd.read_csv('updated_idioms.csv',header=None, names=cols)
lemma_idiom_list = []
idioms_sentiment_list = idiomsdataset['sentiment']
lemma_idiom_list = convert_all_idioms()

def detectidoms(readFile,writeFile):
    result=[]    
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:
            row[0]= lemma_all_items(nlp(row[0]))
            result.append([check_idiom_list(row[0])])  #append the result
    
    writefile(result,writeFile)




#detectidoms('output_data/test_sentence_1.txt','output_data/test_sentence_1.txt')





