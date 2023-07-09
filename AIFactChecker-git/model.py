import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def runModel(val):
    df=pd.read_csv('/home/ubuntu/news.csv')
    #Get shape and head
    df.shape
    df.head()
    labels=df.label
    labels.head()
    x_train,x_test,y_train,y_test=train_test_split(df['text'], labels, test_size=0.2, random_state=7)
    #Initialize a TfidfVectorizer
    tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)

    # Fit and transform train set, transform test set
    tfidf_train=tfidf_vectorizer.fit_transform(x_train) 
    
    test_x_set = pd.Series([val])
    test_y_set = pd.Series(['FAKE'])
    tfidf_test=tfidf_vectorizer.transform(test_x_set)

    # Initialize a PassiveAggressiveClassifier
    pac=PassiveAggressiveClassifier(max_iter=50)
    pac.fit(tfidf_train,y_train)

    # Predict on the test set and calculate accuracy
    y_pred=pac.predict(tfidf_test)
    #score=accuracy_score(y_test,y_pred)
    #print(f'Accuracy: {round(score*100,2)}%')
    output = np.array_str(y_pred)
    return output






