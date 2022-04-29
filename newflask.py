import re
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
import TextPreprocessing as tp
import classificationModel as clfmodel
from LVCdetection import detectLVC
from fixedExpressionDetection import detectFE
from idiomsDetection import detectidoms
from vpDetection import detectVp
import math

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10


@app.route("/")
def home():
    return render_template('main.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
        
        # take file from the user and save into uploaded file and output file 
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
		tp.takefile('uploaded_data/'+ f.filename, 'output_data/'+ f.filename)
		fileName =re.sub('.txt', '', f.filename) 

		
        #take the file in the output file to process the mwe detection 
		mwe=""              
		if request.form.get('idm'):
                        mwe = mwe+"Idioms"
                        tp.process2('output_data/'+ f.filename, 'output_data/'+ f.filename)                                            
                        detectidoms('output_data/'+ f.filename, 'output_data/'+ f.filename)                                            

		if request.form.get('fe'):
                        mwe = mwe+ " Fixed Expression Construction "
                        tp.process1('output_data/'+ f.filename, 'output_data/'+ f.filename)                    
                        detectFE('output_data/'+ f.filename, 'output_data/'+ f.filename)             
      
		if request.form.get('lvc'):
                        mwe = mwe+" Light verb Construction"
                        tp.process('output_data/'+ f.filename, 'output_data/'+ f.filename)
                        detectLVC('output_data/'+ f.filename, 'output_data/'+ f.filename)
    
		if request.form.get('vp'):        
                        mwe = mwe+" Verb Particle "
                        tp.process('output_data/'+ f.filename, 'output_data/'+ f.filename)
                        detectVp('output_data/'+ f.filename, 'output_data/'+ f.filename)
		tp.process('output_data/'+ f.filename, 'output_data/'+ f.filename) #if user no choose any mwe detection then it will process the normal text preprocessing 
		
        
		
		# take the model choose to train data
		modelchooseresult=""
		modelchoose = request.form.get('modeltype')
		if str(modelchoose) == 'lsvm':
                        total,happiness,sadness, anger, fear,disgust , surprise = clfmodel.LSVMmmodel_predict('uploaded_data/' + f.filename,'output_data/'+ f.filename, 'output_data/result_' + fileName + '.csv')
                        modelchooseresult = 'Linear Support Vector Machine'
                        
                        
        
		elif str(modelchoose) == 'nb':
                         total,happiness,sadness, anger, fear,disgust , surprise = clfmodel.NBmodel_predict('uploaded_data/' + f.filename,'output_data/'+ f.filename, 'output_data/result_' + fileName + '.csv')
                         modelchooseresult = 'Naive Bayes'
            
		elif str(modelchoose) == 'rf':
                        total,happiness,sadness, anger, fear,disgust , surprise = clfmodel.RFmodel_predict('uploaded_data/' + f.filename,'output_data/'+ f.filename, 'output_data/result_' + fileName + '.csv')
                        modelchooseresult = 'Random Forest'
            
		elif str(modelchoose) == 'ensemble':
                        total,happiness,sadness, anger, fear,disgust , surprise = clfmodel.Brtmodel_predict('uploaded_data/' + f.filename,'output_data/'+ f.filename, 'output_data/result_' + fileName + '.csv')
                        modelchooseresult = 'Ensemble (bagging) with Random Forest'
                        
            
		#build the bar chart
		labels = ['happiness', 'sadness', 'surprise', 'fear','anger','disgust']
        
		values = [happiness,sadness , surprise, fear, anger, disgust ]
		max1= max(values)
		max1= roundup(max1)
		
        
        


        
        
		Result = pd.read_csv('output_data/result_'+fileName+'.csv')
		return render_template("result.html",result = [Result.to_html(index=False)],resultfile = modelchooseresult,mweChoose=str(mwe), total1= total,happiness1 = happiness,sadness1 = sadness,anger1= anger, fear1= fear,disgust1 = disgust , surprise1 = surprise, title='Sentiment Analysis result', max=max1, labels=labels, values=values, steps=10 )
		
		 
    
	
		
		
	

if __name__ == "__main__":
    app.run()