
import requests
import json

 
kw = {'wd':'长城'}
 
headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}
 
response = requests.get("http://push2.eastmoney.com/api/qt/stock/trends2/get?secid=1.000001&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11%2Cf12%2Cf13&fields2=f51%2Cf53%2Cf56%2Cf58&iscr=0&iscca=0&ndays=1&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&cb=fsdata1615288182362&fsdata1615288182362=fsdata1615288182362", params = kw, headers = headers)
 
json_data = json.loads(response.text[20:-2])
 
# print(json_data["data"]['trends'])

for tmp in json_data["data"]['trends']:
    print(tmp)
    # print(json_data[tmp])
# print(response.content)
# print(response.url)
 

