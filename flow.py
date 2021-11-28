#!/usr/bin/python3

import requests
import json
import time
# import sqlite3


pe_dynamic = 0
pe_static = 0
pe_ttm = 0
index = 0
exclude_cnt = 0
total_valid_marketValue = 0
dict_stock = {}

# url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.000100&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fields=f13,f19,f20,f23,f24,f25,f26,f27,f28,f29,f30,f43,f44,f45,f46,f47,f48,f49,f50,f57,f58,f59,f60,f85,f107,f111,f113,f114,f115,f116,f117,f127,f130,f131,f132,f133,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f152,f161,f162,f164,f165,f167,f168,f169,f170,f171,f174,f175,f177,f178,f181,f182,f198,f199,f251,f252,f253,f254,f255,f256,f257,f260,f261,f288,f292,f293,f294,f295,f530,f531&invt=2&cb=jQuery341032191508327964113_1635681329518&_=1635681329520'
# url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.000100&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f62,f71,f84,f85,f92,f107,f108,f111,f116,f117,f119,f122,f130,f152,f161,f162,f163,f164,f165,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f191,f260,f261,f277,f278,f288,f292,f293,f294,f295&invt=2&cb=hqCall&callback=jQuery341004789702468919654_'+str(int(time.time()*1000)-1)+'&_=1636179047411'+str(int(time.time()*1000))
# url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.600030&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f62,f71,f84,f85,f92,f107,f108,f111,f116,f117,f119,f122,f130,f152,f161,f162,f163,f164,f165,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f191,f260,f261,f277,f278,f288,f292,f293,f294,f295&invt=2&cb=hqCall&callback=jQuery341035354854109769573_1636181813152&_=1636181813153'
# url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.300014&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f62,f71,f84,f85,f92,f107,f108,f111,f116,f117,f119,f122,f130,f152,f161,f162,f163,f164,f165,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f191,f260,f261,f277,f278,f288,f292,f293,f294,f295&invt=2&cb=hqCall&callback=jQuery34104179698485775576_1636198229189&_=1636198229190'

with open('./hs300.txt', 'r+') as f:
    stock_list = f.read().splitlines()
    print(len(stock_list))

for stock_code in stock_list:
    if stock_code[0] == '6':
        foo_header = '1'
    else:
        foo_header = '0'
    url = 'https://push2.eastmoney.com/api/qt/stock/get?secid='+foo_header+'.' + \
        str(stock_code) + '&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f62,f71,f84,f85,f92,f107,f108,f111,f116,f117,f119,f122,f130,f152,f161,f162,f163,f164,f165,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f191,f260,f261,f277,f278,f288,f292,f293,f294,f295&invt=2&cb=hqCall&callback=jQuery341035354854109769573_'+str(int(time.time()*1000)-1)+'&_='+str(int(time.time()*1000))
    # print(url)
    r = requests.get(url)
    # print(r.text)
    stock_data = json.loads(r.text[r.text.find('{'):-2])['data']
    # print(stock_data)

    if stock_data['f162'] < 0 or stock_data['f163'] < 0 or stock_data['f164'] < 0 or stock_data['f163']/100 > 180:
        print("{} {} {} {} {} {}".format(index, stock_data['f58'], stock_code,
              stock_data['f162']/100, stock_data['f163']/100, stock_data['f164']/100))
        exclude_cnt += 1
    else:
        pe_dynamic += stock_data['f162']
        pe_static += stock_data['f163']
        pe_ttm += stock_data['f164']

        dict_stock[str(stock_data['f58'])] = {
            'pe_dynamic': stock_data['f162']/100,
            'pe_static' : stock_data['f163']/100,
            'pe_ttm' : stock_data['f164']/100,
            'marketValue': stock_data['f116']
            }

        total_valid_marketValue += int(stock_data['f116'])
    index += 1

    # print("{} {} {} {} {}".format(index, stock_code, stock_data['f162']/100, stock_data['f163']/100, stock_data['f164']/100 ))
foo_rate = (300-exclude_cnt)*100
print("exclude_cnt: " + str(exclude_cnt))
print("dynamic: " + str(pe_dynamic/foo_rate))
print("static: " + str(pe_static/foo_rate))
print("ttm: " + str(pe_ttm/foo_rate))


pe_dynamic = 0
pe_static = 0
pe_ttm = 0

for key,value in dict_stock.items():
    pe_dynamic += value['pe_dynamic'] * (int(value['marketValue'])/total_valid_marketValue)
    pe_static += value['pe_static'] * (int(value['marketValue'])/total_valid_marketValue)
    pe_ttm += value['pe_ttm'] * int(value['marketValue']) / total_valid_marketValue
print("===>weighting")
print("dynamic: " + str(pe_dynamic))
print("static: " + str(pe_static))
print("ttm: " + str(pe_ttm))