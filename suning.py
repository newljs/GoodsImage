import requests
import time
import os

def suning_gimg(goodshtml_text,skuId,pathdate):
    goods_titles = goodshtml_text.xpath('//title/text()')  # xpath截取内容
    goodsshowurls = goodshtml_text.xpath('//img[@onload="if(this.width>750){this.height=this.height*(750.0/this.width); this.width = 750;}"]/@src2')#xpath截取内容
    goods_imgs_it = goodshtml_text.xpath('//div[@class="imgzoom-thumb-main"]/ul/li/a/img/@src-large')#xpath截取内容
    for goods_title in goods_titles:  # 遍历商品名称列表
        goods_title=goods_title.replace(' ','').replace('{content}','')
        if goods_title:
            print('正在抓取苏宁易购商品：%s' % goods_title)
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
            num = 1
            for goodsshowurl in goodsshowurls:  # 遍历商品详情图列表
                if 'https://' in goodsshowurl:
                    showdescimgurl = requests.get(goodsshowurl)
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
                    showdescimgurl = requests.get('http:' + goodsshowurl)
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
                goods_img_url = requests.get('http:' + goods_imgs)
                open(str(goodsimg_path) + '/' + 'f' + str(f_num) + '.jpg', 'wb').write(goods_img_url.content)
                print('保存封面图片%d.jpg成功' % f_num)
                time.sleep(1)
                f_num = f_num + 1
            print('商品：%s抓取完毕，正在获取下一个商品信息' % goods_title)
        else:
            pass
    time.sleep(2)