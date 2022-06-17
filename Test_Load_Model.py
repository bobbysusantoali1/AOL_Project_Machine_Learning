import pickle

filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

X_new = [
	[267, 250, 4, 4, 0],
	# [250, 250, 3, 3, 0],
	# [200, 250, 2, 2, 0],
	# [167, 250, 1, 1, 0],
]

result = loaded_model.predict(X_new)

for i in result:
	print(int(i))