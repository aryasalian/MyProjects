import numpy as np
import pandas as pd
import json
from flask import Flask, request
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from newsapi import NewsApiClient
import time
from flask import Flask, request
from flask_cors import CORS, cross_origin
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class news:
    def __init__(self, title, desc, source):
        self.title = title
        self.desc = desc
        self.source = source
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route('/veritas')
def increment_model():
            listnews = [] 
            args = request.args
            val = args.get('news')
            df = pd.DataFrame([val])
            value_list = [row[0] for row in df.itertuples(index=False, name=None)]
            cv = CountVectorizer(stop_words='english')
            x_train = cv.fit_transform(value_list)
            qstr = ''
            for key in cv.vocabulary_.keys():
                qstr = qstr + ' AND '+key
            query = qstr[5:len(qstr)]
            newsapi = NewsApiClient(api_key='0d7678cab9444a85aba6d0b93a420dd3')
            listOfNews = newsapi.get_everything(q=query, language='en')
            print('--------------START------------')
            hits = 0
            allKeys = 0
            keyHit = 0
            totalKeys = 0
            allnews = 0
            allFound = 0
            for each in listOfNews['articles']:
                    eachSource = each['source']
                    eachnews = { 'title' : each['title'], 'description' : each['description'], 'source' : eachSource['name']}
                    listnews.append(eachnews)
                    allKeys = 0
                    hits = 0
                    allnews += 1
                    for key in cv.vocabulary_.keys():
                            allKeys += 1 
                            totalKeys += 1
                            print(each['description'])
                            description = each['description'].lower()
                            print('=========>')
                            print(key)
                            key = key.lower()
                            if(description.find(key) != -1):
                                print('found')
                                hits += 1
                                keyHit += 1
                            else:
                                print('not found')
                    if(hits==allKeys):
                        print('all found')
                        allFound += 1

            print('-----------------Result----------------------')
            print('Number of hits '+str(keyHit))
            print('All combinations '+str(totalKeys))
            print('All keys found ' + str(allFound))
            print('All news '+str(allnews))
            x =  '{ "allKeyFound": '+str(allFound)+', "allNews": '+str(allnews)+',"news": '+json.dumps(listnews)+'}'
            y = x
            return y


def validate(news):
            listnews = [] 
            args = request.args
            val = news
            df = pd.DataFrame([val])
            value_list = [row[0] for row in df.itertuples(index=False, name=None)]
            cv = CountVectorizer(stop_words='english')
            x_train = cv.fit_transform(value_list)
            qstr = ''
            for key in cv.vocabulary_.keys():
                qstr = qstr + ' AND '+key
            query = qstr[5:len(qstr)]
            newsapi = NewsApiClient(api_key='0d7678cab9444a85aba6d0b93a420dd3')
            listOfNews = newsapi.get_everything(q=query, language='en')
            
            hits = 0
            allKeys = 0
            keyHit = 0
            totalKeys = 0
            allnews = 0
            allFound = 0
            for each in listOfNews['articles']:
                    eachSource = each['source']
                    eachnews = { 'title' : each['title'], 'description' : each['description'], 'source' : eachSource['name']}
                    listnews.append(eachnews)
                    allKeys = 0
                    hits = 0
                    allnews += 1
                    for key in cv.vocabulary_.keys():
                            allKeys += 1 
                            totalKeys += 1
                            print(each['description'])
                            description = each['description'].lower()
                            print('=========>')
                            print(key)
                            key = key.lower()
                            if(description.find(key) != -1):
                                print('found')
                                hits += 1
                                keyHit += 1
                            else:
                                print('not found')
                    if(hits==allKeys):
                        print('all found')
                        allFound += 1

            
            x =  '{ "allKeyFound": '+str(allFound)+', "allNews": '+str(allnews)+',"news": '+json.dumps(listnews)+'}'
            if(allFound > 0):
                y = "This is most probably a real news"
            else:
                y = "fake news"
            return y

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        body = request.values.get("Body")
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing NumMedia parameter", 400
    response = MessagingResponse()
    if not body:
        msg = response.message("Send us a fact/news you want to validate")
    else:
        msg = response.message(validate(body))
    return str(response)

if __name__ == '__main__':
   app.run(host='0.0.0.0')

            

