import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

df = pd.read_csv('dataset.csv')
#df.head()

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
X_train, X_test, y_train, y_test = train_test_split(df['Resume'], df['Category'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)

#print(X_train_counts)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#print(X_train_tfidf)
model = LinearSVC().fit(X_train_tfidf, y_train)

from sklearn.externals import joblib
filename='final_svm model.sav'
joblib.dump(model,filename)

filename="vect.joblib"
joblib.dump(count_vect,open(filename,"wb"))