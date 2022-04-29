import re
import unicodedata
import emoji
import spacy
import csv
import string
nlp = spacy.load('en_core_web_sm')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
#remove accents
#remove URL 
#remove HTML tag
#remove @username
#tokenization
#remove stopwords
#remove punctuation
#convert to lowercase
#apply lemmatizer
#emoji



def clean_url(text):
   cleanr = re.compile('(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*')
   cleantext = re.sub(cleanr,'', text)
   return cleantext

def clean_html(text): 
   cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
   cleantext = re.sub(cleanr,'', text)
   return cleantext

def clean_username(text): 
   cleanr = re.compile('@[^\s]+')
   cleantext = re.sub(cleanr, '', text)
   return cleantext

def strip_accents(text):
   return ''.join(c for c in unicodedata.normalize('NFD', text) if not unicodedata.combining(c))

def clean_punc(text):
    punctuation = "!@#$%^&*()_+=[]{}:\|/<>?:.-,;"
    for c in text:
         if c in punctuation:
             text = text.replace(c,' ')
    return text

def replace_emoji(text):
    return emoji.demojize(text, delimiters=("", "")) 




def tokenization(text):   
    # put the commnet into spacy model 
    sentence = nlp(text)
    #data pre-processing 
    #tokenization and lemmatization and lowercase the text and remove digit
    text = [token.lemma_.strip().lower() for token in sentence if token.is_digit==False and token.lemma_ != '-PRON-' and token.is_alpha == True ] 
        #make it token become sentence
    sentence_text =' '.join(text)
    return sentence_text

def name_en_rec(text):
    doc = nlp(text)
    for ent in doc.ents:
        text = text.replace(ent.text,ent.label_)
    return text



def sentence_cleaner(text):
    lemmatizer=WordNetLemmatizer()
    #regex for @mention detection
    mention_regex = r'@[A-Za-z0-9_]+'
    #regex for links detection
    http_regex = r'https?://[^ ]+'
    www_regex = r'www./[A-Za-z0-9-]+./[A-Za-z][ ]'
    bom_removing = "ï¿½"
    string.punctuation = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
    combined_regex = r'|'.join((mention_regex, http_regex))
    #negation dictionnary
    negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                    "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                    "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                    "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                    "mustn't":"must not"}
    neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

    tokenized_list = []
    soup = BeautifulSoup(text,"lxml")
    souped = soup.get_text()
    
    try:
        bom_removed = souped.replace(bom_removing, "?")
    except:
        bom_removed = souped
        
    #remove noise
    stripped = re.sub(combined_regex, '', bom_removed)
    stripped = re.sub(www_regex, '', stripped)
    stripped = re.sub(r'\d+', '', stripped)
    stripped = replace_emoji(text)
    #lowercasing
    lower_case = stripped.lower()
    
    #replace negation word 
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
    
    text_handled = ' '.join(word.strip(string.punctuation) for word in neg_handled.split())
       
    text_handled = word_tokenize(text_handled)
   
    for word in text_handled:
        tokenized_list.append(lemmatizer.lemmatize(word,pos = "v"))

    return ' '.join(tokenized_list)






   
 
def processdata(text):
    text = clean_html(text)
    text = clean_url(text)
    text = clean_username(text)
    text = strip_accents(text)
    text = replace_emoji(text)
    text = clean_punc(text)
#   text = name_en_rec(text)
    text = tokenization(text)
   
    return text

def data_cleaning(text):
    text = clean_username(text)
    text = clean_punc(text)
    text=re.sub('[0-9]+','',text)
    text=text.lower() #lowercasing
    text = clean_url(text)
    text = replace_emoji(text)
    return text 




def process(readFile,writeFile):
    conl=[]
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:
            
            row[0] = processdata(row[0])
            print(row[0])
            conl.append([row[0]])
                    
    with open(writeFile, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(conl)      


def process1(readFile,writeFile):
    conl=[]
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:
            
            row[0] = data_cleaning(row[0])
            print(row[0])
            conl.append([row[0]])
                    
    with open(writeFile, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(conl)      



def process2(readFile,writeFile):
    conl=[]
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:
            
            row[0] = sentence_cleaner(row[0])
            print(row[0])
            conl.append([row[0]])
                    
    with open(writeFile, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(conl)    



def takefile(readFile,writeFile):
    conl1=[]
    with open(readFile,encoding='utf-8') as txtfile:
        readtxt = csv.reader(txtfile, delimiter='\n')
        for row in readtxt:
            conl1.append([row[0]])
                    
    with open(writeFile, 'w', newline='',encoding='utf-8') as txtfile:
        writer = csv.writer(txtfile)
        writer.writerows(conl1)      
            

