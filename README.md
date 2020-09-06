# dk_tensor_fw
using docker-compose

## 確認方法
1. docker環境構築後、ブラウザでURLを入力
```
http://localhost:7020/recommend/api/what-music/青春 ドラマ
```

## 開発サーバ起動する場合の注意
FlaskにてデバッグモードをONにするとtensorflowでエラーとなる。
そのため、ソースコード変更毎に開発サーバを再起動する必要がある。
```
# 起動している場合はcntr+cで停止し、以下コマンド実行
python3 webQueApiRunServer.py
```

## docker環境構築方法
1. イメージビルド
```
docker-compose up -d --build
```

## 機械学習モデル作成

1. docker-composeでUbuntuに入る。
```
docker-compose ps
docker-compose exec app_tensor /bin/bash
```

2. 必要あればツールを使用して参考用のcsvを出力する（g_output.csv）
```
# keys.csvを作成後、以下コマンド
python3 cInfoTool.py
```

3. 機械学習モデル作成 方法
```
# （手順1）学習用のテキストデータを作成（ans_studyInput_fork.txt）
# （手順2）mkdbAndStudy.pyを実行
python3 mkdbAndStudy.py
```

4. コンテナからexitしてdocker-composeを再起動する。
```
docker-compose restart
```

## 参考
```
#必要あれば開発サーバ起動（コンテナ内で）
python3 webQueApiRunServer.py
# サービス停止
docker-compose stop
# サービス開始
docker-compose start
# コンテナの停止（ボリュームも削除）
docker-compose down -v

# 出てなければ空いてる
netstat -an | grep 7000

# docker-compose 実行方法
docker-compose --version
docker-compose up -d --build
docker-compose ps
docker-compose exec サービス名 /bin/bash
docker-compose exec app_tensor /bin/bash
docker-compose exec web-nginx /bin/bash

docker-compose stop
docker-compose start

# docker-compose 停止・削除
docker-compose down
# docker-compose 削除
docker-compose rm
```

## Web APIへアクセス

* （例1） http://localhost:7020/recommend/api/what-music/ハンバード・ハンバードさんが歌う切ない曲
* （例2） http://localhost:7020/recommend/api/what-music/出会いをテーマにした曲でみゆきさんが歌う
* （例2） http://localhost:7020/recommend/api/what-music/切なくて誰かの幸せ願う歌