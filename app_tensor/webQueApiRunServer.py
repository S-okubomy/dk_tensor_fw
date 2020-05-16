import joblib
import flask
import numpy as np
import os
import requests
import json
import datetime
import pytz
import exeWhatMusic

#ポート番号
TM_PORT_NO = 7010

# initialize our Flask application and pre-trained model
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # <-- 日本語の文字化け回避


@app.route('/alexspeak/api/how-to-spend', methods=['GET'])
def get_how_to_spend():
    alexSpeakInfos = getAlexSpeakMojiRst()
    return flask.jsonify({'alexSpeakInfos': alexSpeakInfos})


# 占い結果を返す
def getUranaiRst():
    now_jp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    date_jp_form = now_jp.strftime("%Y/%m/%d")

    res = requests.get(url='http://api.jugemkey.jp/api/horoscope/free/'+ date_jp_form)
    uranaiRstKaniza = res.json()["horoscope"][date_jp_form][3]["content"]
    
    return uranaiRstKaniza

# 天気予報の結果を返す
def getWeatherInfo():
    LOCATION = 'Tokyo,jp' # 場所を設定してください
    APPID='de8940f9f25cc75800cd17380cd25ef8' # openweathermap のAPIキーを設定してください

    # 天気のデータを取得する
    url ='http://api.openweathermap.org/data/2.5/forecast?q={}&cnt=10&appid={}&units=metric'\
    .format(LOCATION, APPID)
    response = requests.get(url)
    response.raise_for_status()

    weather_data = json.loads(response.text)
    
    w = weather_data['list']

    tenki_1200 = w[2]['weather'][0]['main']
    temp_1200 = w[2]['main']['temp']

    # 雨かどうか
    isRain = False
    if tenki_1200 == 'Rain':
        isRain = True
    else:
        isRain = False
        
    # 服装を返す
    fukuso = '冬服'
    if -80.0 < temp_1200 < 10.0:
        fukuso = '冬服'
    elif 10.0 <= temp_1200 < 15.0:
        fukuso = '秋服'
    elif 15.0 <= temp_1200 < 25:
        fukuso = '春服'
    elif 25 <= temp_1200:
        fukuso= '夏服'
    
    #print(isRain,fukuso)
    
    return isRain, fukuso

# 取得時間情報を元に文字列を返却します。
def getDateInfoStr():
    now_jp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    hourNow = now_jp.hour

    # 挨拶文字と応援フレーズを生成
    greetingStr = ''
    cheerPhrase = ''
    if 5 < hourNow < 10:
        greetingStr = 'おはようございます。' 
        cheerPhrase = '今日もいちにちはじまりました。頑張りましょう。ビートたけしさんの名言です。「夢を持て、目的を持て、やれば出来る。」そんな言葉に騙されるな。'\
                      '何も無くていいんだ。人は生まれて、生きて、死ぬ、これだけで大したもんだ。。って言う気持ちで頑張りましょう。'
    elif 10 <= hourNow < 16:
        greetingStr = 'こんにちは。'
        cheerPhrase = 'いちにちも中盤ですね。長いですね。みわ あきひろさんの名言です。人生いくら扉を叩いても開かないときもある。そのときは神様の与えてくれた時間だと'\
                      '思って、自分の中身を膨らませることね。。って言う気持ちで頑張りましょう。'
    elif 16 <= hourNow < 21:
        greetingStr = 'こんばんは。'
        cheerPhrase = 'もう少しですね。あとちょっと頑張りましょう。よしゆき じゅんのすけさんの名言です。激しく傷つくということは。。'\
                      '傷つく能力があるから傷つくのであって。。その能力の内容といえば、豊かな感受性と鋭い感覚である。。って言う気持ちで頑張りましょう。'
    elif 21 <= hourNow < 24:
        greetingStr = 'こんばんは。いちにちお疲れ様です。'
        cheerPhrase = '休める人はゆっくり休みましょう。まだの人は無理しない程度に頑張ってくださいね。のび太「ドラえもん名言集」とヘンリー・フォードさんの名言です。'\
                      'あきらめのいいところが僕の長所なんだ。。あなたができると思えばできる。できないと思えばできない。どちらにしてもあなたが思ったことは正しい。'\
                      '。。って言う気持ちで参りましょう。'
    else:
        greetingStr = 'こんばんは。遅くまで頑張ってますね。お疲れ様です。'
        cheerPhrase = 'いちにちは長いので、可能ならお休みしてくださいね。まつした こうのすけさんとシェイクスピアさん、ソローさんの名言です。'\
                      '山は西からも東からでも登れる。自分が方向を変えれば、新しい道はいくらでもひらける。。今後のことなんかは、ぐっすりと眠り、忘れてしまうことだ。。'\
                      'すべての不幸は未来への踏み台にすぎない。'\
                      '。。って言う気持ちで参りましょう。'


    # 今日の残り時間文字列を生成
    time_jp_str = now_jp.strftime('%H:%M:%S')
    nowTimeJp = datetime.datetime.strptime(time_jp_str, '%H:%M:%S')
    oneDayHour = datetime.datetime.strptime('23:59:59', '%H:%M:%S')
    remainingSec = (oneDayHour - nowTimeJp).total_seconds() + 1   # 1秒加える

    remainingHourStr = '{:.0f}'.format(remainingSec//3600)
    remainingMinStr = '{:.0f}'.format(remainingSec%3600//60)
    remainingTimeStr = '今日の残り時間は、' + remainingHourStr + '時間、' + remainingMinStr + '分です。'

    # 返却文字生成
    dateInfoStr = greetingStr + remainingTimeStr + cheerPhrase

    return dateInfoStr


# 話し言葉を返す
def getAlexSpeakMojiRst():

    dateInfoStr = getDateInfoStr()
    isNesKasa, fukusoMoji = getWeatherInfo()
    
    # 傘の要否
    kasaYohi = '不要'
    if isNesKasa:
        kasaYohi = '必要' 
    
    uranaiMoji = getUranaiRst()
    alexSpeakMoji = '{}、さて、今日は、傘は{}で、服装は{}が良いと思います。以下も参考にしましょう。{}。。'\
                    'このご時世大変かと思いますが、皆様体調お気をつけください。よかったらまた話かけてください。'\
                    '一応毎日内容は変わってます。'\
                    .format(dateInfoStr,kasaYohi,fukusoMoji,uranaiMoji)
    
    #JSON作成
    alexSpeakJson = [
        {
            'id':1,
            'alexSpeakMoji':alexSpeakMoji,
            'kasaYohi':kasaYohi,
            'fukusoMoji':fukusoMoji
        }
    ]
    
    return alexSpeakJson


@app.route('/recommend/api/what-music/<how_music>', methods=['GET'])
def get_recom_music(how_music):
    recoMusicInfos = getRecoMusicMoji(how_music)
    return flask.jsonify({'recoMusicInfos': recoMusicInfos})

# オススメの楽曲名を返す
def getRecoMusicMoji(how_music):

    recMusicName, predict_val = exeWhatMusic.check_genre(how_music)

    #JSON作成
    recoMusicInfoJson = [
        {
            'id':1,
            'recoMusicMoji':recMusicName,
            'predict_val':predict_val,
            'how_music':how_music
        }
    ]
    
    return recoMusicInfoJson


if __name__ == "__main__":
    print(" * Flask starting server...")
    app.run(threaded=False, host="0.0.0.0", port=int(os.environ.get("PORT", TM_PORT_NO)))
#    app.run(port=TM_PORT_NO)
#    app.run()

