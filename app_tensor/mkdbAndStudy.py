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
labelToCode = {}

# csvファイルを読み込む
def read_file(path):
    '''テキストファイルを学習用に追加する''' # --- (*6)
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)   
        label_id = 0  
        for row in reader:
            # ラベルコード作成
            if row[2] not in labelToCode:
                labelToCode[row[2]] = label_id
                label_id += 1

            y.append(labelToCode[row[2]])  # ラベルをセット
            tfidfWithIni.add_text(row[3])  # 文章をセット
           # print("ラベル: ", row[2], "(", labelToCode[row[2]], ")",  " 文章: ", row[3])

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
    pickle.dump(labelToCode, open('studyModel/label_to_code.pickle', 'wb'))


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

# 分類するラベルの数
labelToCode = pickle.load(open("studyModel/label_to_code.pickle", "rb"))
nb_classes = len(labelToCode) 

# データベースの読込
data = pickle.load(open("studyModel/genre.pickle", "rb"))
y = data[0] # ラベルコード
x = data[1] # TF-IDF
# ラベルデータをone-hotベクトルに直す
y = keras.utils.np_utils.to_categorical(y, nb_classes)
in_size = x[0].shape[0] # 入力x[0]の要素数

# 学習用とテスト用を分ける
x_train, x_test, y_train, y_test = train_test_split(
        np.array(x), np.array(y), test_size=0.2)

# MLPモデル構造を定義
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(in_size,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(nb_classes, activation='softmax'))

# モデルをコンパイル
model.compile(
    loss='categorical_crossentropy',
    optimizer=RMSprop(),
    metrics=['accuracy'])

# 学習を実行
hist = model.fit(x_train, y_train,
          batch_size=16, # 1回に計算するデータ数
          epochs=150,    # 学習の繰り返し回数みたいなもの
          verbose=1,
          validation_data=(x_test, y_test))

# 評価する
score = model.evaluate(x_test, y_test, verbose=1)
print("正解率=", score[1], 'loss=', score[0])

# 重みデータを保存
model.save_weights('./studyModel/genre-model.hdf5')

# 学習の様子をグラフへ描画
plt.plot(hist.history['val_accuracy'])
plt.title('Accuracy')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

