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

# ラベルの定義
LABELS = ["TSUNAMI", "雲がゆくのは", "空も飛べるはず", "糸", "おなじ話"
            , "今宵の月のように","贈る言葉", "サボテンの花", "民衆の歌"
            , "いつも何度でも"]

# 独自のテキストを指定 --- (*1)
text1 = """
桑田圭佑 しっとり　切ない。
"""
text2 = """
他の人がいる場所が晴れる
癒やし
"""
text3 = """
我慢しない
"""

# 辞書から入力 要素数を求める。
in_size_hantei = pickle.load(open("studyModel/genre-tdidf.dic", "rb"))[0]['_id']

# TF-IDFの辞書を読み込む --- (*2)
tfidfWithIni.load_dic("studyModel/genre-tdidf.dic")

# Kerasのモデルを定義して重みデータを読み込む --- (*3)
nb_classes = len(LABELS) # TODO 修正
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

# テキストを指定して判定 --- (*4)
def check_genre(text):
    # TF-IDFのベクトルに変換 -- (*5)
    data = tfidfWithIni.calc_text(text)
    # MLPで予測 --- (*6)
    pre = model.predict(np.array([data]))[0]
    n = pre.argmax()
    # recMusicName = LABELS[n] + "(推定値：" + "{:.3f}".format(pre[n]) + ")"
    recMusicName = LABELS[n]
    predict_val = "{:.4f}".format(pre[n])

    print(recMusicName, predict_val)
    return recMusicName, predict_val


