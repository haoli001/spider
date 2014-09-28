# -*- coding:utf-8 -*-
######################
#   程序：百度贴吧爬虫
#   版本：0.9
#   作者：昊海东青
#   日期：2014－09-28
#   语言：python2.7
#   功能：查看小说最近的更新章节，并可以查看内容
######################
import re
import urllib2
import urllib
import thread
import time
import chardet
import sys
#--------------- '加载处理贴吧'-------------

reload(sys)
sys.setdefaultencoding('utf-8')
#str转utf-8
class spider_model:
    def __init__(self):
        self.page=1
        self.pages=[]
    #待定
    
    def get_req(self,myurl):
        user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers ={'User-Agent':user_agent}
        req=urllib2.Request(myurl,headers=headers)
    	return req
    #模拟浏览器并且获得页面
    
    def get_depage(self,req):
        myresquest=urllib2.urlopen(req)
        mypage=myresquest.read()
        mychar=chardet.detect(mypage)
        bianma=mychar['encoding']
        if bianma!='utf-8' and bianma!='UTF-8':
            mypage=mypage.decode('gb2312','ignore').encode('utf-8')
        return mypage
    #获得编码后的页面

    def getpage(self,myurl):
         req=self.get_req(myurl)
         mypage=self.get_depage(req)
         res='<a href="(.*?)".*?title="(.*?[^"])".*?>.*?</a>'
         items=[]
         myitem=re.findall(res,mypage,re.S)
         for i in myitem:
             if i[1].decode()[0]==u'完' or i[1].decode()[0]==u'第' :
                 items.append([i[0],i[1].replace("\n","")])
         return items
#显示
    def showpage(self,items,n):
	 for i in range(n):
 		print(str(i)+'. '+items[i][1])
    def shownr(self,url,items,n):
	    if n>=0:
		    url=url+items[n][0]
		    print(url)
		    self.getnr(url)
	    else :
		    return
    def getnr(self,url):
	    user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	    headers={'User-Agent':user_agent}
	    req=urllib2.Request(url,headers=headers)
	    myresquest=urllib2.urlopen(req)
	    mypage=myresquest.read()
	    mychar=chardet.detect(mypage) 	
	    bianma=mychar['encoding']
	    if bianma!='utf-8' and bianma!='UTF-8':
	 	mypage=mypage.decode('gb2312','ignore').encode('utf-8')
                #匹配       
	    res='<br>(.[^abcdefghijklmnopqrstuvwxyz]*?)<br>'
	    items=[]
	    myitem=re.findall(res,mypage,re.S)
            for i in myitem:
		items.append(i.replace("\n",""))
	    for i in items:
	    	print(i)
	    return items

############
wz=["http://tieba.baidu.com/f/good?kw=%CD%EA%C3%C0%CA%C0%BD%E7%D0%A1%CB%B5&tab=good&cid=4",
    "http://tieba.baidu.com/f/good?kw=%B1%A6%BC%F8&cid=1",
    "http://tieba.baidu.com/f/good?kw=%C3%A7%BB%C4%BC%CD&tab=good&cid=2",
    "http://tieba.baidu.com/f/good?kw=%C5%D1%C4%E6%B5%C4%D5%F7%CD%BE&cid=2"]

############
w=spider_model()
while 1:
    gg=input("输入想看的书的编号\n0.完美世界\n1.宝鉴\n2.莽荒纪\n3.叛逆的征途\n")
    if(gg>=0):
        wan=w.getpage(wz[gg])
        w.showpage(wan,10)
        while 1:
            pp=input("输入想看的章节编号或者－1退出")
            if(pp<0):
                break
            else:
                w.shownr('http://tieba.baidu.com',wan,pp)
                w.showpage(wan,10)
    else:
        break

