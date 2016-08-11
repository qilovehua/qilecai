import re
import urllib2
import datetime
from py_db_lib import mongoDB

year=datetime.date.today().year
year_list=[year for year in xrange(year,2006,-1)]
#year_list=[2015,]
url="http://baidu.lecai.com/lottery/draw/list/51?d=%s-01-01"
testurl="http://baidu.lecai.com/lottery/draw/list/51?d=2015-01-01"

re_all=re.compile(r'''<tbody>(.*?)</tbody>''', re.DOTALL)
re_list=re.compile(r'''<tr class="bgcolor[0-9]">(.+?)</tr>''', re.DOTALL)
re_lottery_date=re.compile(r'''<td class="td1">([0-9]{4}-[0-9]{2}-[0-9]{2})</td>''')
re_number=re.compile(r'''<a href="/lottery/draw/view/51\?phase=[0-9]{7}">([0-9]{7})</a>''')
re_ball_basic=re.compile(r'''<span class="ball_1">([0-9]{2})</span>''')
re_ball_special=re.compile(r'''<span class="ball_2">([0-9]{2})</span>''')
re_ball_sale=re.compile(r'''<td class="td4">(.+?)</td>''')



class lottery:
    
    req=None
    year=None
    mongodb=None
    
    def __init__(self,year=year):
        #self.req=self.getLatestReq(year)
        self.mongodb=mongoDB()
        
    def close(self):
        if self.req is not None:
            self.req.close()
            self.req=None
        if self.mongodb is not None:
            self.mongodb.closeDB()
    
    # main function to get lottery info        
    def getAllLottery(self):
        for year in year_list:
            self.getLatestReq(year)
            ret=self.getLotteryInfo()
            if ret != 0:
                break
        print "Done..."
        
    def getLatestReq(self,year=year):
        if self.year is None:
            self.year=year
        elif self.year != year:
            # return a new req
            self.close()
            self.year=year
        else:
            pass
            
        if self.req is None:
            self.req=urllib2.urlopen(url % str(year),'',30)
        return self.req
    
    # url page info
    def getPage(self):
        pageContent=self.req.read()
        return pageContent
    
    # url <tbody> ... </tbody>
    def getAll(self):
        pageContent=self.getPage()
        userfull_info=re_all.findall(pageContent)
        # userfull_info is a list, just return the first one
        return userfull_info[0]
    
    # <tr> ... </tr>
    # return a list
    def getList(self,userfull_info):
        lottery_list=re_list.findall(userfull_info)
        return lottery_list
    
    # get lottery info
    # put all the lottery info into mongodb
    def getLotteryInfo(self):
        userfull_info=self.getAll()
        lottery_list=self.getList(userfull_info)
        current_maxnum=self.getMaxNum()
        dictLottery={}
        for lottery_info in lottery_list:
            dictLottery['lottery_date'] = self.getDate(lottery_info)
            dictLottery['lottery_num'] = self.getNumber(lottery_info)
            dictLottery['lottery_ball'] = self.getBall(lottery_info)
            dictLottery['lottery_sale'] = self.getSall(lottery_info)
            print dictLottery
            if current_maxnum == dictLottery['lottery_num']:
                print "lottery info is up-to-day, no new insert is needed." 
                return 1
            self.mongodb.insert(dictLottery)
        return 0
    
    # lottery_info - str
    # lottery_info is lottery_list[N]
    def getDate(self,lottery_info):
        lottery_date=re_lottery_date.findall(lottery_info)
        return lottery_date[0]
    
    def getNumber(self,lottery_info):
        lottery_num=re_number.findall(lottery_info)
        return lottery_num[0]
    
    def getBall(self,lottery_info):
        # lotter_ball_basic include 7 numbers
        lottery_ball_basic=re_ball_basic.findall(lottery_info)
        # lotter_ball_special include one number
        lottery_ball_special=re_ball_special.findall(lottery_info)
        return [lottery_ball_basic,lottery_ball_special[0]]
    
    def getSall(self,lottery_info):
        lottery_ball_sale=re_ball_sale.findall(lottery_info)
        return lottery_ball_sale[0]
    
    def getMaxNum(self):
        return self.mongodb.getMaxNum()
    
    def getMinNum(self):
        return self.mongodb.getMinNum()


# req=urllib2.urlopen(url % str(year),'',30)
# pageContent=req.read()
# # print(len(pageContent))
# userfull_info=re_all.findall(pageContent)
# lottery_list=re_list.findall(userfull_info[0])
# print lottery_list[0]
# print "======================================="
# print lottery_list[1]
# print "======================================="
# lottery_date=re_lottery_date.findall(lottery_list[0])
# lottery_num=re_number.findall(lottery_list[0])
# lottery_ball_basic=re_ball_basic.findall(lottery_list[0])
# lottery_ball_special=re_ball_special.findall(lottery_list[0])
# lottery_ball_sale=re_ball_sale.findall(lottery_list[0])
# print lottery_date[0]
# print lottery_num[0]
# print str(lottery_ball_basic)
# print lottery_ball_special[0]
# print lottery_ball_sale[0]
