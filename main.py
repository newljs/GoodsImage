from jd import *
from suning import *
from tmall import *
from taobao import *
from jiuxian import *
import requests
from lxml import etree
import time

txtpath = r"url.ini"
fp=open(txtpath)
skuIds=[]
for lines in fp.readlines():
    lines = lines.replace("\n", "")
    if lines:
        skuIds.append(lines)
    else:
        pass
fp.close()
pathdate=time.strftime("%Y%m%d", time.localtime())

for skuId in skuIds:
    if '.com' in skuId:
        goodshtml=requests.get(skuId,allow_redirects=False)
        goodshtml_302=requests.get(skuId)
        goodshtml_text = etree.HTML(goodshtml.text)  # 通过lxml模块中的etree将数据转换成html可读取内容
        goodshtml_text_302 = etree.HTML(goodshtml_302.text)  # 通过lxml模块中的etree将数据转换成html可读取内容
        if 'jd.com' in skuId:
            if goodshtml.status_code == 200:
                jd_gimg(goodshtml_text, goodshtml, skuId, pathdate)
            else:
                print('%s 商品链接错误,可能已被删除' % skuId)
        elif 'suning.com' in skuId:
            if goodshtml.status_code == 200:
                suning_gimg(goodshtml_text, skuId, pathdate)
            else:
                print('%s 商品链接错误,可能已被删除' % skuId)
        elif 'jiuxian.com' in skuId:
            if goodshtml.status_code == 200:
                jiuxian_gimg(goodshtml_text, skuId, pathdate)
            else:
                print('%s 商品链接错误,可能已被删除' % skuId)
        elif 'tmall.com' in skuId:
            tmall_gimg(goodshtml_text_302, goodshtml_302, skuId, pathdate)
        elif 'taobao.com' in skuId:
            taobao_gimg(goodshtml_text_302, goodshtml_302, skuId, pathdate)
    else:
        print('链接错误，进行下一个')
print('抓取完毕')