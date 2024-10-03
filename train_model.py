import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle


data = pd.read_csv('spam.csv', encoding='latin-1')[['v1', 'v2']]
data.columns = ['label', 'message']


data['label'] = data['label'].map({'ham': 0, 'spam': 1})

vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['message'])


y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


models = {
    "Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=200),
    "SVM": SVC(),
    "Random Forest": RandomForestClassifier(n_estimators=100)
}


for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{name} Model Accuracy: {accuracy}")

with open('spam_classifier_model.pkl', 'wb') as f:
    pickle.dump(models['Random Forest'], f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
