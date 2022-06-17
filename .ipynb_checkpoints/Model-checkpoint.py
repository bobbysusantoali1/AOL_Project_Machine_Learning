
import pandas as pd
import numpy as np
df = pd.read_csv(r"D:\Kuliah\Semester 4\NLP\Project\AOL_Project_Machine_Learning\DataMix.csv", sep = ';')
df.info()


x = df[['LB', 'LT', 'KT', 'KM', 'GRS']]
y = df.HARGA


x.GRS = x.GRS.astype('category')
y = y.astype('category')
x.info()


from sklearn.preprocessing import LabelEncoder, OneHotEncoder 
label_encode = LabelEncoder()
x['GRS'] = label_encode.fit_transform(x['GRS'])
x


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(x_train, y_train.values.ravel())


predict_test = model.predict(x_test)
abs(predict_test)
print("Test Score : " + str(model.score(x_test, y_test)))


predict_train = model.predict(x_train)
abs(predict_train)
print("Train Score : " + str(model.score(x_train, y_train)))


# import matplotlib.pyplot as plt
# fig, (x1, x2) = plt.subplots(1, 2, figsize = (15, 7))
# fig.suptitle('scatter of predict result')
# x1.scatter(y_train, predict_train)
# x1.set_title('Prediction Train Data')
# x1.set_ylabel('y_train')
# x1.set_xlabel('y_prediction')
# x2.scatter(y_test, predict_test)
# x2.set_title('Prediction Test Data')
# x2.set_ylabel('y_test')
# x2.set_xlabel('y_prediction')
# plt.show()