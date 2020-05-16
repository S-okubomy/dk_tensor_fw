"""
## 手順(4)  学習データ（DB）を作成
   ↓↓↓↓↓↓↓↓
"""

import os, csv, glob, pickle
import tfidfWithIni
import importlib

# モジュール（tfidfWithIni）のリロード
importlib.reload(tfidfWithIni)

# 変数の初期化
y = []
x = []

# ラベルのコード変換用 辞書
labelToCode = {"TSUNAMI":0, "雲がゆくのは":1, "空も飛べるはず":2
               , "糸":3, "おなじ話":4, "今宵の月のように":5, "贈る言葉":6
               ,"サボテンの花":7, "民衆の歌":8, "いつも何度でも":9}

# csvファイルを読み込む
def read_file(path):
    '''テキストファイルを学習用に追加する''' # --- (*6)
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)     
        for row in reader:
            y.append(labelToCode[row[2]])  # ラベルをセット
            tfidfWithIni.add_text(row[3])  # 文章をセット
            print("ラベル: ", row[2], "(", labelToCode[row[2]], ")",  " 文章: ", row[3])

# モジュールのテスト --- (*15)
if __name__ == '__main__':
    # TF-IDFベクトルを初期化(filesを空にする)
    tfidfWithIni.iniForOri()
    
    # ファイル一覧を読む --- (*2)
    read_file("inputFile/ans_studyInput_fork.txt")

    # TF-IDFベクトルに変換 --- (*3)
    x = tfidfWithIni.calc_files()

    # 保存 --- (*4)
    pickle.dump([y, x], open('studyModel/genre.pickle', 'wb'))
    tfidfWithIni.save_dic('studyModel/genre-tdidf.dic')
    # print(x)
    print('ok')


"""
## 手順(5)  学習（MLP）を実行
   ↓↓↓↓↓↓↓↓
"""

import pickle
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import numpy as np
import h5py

# 分類するラベルの数 --- (*1)
nb_classes = len(labelToCode)  # TODO 修正

# データベースの読込 --- (*2)
data = pickle.load(open("studyModel/genre.pickle", "rb"))
y = data[0] # ラベルコード
x = data[1] # TF-IDF
# ラベルデータをone-hotベクトルに直す --- (*3)
y = keras.utils.np_utils.to_categorical(y, nb_classes)
in_size = x[0].shape[0] # 入力x[0]の要素数

# 学習用とテスト用を分ける --- (*4)
x_train, x_test, y_train, y_test = train_test_split(
        np.array(x), np.array(y), test_size=0.2)

# MLPモデル構造を定義 --- (*5)
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(in_size,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(nb_classes, activation='softmax'))

# モデルをコンパイル --- (*6)
model.compile(
    loss='categorical_crossentropy',
    optimizer=RMSprop(),
    metrics=['accuracy'])

# 学習を実行 --- (*7)
hist = model.fit(x_train, y_train,
          batch_size=16, # 128 → x 
          epochs=150,  # TODO 調整 反復回数
          verbose=1,
          validation_data=(x_test, y_test))

# 評価する ---(*8)
score = model.evaluate(x_test, y_test, verbose=1)
print("正解率=", score[1], 'loss=', score[0])

# 重みデータを保存 --- (*9)
model.save_weights('./studyModel/genre-model.hdf5')

# 学習の様子をグラフへ描画 --- (*10)
plt.plot(hist.history['acc'])
plt.plot(hist.history['val_acc'])
plt.title('Accuracy')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

