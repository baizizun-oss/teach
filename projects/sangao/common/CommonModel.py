import sqlite3
import os
from config import BASE_DIR

class Common():

    # def select(db="",sql=""):
    #     conn=sqlite3.connect(os.path.join(BASE_DIR,"db",db+".db"))
    #     cursor=conn.cursor()
    #     result=cursor.execute(sql)
    #     conn.commit()
    #     resultset= cursor.fetchall()
    #     #print("结果集:",resultset)
    #     col_name_list = [tuple[0] for tuple in cursor.description]
    #     #print("结果集字段名:",col_name_list)
    #     if len(resultset)==0:
    #         result={col_name_list[0]:None}
    #         for i in range(1,len(col_name_list)):
    #            result[col_name_list[i]]=None
    #         #print("空结果集:",[result])
    #         return [result]
    #     elif len(resultset)==1:
    #         #print("单行结果集:",[dict(zip(col_name_list,resultset[0]))])
    #         return [dict(zip(col_name_list,resultset[0]))]
    #     else:
    #         result_list=[dict(zip(col_name_list,resultset[0]))]
    #         for i in range(1,len(resultset)):
    #             result_list+=[dict(zip(col_name_list,resultset[i]))]
    #         #print("result_list:",result_list)
    #         return result_list


    def execute(db_name, sql, parameters=()):
        """
        执行单条 SQL 语句（支持参数化查询）
        
        :param db_name: 数据库名（如 "sangao"），对应 db/{db_name}.db
        :param sql: SQL 语句，使用 ? 作为占位符
        :param parameters: 参数元组
        :return: fetchall() 结果（如果是查询）或 None
        """
        db_path = os.path.join(BASE_DIR, "db", f"{db_name}.db")
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(sql, parameters)  # ✅ 安全的参数化查询
            if sql.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = None
            return result
        finally:
            conn.close()


            
    def select(db="", sql="", parameters=()):
        """
        执行 SELECT 查询（支持参数化查询）
        
        :param db: 数据库名（如 "sangao"），对应 db/{db_name}.db
        :param sql: SQL 查询语句，使用 ? 作为占位符
        :param parameters: 参数元组，默认为空元组
        :return: 字典列表，每个元素是一行记录
        """
        db_path = os.path.join(BASE_DIR, "db", db + ".db")
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            if parameters:
                cursor.execute(sql, parameters)  # 使用参数化查询
            else:
                cursor.execute(sql)  # 兼容旧用法
            
            resultset = cursor.fetchall()
            col_name_list = [tuple[0] for tuple in cursor.description] if cursor.description else []
            
            if not col_name_list:  # 无结果集字段
                return []
                
            if len(resultset) == 0:
                # 空结果集：返回带 None 值的字典
                result = {col_name: None for col_name in col_name_list}
                return [result]
            elif len(resultset) == 1:
                # 单行结果集
                return [dict(zip(col_name_list, resultset[0]))]
            else:
                # 多行结果集
                result_list = [dict(zip(col_name_list, row)) for row in resultset]
                return result_list
        finally:
            conn.close()


    def find(db="", sql="", parameters=()):
        """
        执行 SELECT 查询，返回单行结果（支持参数化查询）
        
        :param db: 数据库名（如 "sangao"），对应 db/{db_name}.db
        :param sql: SQL 查询语句，使用 ? 作为占位符
        :param parameters: 参数元组，默认为空元组
        :return: 字典表示的一行记录，如果没有结果则返回None
        """
        try:
            db_path = os.path.join(BASE_DIR, "db", db + ".db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            if parameters:
                cursor.execute(sql, parameters)  # 使用参数化查询
            else:
                cursor.execute(sql)  # 兼容旧用法
                
            resultset = cursor.fetchall()
            
            # 健壮性处理：空结果集直接返回None
            if len(resultset) == 0:
                return None  # 明确返回None而非空字典[1,9](@ref)
            
            col_name_list = [tuple[0] for tuple in cursor.description]
            return dict(zip(col_name_list, resultset[0]))
        
        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            return None  # 异常时返回None[2](@ref)
        
        finally:
            conn.close()  # 确保连接关闭[8](@ref)
    
    # def execute(db="",sql=""):
    #     conn=sqlite3.connect(os.path.join(BASE_DIR,"db",db+".db"))
    #     cursor=conn.cursor()
    #     result=cursor.execute(sql)
    #     conn.commit()
    #     return result