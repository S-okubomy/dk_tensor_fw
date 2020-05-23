"""
## 手順(6)  学習（MLP）モデルを実行して、判定
↓↓↓↓↓↓↓↓
"""

import pickle, tfidfWithIni
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.models import model_from_json
import importlib

# モジュール（tfidfWithIni）のリロード
importlib.reload(tfidfWithIni)

def inverse_dict(d):
    return {v:k for k,v in d.items()}

# テキストを指定して判定
def getMusicName(text):
    # TF-IDFのベクトルに変換 
    data = tfidfWithIni.calc_text(text)
    # MLPで予測
    pre = model.predict(np.array([data]))[0]
    n = pre.argmax()
    recMusicName = label_dic[n]
    predict_val = "{:.4f}".format(pre[n])

    print(recMusicName, predict_val)
    return recMusicName, predict_val


# ラベルの定義
labelToCode = pickle.load(open("studyModel/label_to_code.pickle", "rb"))
nb_classes = len(labelToCode) 
label_dic = inverse_dict(labelToCode)

# 辞書から入力 要素数を求める。
in_size_hantei = pickle.load(open("studyModel/genre-tdidf.dic", "rb"))[0]['_id']

# TF-IDFの辞書を読み込む --- (*2)
tfidfWithIni.load_dic("studyModel/genre-tdidf.dic")

# Kerasのモデルを定義して重みデータを読み込む --- (*3)
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(in_size_hantei,))) # input_shape 202
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(nb_classes, activation='softmax'))
model.compile(
    loss='categorical_crossentropy',
    optimizer=RMSprop(),
    metrics=['accuracy'])
model.load_weights('./studyModel/genre-model.hdf5')