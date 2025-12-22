import sqlite3
import time
#import androidhelper
import os


    
BASE_DIR = os.path.join(os.path.dirname(__file__),"..")
#获取远端ip
def get_ip():
    if os.path.exists("/storage/emulated/0/vivoX9s"):
        ip   ="192.168.43.178:8000"
    if os.path.exists("/storage/emulated/0/vivoY31s"):
        ip   ="192.168.43.123:8000"
    if os.path.exists("/storage/emulated/0/huawei20"):
        ip   ="192.168.43.178:8000"
    if os.path.exists("/storage/emulated/0/oppoR9s_1d79df"):
        ip   ="192.168.43.178:8000"
    if os.path.exists("/storage/emulated/0/vivoX70pro"):
        ip  ="192.168.43.123:8000"
    if os.path.exists("/storage/emulated/0/oppoA57"):
        ip  ="192.168.43.178:8000"        
    return ip
def get_device():
    device=""
    if os.path.exists("/storage/emulated/0/vivoX9s"):
        device   ="vivoX9s"
    if os.path.exists("/storage/emulated/0/oppoR9s_3881f5"):
        device   ="oppoR9s_3881f5"
    if os.path.exists("/storage/emulated/0/honor7C"):
        device   ="honor7C"
    if os.path.exists("/storage/emulated/0/oppoA57"):
        device   ="oppoA57"                
    if os.path.exists("/storage/emulated/0/oppoR9s_1d79df"):
        device   ="oppoR9s_1d79df"         
    if os.path.exists("/storage/emulated/0/oppoR9s_bfd8c5"):
        device   ="oppoR9s_bfd8c5"         
    if os.path.exists("/storage/emulated/0/oppoR9s_ae68bb"):
        device   ="oppoR9s_ae68bb"         
    if os.path.exists("/storage/emulated/0/vivoX70pro"):
        device ="vivoX70pro"
    return device
    
def tongji(click_client_ip="",click_client_device="",module="",item_id="0",visit_spend="0"):
    pass
    #print("device:",click_client_device)
    # #统计模块开始
    # conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
    # sql="insert into tongji(click_time,click_action,visit_spend,item_id,click_client_ip,click_client_device) values("+str(int(time.time()))+",'"+module+"',"+visit_spend+","+item_id+",'"+click_client_ip+"','"+click_client_device+"')"
    # result=conn.cursor().execute(sql)
    # conn.commit()
    # conn.close()
    # #统计模块结束




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
        
    
    
    

#通过判断特定位置的文件获取当前手机名称
def getPhoneName():
    device="没有获取当前手机名称"
    if os.path.exists("/storage/emulated/0/vivoX9S"):
        device   ="vivoX9S"
    if os.path.exists("/storage/emulated/0/oppoA57"):
        device   ="oppoA57"
    return device


            
        
                
            
