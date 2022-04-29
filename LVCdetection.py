
#import the spacy library
import spacy
import csv
from spacy.matcher import Matcher
#load the dictionary model
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)



def writefile(content,filename):
    with open(filename, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        #sort the data from nested list
        #result=(sorted(result, key=operator.itemgetter(0)))
        writer.writerows(content)



# light verb detection
def extract_full_name(string,filename):
     nlp_doc= nlp(string)  
     #put the sentences
     matches = matcher(nlp_doc)
     for match_id, start, end in matches:
         verb = nlp_doc[start]
         span = nlp_doc[start:end]
         if verb.text == 'do' or verb.text == 'get' or verb.text =='give' or verb.text =='have' or verb.text =='make' or verb.text =='take':
             with open(filename) as csvfile:
                 readCSV = csv.reader(csvfile, delimiter=',')
                 for row in readCSV:
                     if span.text == row[0]:
                         string= string.replace(span.text,row[1])
                         print(string)
                
             csvfile.close    
     
     return string
                        

# tokenization each comment one by one
def data_processing(string):        
        # put the commnet into spacy model 
        sentence = nlp(string)
        #data pre-processing 
        #tokenization and lemmatization and lowercase the text  
        text = [token.lemma_.strip().lower() for token in sentence if token.lemma_ != '-PRON-' 
            and token.dep_ != "punct" and token.pos_ != "SYM" and token.is_digit==False and token.is_alpha == True] 
        #make it token become sentence
        sentence_text =' '.join(text)
        return sentence_text
        

#rule based approach
#declara the pattern
pattern = [{'POS': 'VERB'}, {'POS': 'DET','OP':'*'}, {'POS': 'ADP','OP':'?'},{'POS': 'ADV','OP':'?'},{'POS': 'ADJ','OP':'*'},{'POS': 'NOUN','OP':'+'}]
pattern1 = [{'POS': 'AUX'}, {'POS': 'DET','OP':'*'}, {'POS': 'ADP','OP':'?'},{'POS': 'ADV','OP':'?'},{'POS': 'ADJ','OP':'*'},{'POS': 'NOUN','OP':'+'}]
# put the pattern into mathcher 
matcher.add('light_verb', None, pattern)
matcher.add('light_verb', None, pattern1)
def detectLVC(readFile,writeFile):
    result=[]
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:
            data_lemma = data_processing(row[0]) # process the tokenization and lemmatization
            data_convert = extract_full_name(data_lemma,'LVC.csv') # POS tagging by rule based approach technique
            result.append([data_convert])  #append the result
    
    writefile(result,writeFile)
        
        
#detectLVC('uploaded_data/test_sentence_1.txt','output_data/test_sentence_1.txt')











