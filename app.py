from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json
import keras
import os
from keras.models import load_model
import pickle
import tensorflow as tf


app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#load modal
mymodel = tf.keras.models.load_model('sq_inj.h5')
myvectorizer = pickle.load(open("vectorizer_cnn", 'rb'))  

@app.route("/")
def main():
    result=" "
    return render_template('app.html',result=result)


@app.route('/check',methods=['GET', 'POST']) 
def check():
  
    
    if request.method == 'POST':
        query = request.form['query']

    result=predict_sqli_attack(query)  
              
    return render_template('app.html',result=result)


def clean_data(input_val):

    input_val=input_val.replace('\n', '')
    input_val=input_val.replace('%20', ' ')
    input_val=input_val.replace('=', ' = ')
    input_val=input_val.replace('((', ' (( ')
    input_val=input_val.replace('))', ' )) ')
    input_val=input_val.replace('(', ' ( ')
    input_val=input_val.replace(')', ' ) ')
    input_val=input_val.replace('1 ', '1')
    input_val=input_val.replace(' 1', '1')
    input_val=input_val.replace("'1 ", "'1 ")
    input_val=input_val.replace(" 1'", " 1'")
    input_val=input_val.replace('1,', '1,')
    input_val=input_val.replace(" 2 ", " 1 ")
    input_val=input_val.replace(' 3 ', ' 1 ')
    input_val=input_val.replace(' 3--', ' 1--')
    input_val=input_val.replace(" 4 ", ' 1 ')
    input_val=input_val.replace(" 5 ", ' 1 ')
    input_val=input_val.replace(' 6 ', ' 1 ')
    input_val=input_val.replace(" 7 ", ' 1 ')
    input_val=input_val.replace(" 8 ", ' 1 ')
    input_val=input_val.replace('1234', ' 1 ')
    input_val=input_val.replace("22", ' 1 ')
    input_val=input_val.replace(" 8 ", ' 1 ')
    input_val=input_val.replace(" 200 ", ' 1 ')
    input_val=input_val.replace("23 ", ' 1 ')
    input_val=input_val.replace('"1', '"1')
    input_val=input_val.replace('1"', '"1')
    input_val=input_val.replace("7659", '1')
    input_val=input_val.replace(" 37 ", ' 1 ')
    input_val=input_val.replace(" 45 ", ' 1 ')

    return input_val


def predict_sqli_attack(query):
    
    input_val=query
    res = len(input_val.split())
    res2 = len(input_val.split('='))  
    print(input_val)
    print(res2)
    
    if res2 == res and res<=2:
        return "injected query seems to be safe"    

    input_val=clean_data(query)
    input_val=[input_val]

    input_val=myvectorizer.transform(input_val).toarray()
    input_val.shape=(1,4096)
    resultNum=mymodel.predict(input_val)    
        
    if resultNum>0.5:
        print(resultNum)
        print("ALERT :::: This can be SQL injection")
        result="ALERT :::: This can be SQL injection"

    elif resultNum<=0.5:
        print(resultNum)
        print("It seems to be safe")
        result="injected query seems to be safe"
            
    return result    

if __name__ == "__main__":
	app.run(debug=True, use_reloader=False)