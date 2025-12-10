import sqlite3
import os
from config import BASE_DIR

class Common():

    def select(db="",sql=""):
        conn=sqlite3.connect(os.path.join(BASE_DIR,"db",db+".db"))
        cursor=conn.cursor()
        result=cursor.execute(sql)
        conn.commit()
        resultset= cursor.fetchall()
        #print("结果集:",resultset)
        col_name_list = [tuple[0] for tuple in cursor.description]
        #print("结果集字段名:",col_name_list)
        if len(resultset)==0:
            result={col_name_list[0]:None}
            for i in range(1,len(col_name_list)):
               result[col_name_list[i]]=None
            #print("空结果集:",[result])
            return [result]
        elif len(resultset)==1:
            #print("单行结果集:",[dict(zip(col_name_list,resultset[0]))])
            return [dict(zip(col_name_list,resultset[0]))]
        else:
            result_list=[dict(zip(col_name_list,resultset[0]))]
            for i in range(1,len(resultset)):
                result_list+=[dict(zip(col_name_list,resultset[i]))]
            #print("result_list:",result_list)
            return result_list
            

    
    def execute(db="",sql=""):
        conn=sqlite3.connect(os.path.join(BASE_DIR,"db",db+".db"))
        cursor=conn.cursor()
        result=cursor.execute(sql)
        conn.commit()
        return result