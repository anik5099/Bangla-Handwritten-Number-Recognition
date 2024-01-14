import numpy as np
import pandas as pd
import pickle
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import save_model

file_path = 'assets/bhand.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file, encoding = 'latin1')
df = pd.DataFrame(data)
first_el = df.iloc[0, 0]
x = df.iloc[0, 1]
y = df.iloc[1, 1]
z = df.iloc[2, 1]
X_train, y_train = first_el, x
X_val, y_val = df.iloc[1, 0], y
X_test, y_test = df.iloc[2, 0], z
X_combined = np.concatenate((X_train, X_val), axis=0)
y_combined = np.concatenate((y_train, y_val), axis = 0)
y_combined = y_combined.reshape(-1, 1)
for i in range(len(X_combined)):
    X_combined[i] = (X_combined[i] >= 0.5).astype(int)
X_train = X_train.reshape(-1, 32, 32, 1)
X_val = X_val.reshape(-1, 32, 32, 1)
X_test = X_test.reshape(-1, 32, 32, 1)
for i in range(len(X_train)):
    X_train[i] = (X_train[i] >= 0.5).astype(int)
for i in range(len(X_val)):
    X_val[i] = (X_val[i] >= 0.5).astype(int)
    X_test[i] = (X_test[i] >= 0.5).astype(int)
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
X_combined = X_combined.reshape(-1, 32, 32, 1)
y_train = np.array(y_train)
model.fit(X_train, y_train, epochs=10, batch_size=32)
y_val = np.array(y_val)
y_test = np.array(y_test)
predictions = model.predict(X_test)
predicted_labels = np.argmax(predictions, axis=1)
print(y_test[0])
print(predicted_labels[0])
plt.imshow(X_test[0])
save_model(model, 'cnn.h5')