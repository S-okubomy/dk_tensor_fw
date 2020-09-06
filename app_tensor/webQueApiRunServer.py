import flask
import os
import exeWhatMusic

#ポート番号
TM_PORT_NO = 7010

# initialize our Flask application and pre-trained model
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # <-- 日本語の文字化け回避

@app.route('/recommend/api/what-music/<how_music>', methods=['GET'])
def get_recom_music(how_music):
    recoMusicInfos = getRecoMusicMoji(how_music)
    return flask.jsonify({'recoMusicInfos': recoMusicInfos})

# オススメの楽曲名を返す
def getRecoMusicMoji(how_music):

    recMusicName, predict_val = exeWhatMusic.getMusicName(how_music)

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