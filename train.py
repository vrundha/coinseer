import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dropout, Dense, Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split

window = 25



def get_data(filename,num_days_to_predict):
    data = []
    with open(filename) as f:
        for line in f.readlines():
            _parts = line.split("\t")
            data.append([float(_parts[4].replace(",", "").replace("$", ""))])
    data.reverse()
    data = np.array(data)
    norm = np.linalg.norm(data)
    data = data / norm
    x = []
    y = []
    for i in range(len(data) - window-1-num_days_to_predict):
        x.append(data[i:i+window])
        y.append(data[i+window])
    x_train = np.array(x)
    y_train = np.array(y)
    return x_train, y_train, norm, data


def train_model(x_train, y_train, model_file):
    # print(model_file, os.path.exists(model_file))
    if "xrp" in model_file:
        model_file = model_file.replace("xrp", "xpr")
    epochs = 40
    if not os.path.exists(model_file):
        exit()
        model = Sequential()
        model.add(LSTM(units=window, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=window, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=window, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=window))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        opt = tf.keras.optimizers.Adam(learning_rate=0.01)
        model.compile(loss="mse", optimizer=opt)
        model.fit(x_train, y_train, batch_size=32, epochs=epochs)
        model.save(model_file)
        print("Saved model to disk")
    else:
        print("Loading from disk...", model_file)
        model = tf.keras.models.load_model(model_file)
    return model


def predict(model, number_of_days, x, norm):
    for i in range(number_of_days):
        next_pred = model.predict(x[:, i:25 + i])
        # print("\n\n", next_pred*norm)
        x = np.append(x, next_pred).reshape((1, window+i+1, 1))
    return x[:,:-10,:]*norm


def predict_model(crypto, model_file_name, num_days_to_predict):
    x_train, y_train, norm, full_data = get_data(filename=crypto+".csv", num_days_to_predict=num_days_to_predict)
    model = train_model(x_train, y_train, model_file_name)
    predicted_data = predict(model, num_days_to_predict, full_data[-10 - window: -10].reshape(1, window, 1), norm)
    actual_data = full_data*norm
    return actual_data, predicted_data

#
# number_of_days = 10
# # x_train, y_train, norm, full_data = get_data(filename="btc.csv")
# # model = train_model(x_train, y_train, "btc_model-10.h5")
# # predict(model, number_of_days, full_data[-10-window: -10].reshape(1, window, 1), norm)
# # print(full_data[-10:]*norm)
#
#
#
# x_train, y_train, norm, full_data = get_data(filename="xrp.csv",num_days_to_predict=number_of_days)
# model = train_model(x_train, y_train, "xpr_model.h5")
# predict(model, number_of_days, full_data[-10-window: -10].reshape(1, window, 1), norm)
#
#
