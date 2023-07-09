import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from newsapi.newsapi_client import NewsApiClient
import time

val=input('enter news')
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

