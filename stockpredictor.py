import pandas as pd
import gspread
import plotly.express as px
import pylab as plt 
from oauth2client.service_account import ServiceAccountCredentials
import plotly.graph_objects as go
import smtplib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn import *
import math
from keras.models import *
from keras.layers import *

from datetime import date
from nsepy import get_history
import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [[sg.Text('Enter symbol of stock'),sg.InputText()]]
layout.append([sg.CloseButton("OK"), sg.CloseButton("Cancel")])

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    h = values[0]

window.close()

sbin = get_history(symbol= h,
                   start=date(2019,1,1),
                   end=date(2020,4,16))

df = pd.DataFrame(sbin)


data = df.filter(['Close'])
dataset = data.values
training_data_len = math.ceil(len(dataset)* .85)
print(training_data_len)

scaler = MinMaxScaler(feature_range = (0,1))
scaled_data = scaler.fit_transform(dataset)


train_data = scaled_data[0: training_data_len, :]
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60: i, 0])
    y_train.append(train_data[i, 0])
   
        
        
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[1],1))


model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape= (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences= False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, batch_size=1, epochs=1)
test_data = scaled_data[training_data_len - 60: , :]

x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])

x_test = np.array(x_test)

x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
rmse

train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16,8))
plt.title(print("Stock price of"+h))
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'])
plt.show()
