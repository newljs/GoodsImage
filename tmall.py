import requests
import time
import os
import re
from lxml import etree

def tmall_gimg(goodshtml_text,goodshtml,skuId,pathdate):
    goods_titles = goodshtml_text.xpath('//title/text()')  # xpath截取内容
    goodsshowurls = re.findall('.*"descUrl":"(.*)","fetchDcUrl":.*', goodshtml.text)  # 通过re截取无规则html中“desc: '”//到“',”的内容
    goods_imgs_it = goodshtml_text.xpath('//div[@class="tb-thumb-content"]/ul/li/a/img/@src')#xpath截取内容
    for goods_title in goods_titles:  # 遍历商品名称列表
        goods_title=goods_title.replace(' ','')
        if goods_title:
            print('正在抓取天猫商品：%s' % goods_title)
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

            for goodsshowurl in goodsshowurls:  # 遍历商品详情图列表
                hpgoodsshowurl = 'http:' + goodsshowurl
                # headers='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'#模拟浏览器
                showdesc = requests.get(hpgoodsshowurl)  # 通过requests.get获取网络数据
                s = etree.HTML(showdesc.text)  # 通过lxml模块中的etree将数据转换成html可读取内容
                showdescimgurls = s.xpath('//img/@src')  # xpath截取内容
                num = 1
                for i in showdescimgurls:  # 读取列表中的数据
                    showdescimgurl = requests.get(i)  # 截取字符串，从第5位到倒数第2位
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
            print('抓取商品详情图片成功，正在获取商品封面图---')
            f_num = 1
            for goods_imgs in goods_imgs_it:  # 遍历商品封面图列表
                goods_imgs=goods_imgs.replace('_60x60q90.jpg','')
                goods_img_url = requests.get('http:' + goods_imgs)
                open(str(goodsimg_path) + '/' + 'f' + str(f_num) + '.jpg', 'wb').write(goods_img_url.content)
                print('保存封面图片%d.jpg成功' % f_num)
                time.sleep(1)
                f_num = f_num + 1
            print('商品：%s抓取完毕，正在获取下一个商品信息' % goods_title)
        else:
            pass
    time.sleep(2)