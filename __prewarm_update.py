#encoding:utf-8
# -*- coding: utf-8 -*-

import sys
import socket
from concurrent.futures import ThreadPoolExecutor
import http.client
import csv
import importlib
import os

importlib.reload(sys)

#reload(sys) 
#sys.setdefaultencoding('utf-8')

file_context = open("file.txt").read().splitlines()
#file_context = ["http://d2r0qln3p9n9mv.cloudfront.net/example-1.png"]
#domain = "l13-prod-patch-ua3.komoejoy.com"
domain = "xxxxx.example.com"  # 您的实际的自定义域名, 如果您有CNAME,则填写您的实际CNAME(xxx.example.com)，如无，则domain是xxx.cloudfront.net
#http_domain = "https://xxx.xxx.com"
cdn_name = 'xxxx.cloudfront.net'
cur_pops = "pops.csv"
result_file = "result.csv"
no_ip_file = "no_ip_file.csv"
cache_index = 0


def saveStringToCsv(inputString, file_path):
    #f = open(file_path, "w")
    out = open(file_path, 'a',encoding="utf-8",newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(inputString)


def CdnWarm(ip, url, dn, pop):
    global cache_index
    try:
        conn = http.client.HTTPConnection(ip)  # IP地址
        conn.request(method="GET",  # 以GET的方式发送请求
                     url=url,  # 请求的web路径
                     headers={'Host': dn,  # 请求头里面的主机名，
                              "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, lik e Gecko) Chrome/33.0.1750.152 Safari/537.36",
                              # 模拟浏览器
                              "Referer": "im is test"})  # 请求来源
        response = conn.getresponse()  # 获取CDN的回应内容信息
        data1=response.read()
        f1=open("test.jpg", "wb")
        f1.write(data1)
        f1.close()
        headers = response.getheaders()

        #print(response.status)  # 输出http状态码
        conn.close()  # 链接关闭

        if os.path.exists("test.jpg"):
            os.remove("test.jpg")
        else:
            print("The file does not exist")


        if cache_index == 0:
            while str(headers[cache_index]).find("from cloudfront") < 0:
                cache_index = cache_index + 1

        result = [pop, cdn_name % (pop), url, response.status, response.getheaders()[cache_index]]
        saveStringToCsv(result, result_file)
        print(result)
        if (response.getheaders()[cache_index]) == 'Miss from cloudfront':
            CdnWarm(ip, url, dn, pop)

    except BaseException as e:
        print(" ====================================")
        print("||      " + ip + "   error       ||")
        print(e)
        print(" ====================================")
        result = [pop, cdn_name % (pop), url, e]
        saveStringToCsv(result, result_file)


def getCdnIP(url):
    try:
        return socket.gethostbyname(url)
    except Exception as e:
        #print
        return 0
        #return ("IP解析出现错误：%s" % e)


def CdnThreadFunc():
    global cdn_name
    # cdn_name = 'd1s4q8j0xxxxx.cloudfront.net'
    cdnUrls = cdn_name.split(".")
    cdn_name = cdnUrls[0] + ".%s." + cdnUrls[1] + "." + cdnUrls[2]
    with ThreadPoolExecutor(100) as executor:
        with open(cur_pops,encoding="gbk") as csvfile:
            csv_reader = csv.reader(csvfile)
            for cdn in csv_reader:
                #if cdn[2] != "中国" and cdn[2] != "日本" and cdn[2] != "韩国" and cdn[2] != "新加坡" \
                #        and cdn[1] != "旧金山国际机场" and cdn[1] != "华盛顿杜勒斯国际机场":
                #    continue
                low_pop = cdn[0].lower()
                new_cdn = cdn_name % (low_pop)  #new_cdn=xxxx.hkg-10.cloudfront.net
                ip = getCdnIP(new_cdn)
                if ip == 0:
                    list = [cdn, new_cdn, "无法解析该pop点"]
                    saveStringToCsv(list, no_ip_file)
                    print(list)
                    #continue
                for url in file_context:
                    low_pop = cdn[0].lower()
                    new_url = url.replace("http://", "")
                    new_url = new_url.replace("https://", "")
                    new_url = new_url.replace(domain, "")   # 应该是只留下路径
                    task = executor.submit(CdnWarm, new_cdn, new_url, domain, low_pop)


CdnThreadFunc()
