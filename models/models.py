import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


df = pd.read_csv('cleaned.csv')


X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)


dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)
file=open('DecisionTree1.pkl', 'wb')
pickle.dump(dt_model,file)



lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
file1=open('LogisticRegresion.pkl', 'wb')

pickle.dump(lr_model,file1)



svm_model = SVC()
svm_model.fit(X_train, y_train)
file3=open("svm.pkl","wb")
pickle.dump(svm_model,file3)

print("All Models Saved Successfully")