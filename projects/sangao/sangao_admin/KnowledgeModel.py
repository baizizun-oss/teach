from common.CommonModel import Common

class Knowledge():
    def select(id=""):
        if id=="":
            sql="select * from knowledge"
        else:
            sql="select * from knowledge where id="+id

        knowledges=Common.select("sangao",sql)
        return knowledges

        