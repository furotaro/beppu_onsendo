import requests
from bs4 import BeautifulSoup
import csv


# 対象のURLを指定
url_page = [
            'https://onsendo.beppu-navi.jp/feature/',
            "https://onsendo.beppu-navi.jp/feature/page/2/",
            "https://onsendo.beppu-navi.jp/feature/page/3/",
            "https://onsendo.beppu-navi.jp/feature/page/4/"]
count=0

csv_file = '別府温泉道.csv'
items=['住所', 'TEL', '料金', '利用時間', '定休日ほか', '家族湯（貸切湯）', '泉質', '最寄りバス停', '最寄り駅', '駐車場', 'その他', 'URL']
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['番号','施設名']+items)  # ヘッダーを書き込み

for url in url_page:
    # ページの内容を取得
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    # h3タグのdata-original属性の値を取得
    data_original_values = [a.get('title') for a in soup.find_all('a') if a.get('title')]
    isdecimal=[(a.get('href').split("/")[-2].split("y")[-1]).isdecimal() for a in soup.find_all('a') if a.get('title')]
    data_url = [(a.get('title'),a.get('href'),a.get('href').split("/")[-2].split("y")[-1]) for a in soup.find_all('a') if a.get('title') and (a.get('href').split("/")[-2].split("y")[-1]).isdecimal()]
    not_data_url = [(a.get('title'),a.get('href'),a.get('href').split("/")[-2].split("y")[-1]) for a in soup.find_all('a') if a.get('title') and not (a.get('href').split("/")[-2].split("y")[-1]).isdecimal()]
    if len(not_data_url)!=1:data_url+=[('第235番 白糸の滝温泉', 'https://onsendo.beppu-navi.jp/ｙ235/', 'ｙ235'), ('第231番 グランシア別府鉄輪', 'https://onsendo.beppu-navi.jp/ｙ231/', '%ｙ231')]
    # print(not_data_url)
    # continue

    # 取得した値を出力
    for value,onsen_url,num in data_url:
        print(count,value)
        count+=1
    
    with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for value,onsen_url,num in data_url:
            number = value.split("番")[0].replace('第', '')
            name = f"第{number}番 {value.split('番')[-1].replace(' ', '').replace('　', '')}"
            print(onsen_url)
            info={item: "" for item in items}
            # ページの内容を取得
            response = requests.get(onsen_url)
            html_content = response.content

            # BeautifulSoupを使ってHTMLを解析
            soup = BeautifulSoup(html_content, 'html.parser')

            # テーブルを取得
            table = soup.find('table', {'class': 'blog'})
            if table is None:
                figure = soup.find('figure')
                table = figure.find('table')

            # テーブルのヘッダーとデータを取得
            headers = []
            rows = []

            for row in table.find_all('tr'):
                header = row.find('th')
                header = row.find('th').get_text(strip=True) if header is not None else "exception"
                if header=="備考":header="その他"
                elif header=="定休日" or header=="休館日":header="定休日ほか"
                elif header=="入湯料金" or header=="入浴料金" or header=="入湯":header="料金"
                elif header=="家族湯":header="家族湯（貸切湯）"
                headers.append(header)
                data = row.find('td').get_text(strip=True)
                if header=="住所" and "別府市" not in data:data="".join(["別府市",data])
                info[header]=data
            rows=list(info.values())
    #         print(len(headers),headers)
    # exit()
            writer.writerow([number,name]+rows+[onsen_url])


