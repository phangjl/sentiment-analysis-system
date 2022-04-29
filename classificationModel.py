
import pickle
import csv

svmclf = pickle.load(open("ModelPKl/lsvmmodel.pkl",'rb'))
NBclf = pickle.load(open("ModelPKl/NBmodel.pkl",'rb'))
rfclf = pickle.load(open("ModelPKl/rfmodel.pkl",'rb'))
Brtclf = pickle.load(open("ModelPKl/Brtclfmodel.pkl",'rb'))
tfidf= pickle.load(open("ModelPKl/vectorizer.pkl",'rb'))
#


def countemotion(predict):
    total = 0
    happiness = 0
    sadness = 0
    anger = 0
    fear = 0	
    disgust = 0
    surprise = 0 
    for index in predict:
        if index =="happiness":
            happiness= happiness+1
    
        elif index =="sadness":
            sadness= sadness+1
    
        elif index =="anger":
            anger= anger+1
    
        elif index =="fear":
            fear= fear+1
    
        elif index =="disgust":
            disgust= disgust+1
    
        elif index =="surprise":
            surprise= surprise+1
        total=total+1
    return total,happiness,sadness, anger, fear,disgust , surprise
 

def writefile(content,filename):
    with open(filename, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(content)
        
def storeResult(org_sentences, clean_sentences,predict):
    result = []
    result.append(['Original Sentence','Clean Sentence','Predicted Emotion'])
    i=0
    for index in predict:
        result.append([org_sentences[i],clean_sentences[i],predict[i]])
        i=i+1
    return result



def LSVMmmodel_predict(oriReadFile, readFile, writeFile):

    org_source_document= open(oriReadFile,"r",encoding='utf-8').read()
    org_sentences = org_source_document.split("\n")
        
    clean_source_document = open(readFile,"r",encoding='utf-8').read()
    clean_sentences = clean_source_document.split("\n")
        
    predict = svmclf.predict(tfidf.transform(clean_sentences))
        
    result = storeResult(org_sentences, clean_sentences,predict)
    
    writefile(result,writeFile)
    
    return countemotion(predict)

def NBmodel_predict(oriReadFile, readFile, writeFile):

    org_source_document= open(oriReadFile,"r",encoding='utf-8').read()
    org_sentences = org_source_document.split("\n")
        
    clean_source_document = open(readFile,"r",encoding='utf-8').read()
    clean_sentences = clean_source_document.split("\n")
        
    predict = NBclf.predict(tfidf.transform(clean_sentences))
        
    result = storeResult(org_sentences, clean_sentences,predict)
    
    writefile(result,writeFile)
    
    return countemotion(predict)

def RFmodel_predict(oriReadFile, readFile, writeFile):

    org_source_document= open(oriReadFile,"r",encoding='utf-8').read()
    org_sentences = org_source_document.split("\n")
        
    clean_source_document = open(readFile,"r",encoding='utf-8').read()
    clean_sentences = clean_source_document.split("\n")
        
    predict = rfclf.predict(tfidf.transform(clean_sentences))
        
    result = storeResult(org_sentences, clean_sentences,predict)
    
    writefile(result,writeFile)
    
    return countemotion(predict)



def Brtmodel_predict(oriReadFile, readFile, writeFile):

    org_source_document= open(oriReadFile,"r",encoding='utf-8').read()
    org_sentences = org_source_document.split("\n")
        
    clean_source_document = open(readFile,"r",encoding='utf-8').read()
    clean_sentences = clean_source_document.split("\n")
        
    predict = Brtclf.predict(tfidf.transform(clean_sentences))
        
    result = storeResult(org_sentences, clean_sentences,predict)
    
    writefile(result,writeFile)
    
    return countemotion(predict)




