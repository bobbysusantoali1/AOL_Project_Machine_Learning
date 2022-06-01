import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle

df = pd.read_csv(r'DataMix.csv', sep = ';')
X = df[['LB', 'LT', 'KT', 'KM', 'GRS']]
Y = df['HARGA']
test_size = 0.2
seed = 7
from sklearn.preprocessing import LabelEncoder
label_encode = LabelEncoder()
X['GRS'] = label_encode.fit_transform(X['GRS'])
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)
# Fit the model on training set
model = LogisticRegression()
model.fit(X_train, Y_train)

filename = 'Prediksi_Harga_Rumah.ipynb'
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)