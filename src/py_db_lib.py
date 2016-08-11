import pymongo
from pymongo import MongoClient
import datetime

year=datetime.date.today().year

class mongoDB:
    
    db=None
    client=None
    
    def __init__(self):
        self.db=self.getDB()
        
    def getDB(self):
        if self.client is None:
            self.client=MongoClient("mongodb://192.168.137.162:27017")
            self.db=self.client.test
        return self.db
    
    def closeDB(self):
        if self.client is not None:
            self.client.close()
    
    def insert(self,dictLottery):
        cursor=self.db.lottery.find({"_id":dictLottery['lottery_num']})
        if cursor.count() == 0:
            # insert a new one
            self.db.lottery.insert_one(
                {
                     "lottery_date":dictLottery['lottery_date'],
                     "_id":dictLottery['lottery_num'],
                     "lottery_ball":[
                        {
                         "lottery_basic":dictLottery['lottery_ball'][0],
                         "lottery_special":dictLottery['lottery_ball'][1]
                         }             
                    ],
                     "lottery_sale":dictLottery['lottery_sale']
                 }                                   
            )
        #update, insert new collumn
        else:
            pass
            self.db.lottery.update_one(
                {"_id":dictLottery['lottery_num']},
                {
                    "$set":{
                        "aaa":"just a test"
                    }
                 }
            )
            
    def getRecordByYear(self,minyear,maxyear=year+1):
        '''
            if minyear equal to maxyear, get record of that year
            if minyear not equal to maxyear, get record between minyear and maxyear(uninclue)
        '''
        if minyear == maxyear:
            cursor=self.db.lottery.find({"_id":{"$gte":str(minyear)+"000","$lte":str(maxyear)+"999"}})
        else:
            cursor=self.db.lottery.find({"_id":{"$gte":str(minyear)+"000","$lte":str(maxyear)+"000"}})
        c_list=[]
        for c in cursor:
            c_list.append(c)
        return c_list
    
    def getMinNum(self):
        cursor=self.db.lottery.find({},{"_id":1}).sort([("_id",pymongo.ASCENDING)]).limit(1)
        for c in cursor:
            # type: dict
            #print "Type: ",type(c)
            return c["_id"]
    
    def getMaxNum(self):
        # get max _id in db.lottery(collection)
        cursor=self.db.lottery.find({},{"_id":1}).sort([("_id",pymongo.DESCENDING)]).limit(1)
#        cursor=self.db.lottery.aggregate([
#                 {
#                     "$group":
#                         {
#                             "_id":"$_id",
#                             "maxNum":{"$max":"$_id"}
#                         }
#                 },
#                 {
#                     "$sort":
#                         {"_id":-1} #desc
#                 },
#                 {
#                     "$limit":1
#                 }
#             ]
#         )
        for c in cursor:
            return c['_id']
    
    def getBallSpecial(self,cyear=None,oneyear=True):
        '''
            get ball num by group
            if oneyear is true, just calculate one year
            else calcute the record from that year to current year
        '''
        if cyear is None:
            cyear=year
        if oneyear:
            cursor=self.db.lottery.aggregate(
                [
                    {
                        "$match":
                            {
                            "_id":{"$gte":str(year)+"000"}
                             }
                     },
                    {
                        "$group":
                            {
                             "_id":"$lottery_ball.lottery_special",
                             "count":{"$sum":1}
                             }
                     },
                     {
                        "$sort":
                            {
                             "_id":1 # ASC
                             }
                      }
                 ]
            )
        else:
            cursor=self.db.lottery.aggregate(
                [
                    {
                        "$match":
                            {
                            "_id":{"$gte":str(cyear)+"000", "$lte":str(year+1)+"000"}
                             }
                     },
                    {
                        "$group":
                            {
                             "_id":"$lottery_ball.lottery_special",
                             "count":{"$sum":1}
                             }
                     },
                     {
                        "$sort":
                            {
                             "_id":1 # ASC
                             }
                      }
                 ]
            )
        special_list=[]
        for c in cursor:
            special_list.append(c)
        return special_list
        
    def test(self):
        cursor=self.db.user.find({},{"_id":0,"name":1,"age":1})
        for ducumnet in cursor:
            print ducumnet