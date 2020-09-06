import requests as web
import bs4
import csv
import time

# 検索数
kensakuSu = 3

# これがないと説明文とれない
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)" \
     "AppleWebKit/537.36 (KHTML, like Gecko)" \
     "Chrome/60.0.3112.113"

#user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
#user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"

with open('keys.csv', encoding='utf8') as keyListFile:
    with open('g_output.csv','w',newline='',encoding='utf8') as outcsv:
        csvwriter = csv.writer(outcsv)
        csvwriter.writerow(['No','判定','曲名','説明'])
        cntMusic = 0
        key_list = csv.reader(keyListFile)
        for key in key_list:
            resp = web.get('https://www.google.co.jp/search?num=100&q=' + '　'.join(key[0] + '　歌詞　意味')
                    , headers={"User-Agent": user_agent})
            resp.raise_for_status()

            time.sleep(0.5) # スリープ

            # 取得したHTMLをパースする
            resp.encoding = 'utf8'  # 文字コード
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            #soup.find("span", {"class":"f"}).extract()

            # 検索結果の説明部分を取得
            content = soup.select('div > .st')
            for i in range(kensakuSu):
                cntMusic += 1
                # 説明のテキスト部分のみを取得/余分な改行コードは削除する
                content_text = content[i].get_text().replace('\n','').replace('\r','')
                #print(content_text)
                csvwriter.writerow([cntMusic,'T', key[0], content_text])
