# dk_tensor_fw
using docker-compose

## 使い方

```:使い方
#空いているポート調べる（何も表示されなければ空いてる）
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