import requests
import re
from lxml import etree
import time
import os

def jd_gimg(goodshtml_text,goodshtml,skuId,pathdate):
    goods_titles = goodshtml_text.xpath('//div[@class="item ellipsis"]/text()')  # xpath截取内容
    goodsshowurls = re.findall(".*desc: '//(.*)',.*", goodshtml.text)  # 通过re截取无规则html中“desc: '”//到“',”的内容
    goods_imgs_it_bf = goodshtml_text.xpath('//ul[@class="lh"]/li/img/@src')  # xpath截取内容
    goods_imgs_it = re.findall(".*imageList:(.*)],.*", goodshtml.text)  # 通过re截取无规则html中“mageList:”//到“],”的内容
    for goods_title in goods_titles:  # 遍历商品名称列表
        print('正在抓取京东商品：%s' % goods_title)
        print('链接：%s' % skuId)
        time.sleep(1)
        goods_title = goods_title.replace('/', ' ').replace('*', 'x').replace('?', ' ').replace(':', ' ').replace('\\', ' ').replace('<', ' ').replace('>', ' ').replace('|', ' ')  # .replace:替换字符;
        goodsimg_path = "./goodsimg/" + pathdate + "/" + str(goods_title)
        if os.path.exists(goodsimg_path):
            print("目录已存在,等待抓取图片")
            time.sleep(1)
        else:
            os.makedirs(goodsimg_path)  # 创建以商品名为名的文件夹路径
            print('创建目录：%s成功,正在获取商品详情图片---' % goodsimg_path)
            time.sleep(1)
        # 获取商品详情图片隐藏
        for goodsshowurl in goodsshowurls:  # 遍历商品详情图列表
            hpgoodsshowurl = 'http://' + goodsshowurl
            # headers='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'#模拟浏览器
            showdesc = requests.get(hpgoodsshowurl)  # 通过requests.get获取网络数据
            s = etree.HTML(showdesc.text)  # 通过lxml模块中的etree将数据转换成html可读取内容
            showdescimgurls = s.xpath('//img/@data-lazyload')  # xpath截取内容
            num = 1
            if showdescimgurls:  # 判断showdescimgurls是否为空，京东的商品详情图片存储分为两种形式，所以需要两种代码抓取
                for i in showdescimgurls:  # 读取列表中的数据
                    showdescimgurl = requests.get('http://' + i[4:-2])  # 截取字符串，从第5位到倒数第2位
                    # webimg=requests.get(showdescimgurl)
                    time.sleep(1)
                    if showdescimgurl.url[-3:] == 'jpg':  # 截取字符串判断文件后缀名
                        open(str(goodsimg_path) + '/' + str(num) + '.jpg', 'wb').write(showdescimgurl.content)
                        print('抓取商品详情图片%d.jpg成功' % num)
                    elif showdescimgurl.url[-3:] == 'gif':
                        open(str(goodsimg_path) + '/' + str(num) + '.gif', 'wb').write(showdescimgurl.content)
                        print('抓取商品详情图片%d.gif成功' % num)
                    else:
                        open(str(goodsimg_path) + '/' + str(num) + '.png', 'wb').write(showdescimgurl.content)
                        print('抓取商品详情图片%d.png成功' % num)
                    num = num + 1
            else:
                showdescimgurls = re.findall(".*; background-image:url((.*))}.*",
                                             goodshtml.text)  # 通过re截取无规则html中“; background-image:url(”到“)}”的内容
                for i in showdescimgurls:  # 读取列表中的数据
                    i = tuple(set(i))
                    for ii in i:
                        ii = ii.replace('(', '').replace(')', '')  # .replace:替换字符;.split(',')将字符串转换成列表
                        if 'http' in ii:
                            showdescimgurl = requests.get(ii)
                        else:
                            showdescimgurl = requests.get('http:' + ii)
                        time.sleep(1)
                        if showdescimgurl.url[-3:] == 'jpg':  # 截取字符串判断文件后缀名
                            open(str(goodsimg_path) + '/' + str(num) + '.jpg', 'wb').write(showdescimgurl.content)
                            print('抓取商品详情图片%d.jpg成功' % num)
                        elif showdescimgurl.url[-3:] == 'gif':
                            open(str(goodsimg_path) + '/' + str(num) + '.gif', 'wb').write(showdescimgurl.content)
                            print('抓取商品详情图片%d.gif成功' % num)
                        else:
                            open(str(goodsimg_path) + '/' + str(num) + '.png', 'wb').write(showdescimgurl.content)
                            print('抓取商品详情图片%d.png成功' % num)
                        num = num + 1
        print('抓取商品详情图片成功，正在获取商品封面图---')
        f_num = 1
        if goods_imgs_it:
            for goods_imgs in goods_imgs_it:  # 遍历商品封面图列表
                goods_imgs = goods_imgs.replace('[', '').replace('"', '').strip().strip(',').split(
                    ',')  # .replace:替换字符;.split(',')将字符串转换成列表
                for goods_img in goods_imgs:
                    goods_img_url = requests.get('https://img13.360buyimg.com//n0/' + goods_img)
                    open(str(goodsimg_path) + '/' + 'f' + str(f_num) + '.jpg', 'wb').write(goods_img_url.content)
                    print('保存封面图片%d.jpg成功' % f_num)
                    time.sleep(1)
                    f_num = f_num + 1
        else:
            for goods_imgs in goods_imgs_it_bf:
                goods_imgs=goods_imgs.replace('//img11.360buyimg.com/n5/','')
                print(goods_imgs)
                goods_img_url = requests.get('https://img13.360buyimg.com//n0/' + goods_imgs)
                open(str(goodsimg_path) + '/' + 'f' + str(f_num) + '.jpg', 'wb').write(goods_img_url.content)
                print('保存封面图片%d.jpg成功' % f_num)
                time.sleep(1)
                f_num = f_num + 1
        print('商品：%s抓取完毕，正在获取下一个商品信息' % goods_title)
    time.sleep(2)