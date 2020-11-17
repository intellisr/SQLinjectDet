import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv("sqli.csv",encoding='utf-16')
vectorizer = CountVectorizer( min_df=2, max_df=0.7,max_features=4096,stop_words=stopwords.words('english'))
posts = vectorizer.fit_transform(df['Sentence'].values.astype('U')).toarray()

print(posts.shape)

transformed_posts=pd.DataFrame(posts)

df=pd.concat([df,transformed_posts],axis=1)

X=df[df.columns[2:]]

y=df['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer
from keras.wrappers.scikit_learn import KerasClassifier

input_dim = X_train.shape[1] 

model = Sequential()
model.add(layers.Dense(20, input_dim=input_dim, activation='relu'))
model.add(layers.Dense(10,  activation='tanh'))
model.add(layers.Dense(1024, activation='relu'))

model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', 
              optimizer='adam', 
              metrics=['accuracy'])
model.summary()

classifier_nn = model.fit(X_train,y_train,
                    epochs=10,
                    verbose=True,
                    validation_data=(X_test, y_test),
                    batch_size=15)

#save modal
model.save('sq_inj.h5')

print(X_test.shape)
pred=model.predict(X_test)

for i in range(len(pred)):
    if pred[i]>0.5:
        pred[i]=1
    elif pred[i]<=0.5:
        pred[i]=0

print(accuracy_score(y_test,pred))

with open('vectorizer_cnn', 'wb') as fin:
    pickle.dump(vectorizer, fin)
