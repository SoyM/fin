# !/usr/bin/python2
# -*- coding: utf-8 -*-
import sys
import datetime
import urllib2
import sys
import json
import glob

def get_index(fund_code, all_fund_list):
    fund_num = len(all_fund_list)
    fund_index = 0
    while fund_index < fund_num:
        if fund_code in all_fund_list[fund_index]:
            break
        fund_index += 1

    return fund_index

def get_type(fund_code, all_fund_list):
    fund_type = 'none'
    for fund in all_fund_list:
        if fund_code in fund:
            fund_type = fund[3]
            break

    return fund_type


def main():
    strtoday = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    tdatetime = datetime.datetime.strptime(strtoday, '%Y-%m-%d')
    print(strtoday)

    sdatetime = tdatetime - datetime.timedelta(days=365)
    strsdate = datetime.datetime.strftime(sdatetime, '%Y-%m-%d')
    print(strsdate)

    all_fund = []
    fundlist_files = glob.glob('fundlist-*.txt')
    file_object = open(fundlist_files[0], 'r')
    try:
        all_funds_txt = file_object.read()
        # print all_funds_txt
    finally:
        file_object.close()

    all_funds_txt = all_funds_txt[all_funds_txt.find(
        '=')+2:all_funds_txt.rfind(';')]
    all_fund = json.loads(all_funds_txt.decode('utf-8'))

    # 1、 获取近 1 3 6 增长率top50
    month_num = 1
    # month_list = [1, 3]
    month_list = [1, 3, 6, 12]
    all_fund_list = []

    for int_month in month_list:
        try:
            if int_month == 12:
                # 1年增幅
                print('get nearly 1 year top 50 funds')
                url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=1nzf,50&gs=0&sc=1nzf&st=desc&sd=' + \
                    strsdate + '&ed=' + strtoday + '&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1'
            else:
                # 前 n 月增幅
                print('get nearly ' + str(int_month) + ' months top 50 funds')
                url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=' + str(int_month) + \
                    'yzf,50&gs=0&sc=' + str(int_month) + 'yzf&st=desc&sd=' + strsdate + '&ed=' + strtoday + \
                    '&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1'
            # print url + '\n'
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            print(e)
            urllib_error_tag = True
        except StandardError, e:
            print(e)
            urllib_error_tag = True
        else:
            urllib_error_tag = False

        if urllib_error_tag == True:
            print('error to get date,check network!\n')
            sys.exit(1)

        # print response
        all_rank_txt = response.read().decode('utf-8')
        all_rank_txt = all_rank_txt[all_rank_txt.find(
            '["'):all_rank_txt.rfind('"]')+2]
        # print all_rank_txt
        all_rank_list = json.loads(all_rank_txt)
        # print 'rank sum:' + str(len(all_rank_list)) + '\n\n'

        fund_rank = 1
        for rank_txt in all_rank_list:

            rank_list = rank_txt.split(',')
            # print str(len(rank_list)) + '\n'
            if 1 == month_num:
                fund_list = []

                fund_type = get_type(rank_list[0], all_fund)

                fund_list.append(rank_list[0])
                fund_list.append(rank_list[1] + '\t' + fund_type)
                fund_list.append(str(fund_rank))

                all_fund_list.append(fund_list)
            else:
                # 查找是否已在list中
                fund_num = len(all_fund_list)
                fund_index = get_index(rank_list[0], all_fund_list)
                if fund_index < fund_num:
                    # list中已存在 只append rank 和 rate
                    # print fund_code + '\t' + str(fund_index) + '\t' + str(all_fund_list[fund_index])
                    all_fund_list[fund_index].append(str(fund_rank))
                else:
                    # 如果不存在 不仅需要将其加入list中 同样需要将其他几个 rank 和 rate 补上
                    # 如果本fundcode在前几个文件中不存在 就是倒数第一 第100名吧 rank 默认100 rate 默认0
                    # print fund_code + '\tnot found!'
                    fund_list = []
                    # code name type
                    fund_type = get_type(rank_list[0], all_fund)

                    fund_list.append(rank_list[0])
                    fund_list.append(rank_list[1] + '\t' + fund_type)
                    # 补上 前几个文件的 rank 和 rate
                    for i in range(month_num - 1):
                        fund_list.append('100')
                    # 加上当前的rank 和 rate
                    fund_list.append(str(fund_rank))

                    # 将其加入列表
                    all_fund_list.append(fund_list)

            # 处理下一个
            fund_rank += 1

        # 还有 从第2个月开始 如果有fund 不在本文件中出现 就是倒数第一 第100名吧 还要将rank 和 rate 补上 擦 挺复杂
        if month_num > 1:
            # 最长的len 为 2 + month_num
            fund_len = 2 + month_num
            fund_num = len(all_fund_list)
            fund_index = 0
            while fund_index < fund_num:
                if len(all_fund_list[fund_index]) < fund_len:
                    all_fund_list[fund_index].append('100')

                fund_index += 1

        # 处理下一个月
        month_num += 1

    print month_num
    # print all_fund_list[0]
    # print all_fund_list[1]

    # 2、计算平均排名
    fund_num = len(all_fund_list)
    print fund_num
    print '\n\n'
    fund_index = 0
    while fund_index < fund_num:
        sum_rank = 0
        # 有几个文件 就有几个排名 rank的index 2 3 4 5
        for i in range(month_num - 1):
            sum_rank += int(all_fund_list[fund_index][2 + i])

        # 计算平均排名
        avg_rank = float('%.2f' % (float(sum_rank) / (month_num - 1)))

        # 加入avg_rank
        all_fund_list[fund_index].append(avg_rank)

        # 处理下一个
        fund_index += 1

    # 3、排序 写文件 打印
    # avg_rank的index 1 + month_num
    all_fund_list.sort(key=lambda fund: fund[1 + month_num])

    # print all_fund_list[0]
    # print all_fund_list[1]

    file_object = open('results-zf.txt', 'w')
    int_rank = 1
    rank_company = {}
    try:
        for fund_list in all_fund_list:

            if rank_company.has_key(fund_list[1][0:2]):
                rank_company[fund_list[1][0:2]] = rank_company[fund_list[1][0:2]] + 1
            else:
                rank_company[fund_list[1][0:2]] = 1

            if fund_list[1][0:2] == "前海":
                bg_color = "\033[1;;41m"
            elif fund_list[1][0:2] == "国泰":
                bg_color = "\033[1;;42m"
            elif fund_list[1][0:2] == "金鹰":
                bg_color = "\033[1;;43m"
            elif fund_list[1][0:2] == "南方":
                bg_color = "\033[1;;44m"
            elif fund_list[1][0:2] == "博时":
                bg_color = "\033[1;;45m"
            else:
                bg_color = ""

            if bg_color == "":
                print str(int_rank) + '\t' + '\t'.join('{0}'.format(n) for n in fund_list)
            else:
                print bg_color+str(int_rank) + '\t' + '\t'.join('{0}'.format(n) for n in fund_list)+"\033[0m"

            file_object.write(
                str(int_rank) + '\t' + '\t'.join('{0}'.format(n) for n in fund_list) + '\n')

            int_rank += 1
    finally:
        file_object.close()
    
    rank_company = sorted(rank_company.items(), key=lambda d:d[1], reverse = True)

    for per_rank_company in rank_company:
        if per_rank_company[1] == 1:
            break
        print("{company}: {num}".format(company=per_rank_company[0],num=per_rank_company[1]))


    sys.exit(0)


def test():
    month_num = 1

    print month_num


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # sys.setdefaultencoding('GBK')
    # test()
    main()
