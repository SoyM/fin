#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# feature: 30天内加速度;创业板，中小板，白马
import re
import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.graphics.api as smg
import time


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Cookie': '_ga=GA1.2.390769919.1552150985; _gid=GA1.2.102441312.1552150985; qgqp_b_id=f69f83447752be0b46753cdc52717be8; st_pvi=53068450450300; st_sp=2019-03-10%2002%3A14%3A31; st_inirUrl=http%3A%2F%2Fm.data.eastmoney.com%2Fhsgt%2Findex.html; st_si=93379072515284; _gat=1',
           'DNT': '1',
           'Host': 'dcfm.eastmoney.com',
                   'If-Modified-Since': 'Sat, 09 Mar 2019 20:06:00 GMT',
                   'If-None-Match': "8788d883b3d6d41:0",
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}


def colours(font):
    # if type(font) == str:
    if float(re.compile(r'-?\d+\.*\d*').findall(str(font))[0]) >= 0:
        return "\033[0;31m{}\033[0m".format(font)
    else:
        return "\033[0;32m{}\033[0m".format(font)


def mainland_hk_pipe_last():
    r = requests.get(
        r'https://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=P.(x),(x),(x)|0000011|3990012|3990012,0000011,HSI5,BK07071,MK01461,MK01441,BK08041&sty=SHSTD|SZSTD|FCSHSTR&st=z&sr=&p=&ps=&cb=&js=result51858295({result:[(x)]})&token=1942f5da9b46b069953c873404aad4b5&callback=result51858295&_='+str(round(time.time() * 1000)), headers=headers)

    html = str(r.text)
    html_splited = html[html.find('{'):len(html)-1].split('","')
    # print(html_splited)
    # print(" ")
    # print(html_splited[0])
    # print(html_splited[0][html_splited[0].find('["')+2:-1 ])

    temp = html_splited[0][html_splited[0].find('["')+2:-1].split(',')

    print("hk-hu pipe  | hk in: " + colours(temp[0]) + ", shanghai in: " + colours(temp[6]))

    # print(html_splited[1])
    temp = html_splited[1].split(',')
    print("hk-sz pipe  | hk in: " +
          colours(temp[0]) + ", shenzhen in: " + colours(temp[6]))


def hk_to_mainland_1d():
    url = r'https://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id=north&type=EFR&rtntype=2&acces_token=1942f5da9b46b069953c873404aad4b5&js=result10043862({result:[(x)]})&callback=result10043862&_='+str(round(time.time() * 1000))
    r = requests.get(url, headers=headers)
    # print(r.text)
    html = str(r.text)
    html_splited = html[html.find('{'):len(html)-1].split('","')
    # print(html_splited)
    shanghaiIn = []
    shenzhenIn = []

    for key, tradeVolPerMinute in enumerate(html_splited):
        if key == 0:
            temp = tradeVolPerMinute[tradeVolPerMinute.find(
                '"')+1:-1].split(',')
            # print(temp)
            if temp[1].strip() != '':
                shanghaiIn.append(temp[1])
                shenzhenIn.append(temp[2])
        elif key == len(html_splited)-1:
            temp = tradeVolPerMinute[0:tradeVolPerMinute.find(
                '"')-1].split(',')
            # print(temp)
            if temp[1].strip() != '':
                shanghaiIn.append(temp[1])
                shenzhenIn.append(temp[2])
        else:
            # print(tradeVolPerMinute.split(','))
            if tradeVolPerMinute.split(',')[1].strip() != '':
                shanghaiIn.append(tradeVolPerMinute.split(',')[1])
                shenzhenIn.append(tradeVolPerMinute.split(',')[2])
    # print(shanghaiIn)
    # print(shenzhenIn)

    # x = np.array([2, 3, 4, 5, 6, 7, 8, 9])
    x = np.arange(0, len(shanghaiIn))
    # xx = pd.DataFrame({"k": x})
    # yy = pd.Series([20, 33, 44, 55, 66, 77, 88, 105])   # 口算都知道斜率是11,最终方程是y=11x
    yy = np.asarray(shanghaiIn, dtype="float64")
    sz_y = np.asarray(shenzhenIn, dtype="float64")

    X = sm.add_constant(x)
    model = sm.OLS(yy, X)
    sz_model = sm.OLS(sz_y, X)

    sh_results = model.fit()
    sz_results = sz_model.fit()

    print("shanghai <- hk [1d] | coef_const: " +
          str(round(sh_results.params[0], 4)) + ", x1: "+colours(round(sh_results.params[1], 4)))

    print("shenzhen <- hk [1d] | coef_const: " +
          str(round(sz_results.params[0], 4)) + ", x1: "+colours(round(sz_results.params[1], 4)))

    # print("\033[1;37;40m\tHello World\033[0m")
    # print(sh_results.summary())
    # y_fitted = sh_results.fittedvalues
    # sz_y_fitted = sz_results.fittedvalues
    # plt.figure(1)
    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.plot(x, yy, 'o', label='data')
    # ax.plot(x, y_fitted, 'r--.', label='OLS')
    # ax.legend(loc='best')

    # plt.figure(2)
    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.plot(x, sz_y, 'o', label='data')
    # ax.plot(x, sz_y_fitted, 'r--.', label='OLS')
    # ax.legend(loc='best')
    # plt.show()

def hk_to_mainland_several_d():
    hk_to_shenzhen_10d('shanghai')
    hk_to_shenzhen_10d('shenzhen')
    hk_to_shenzhen_10d('shanghai', 30)
    hk_to_shenzhen_10d('shenzhen', 30)


def hk_to_shenzhen_10d(stock_exchange, days=10):
    if stock_exchange == 'shenzhen':
        url = r'https://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?js=({IsSuccess:%271%27,result:(x)})&ps='+str(days) + \
            '&p=1&sr=-1&st=DetailDate&callback=result31360562&type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType%3D3)&rt=51765885&page=1&pagesize=10&_='+str(round(time.time() * 1000))
    else:
        url = r'https://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?js=({IsSuccess:%271%27,result:(x)})&ps='+str(days) + \
            '&p=1&sr=-1&st=DetailDate&callback=result18465975&type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType%3D1)&rt=51772229&page=1&pagesize=10&_='+str(round(time.time() * 1000))
    r = requests.get(url, headers=headers)
    html = str(r.text)
    # print(html)
    html_splited = html[html.find('result:[{')+9:len(html)-1].split('},{')
    # print(html_splited)

    hk_mainland_7d = {}
    list_drzjlr = [] 	# 当日资金流入
    for key, tradePerDay in enumerate(html_splited):
        for detail in tradePerDay.split(','):
            # print(detail.split(':', 1))
            if detail.split(':', 1)[0].replace('"', '') == "DetailDate":
                date = detail.split(':', 1)[1].replace('"', '').split('T')[0]
                hk_mainland_7d[date] = {}
            elif detail.split(':', 1)[0].replace('"', '') == "DRZJLR":
                hk_mainland_7d[date]['DRZJLR'] = detail.split(':', 1)[
                    1].replace('"', '')
                list_drzjlr.append(detail.split(':', 1)[1].replace('"', ''))

    # print(hk_mainland_7d)
    # print(list_drzjlr)
    # print(list_drzjlr[::-1])
    foo_x = np.arange(0, len(list_drzjlr))
    foo_y = np.asarray(list_drzjlr[::-1], dtype="float64")

    d10_X = sm.add_constant(foo_x)
    foo_model = sm.OLS(foo_y, d10_X)
    foo_results = foo_model.fit()
    # print(foo_results.params)
    print(stock_exchange+" <- hk ["+ str(days) +"d] | coef_const: " +
          str(round(foo_results.params[0]/100, 4)) + ", x1: "+colours(round(foo_results.params[1]/100, 4)))
    d10_y_fitted = foo_results.fittedvalues
    plt.figure(1)
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.arange(0, len(foo_y))
    ax.plot(x, foo_y, 'o', label='data')
    ax.plot(x, d10_y_fitted, 'r--.', label='OLS')
    ax.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    mainland_hk_pipe_last()
    hk_to_mainland_1d()
    hk_to_mainland_several_d()
