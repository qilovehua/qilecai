from py_url_lib import lottery
from py_db_lib import mongoDB

if __name__ == '__main__':
#     mylottery=lottery()
# #     mylottery.getAllLottery()
# #     print "the max num is: ",mylottery.getMaxNum()
#     print "the min num is: ",mylottery.getMinNum()
#     mylottery.close()
    
    mydb=mongoDB()
#     ll=mydb.getRecordByYear(2014,2015)
#     print len(ll)
    ll=mydb.getBallSpecial(2013, oneyear=False)
    for x in ll:
        print x
    mydb.closeDB()