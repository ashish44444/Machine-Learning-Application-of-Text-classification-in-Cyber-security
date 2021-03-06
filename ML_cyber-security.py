import csv
import requests
import json
import urllib.request as r
from _datetime import time, datetime
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#For exception handling such as if page is not there
def request_until_succeed(url):
    req = r.Request(url)
    success = False
    while success is False:
        try: 
            response = r.urlopen(req)
            if response.getcode() == 200:
                
                success = True
        except Exception:
            print(Exception)
            time.sleep(5)
            
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return response.read().decode('utf-8')

#will be generated by Facebook API developer.facebook.com
app_id = "xxxxxxxxxxxxxx"
app_secret = "XXXXXXXXXXXXXXXXXXXXXXXXX" # DO NOT SHARE WITH ANYONE!
access_token = app_id + "|" + app_secret

#Text file containing facebook page id like newyork times is Nytimes
f = open('project1.txt','r')
message = f.readlines()
grades = []
for i in range(len(message)):
    grades.append(message[i].strip('\n'))

Headline = [] 
comm = []   


for x in range(0,len(grades)): 
    #Url generation, limit in Url that is limit(50%) this will load 50% of page data
    url = "https://graph.facebook.com/v2.4/"+grades[x]+"/?fields=posts.since(1406851200).limit(40)%7Bcreated_time%2Cmessage%2Ccomments.limit(2000)%7Bcreated_time%2Cmessage%7D%7D&access_token="
    html = url + access_token
    print(html) # you can get the Url and browsing that url you will get json format data that will help
    #in fetching data and comments
    data = json.loads(request_until_succeed(html))
    
    #Appendng headlines
    Headline.append([])    
    for i in range(0,len(data['posts']['data'])):
        if(data['posts']['data'][i].get('message')):
        
            {   
                Headline[x].append(data['posts']['data'][i]['message'])
                }
    
    #Appending comments
    comm.append([])
    for j in range(0,len(data['posts']['data'])):
        for k in range(0,len(data['posts']['data'][j]['comments']['data'])):
                {
                    comm[x].append((data['posts']['data'][j]['comments']['data'][k]['message']).encode('utf-8'))
                    }           

#load comments to CSV file
for i in comm:
    my_df = pd.DataFrame(i)
    my_df.to_csv('fb_comments1.csv', index=False,header = ['comments'])

#Read csv file with labled data
dataset = pd.read_csv('final_dataset.csv')
X = dataset.iloc[:, 0].values
y = dataset.iloc[:, 1].values

#Apply reguler expression
corpus = []
for i in range(0,len(X)):
        review = re.sub('[^a-zA-Z]', ' ', X[i]) # remove other than alphabets
        review = review.lower()  # convert to lower case
        review = review.split()  # split the data
        ps = PorterStemmer()     # stem the data
        # Remove stopwords
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review) # join the words
        corpus.append(review)   # Append to corpus

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = None)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values
    
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = None)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

#SVM classifier
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Fitting Random Forest Classification to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Fitting Decision Tree Classification to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Fitting K-NN to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 2, metric = 'minkowski', p = 2)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

