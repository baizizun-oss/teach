import tornado
import sqlite3
import urllib
import requests
import warnings
warnings.filterwarnings('ignore')
import time



class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'task_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        sql="select * from note where status='未处理'"
        conn=sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        tasks=conn.cursor().execute(sql)
        result=conn.commit()
        self.render("sangao\\templates\\Note\\result.html"
        		,tasks=tasks)
        self.render("sangao\\templates\\Note\\result.html")


class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        self.render("sangao\\templates\\Note\\add.html")
    def post(self):
        data = {}
        data["start_display_time"] = str(int(time.time()))
        data["title"] = self.get_argument("title") + self.get_argument("priority")
        data["content"] = self.get_argument("content").replace(" ", "&nbsp").replace("\n", "<br>").replace("'", "&apos")
        data["address"] = ",".join(self.get_arguments("address[]"))
        data["status"] = "未处理"
        data["ctime"] = str(int(time.time()))
        data["remainder_time"] = str(int(time.time()))
        data["type"] = ",".join(self.get_arguments("type[]"))

        sql = "insert into note(title,content,address,\
        	status,start_display_time,ctime,remainder_time,type) values('" + data["title"] + "' \
        	,'" + data["content"] + "','" + data["address"] + "' \
        	,'" + data["status"] + "'," + data["start_display_time"] + " \
        	," + data["ctime"] + " \
        	," + data["remainder_time"] + " \
        	,'" + data["type"] + "' \
        	)"
        # print("sql语句:"+sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        # print("result:",result)
        conn.commit()
        conn.close()
        # print("result结果为:",result)

class doubleAddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("sangao\\templates\\Note\\add.html")
        
    def post(self):
        #print("进入task_index_doubleadd_post方法了")
        
        data={}
        data["start_display_time"] = str(int(time.time()))
        data["title"] = self.get_argument("title")+self.get_argument("priority")
        data["content"] = self.get_argument("content").replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")
        data["address"]=",".join(self.get_arguments("address[]"))
        data["status"] ="未处理"
        data["ctime"]  = str(int(time.time()))
        data["remainder_time"] = str(int(time.time()))
        data["type"]   = ",".join(self.get_arguments("type[]"))

        sql="insert into task(title,content,address,\
        	status,start_display_time,ctime,remainder_time,type) values('"+data["title"]+"' \
        	,'"+data["content"]+"','"+data["address"]+"' \
        	,'"+data["status"]+"',"+data["start_display_time"]+" \
        	,"+data["ctime"]+" \
        	,"+data["remainder_time"]+" \
        	,'"+data["type"]+"' \
        	)"
        #print("sql语句:"+sql)
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        result=conn.cursor().execute(sql)
        #print("result:",result)
        
        ##remote
        url1   ="http://192.168.43.1:8000/task/Home/Index/add"
        res=requests.post(url1,data=data)
        #print("http响应为:",res.content)
        self.write(res.content)
        conn.commit()
        conn.close()
        #print("result结果为:",result)
        


class editHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_edit_get方法了")
        
    def post(self):
        #print("进入task_edit_post方法了")

        data={}
        data["start_display_time"] = self.get_argument("start_display_time")
        #data["start_display_time"] = str(int(time.mktime(time.strptime(self.get_argument("start_display_time"),"%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"]=self.get_argument("challenge")
        data["impede"]=self.get_argument("impede")
        data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")

        sql = "update task set title='"+data["title"]+"'"
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        sql=sql+",impede='"+self.get_argument("impede")+"' "
        sql=sql+",address='"+",".join(self.get_arguments("address"))+"'"
        #print("地点post数据",self.get_arguments("address"))
        sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        #print("sql语句:"+sql)
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        #print("result结果为:",result)     
        self.write("")  
        
        #task的编辑模块
class doubleEditHandler(tornado.web.RequestHandler):
    def get(self):
        #print("进入task_doubleedit_get方法了")
        tasks=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from task where id="+self.get_argument("id"))
        for vo in tasks:
            task=vo
            
        #print("tasks字符集：",tasks)
        #print("task字符集:",task)
        impedes=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from impede where status = 'abled'")
        challenges=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        #print("challenges:",dir(challenges))
      
        
        self.render("sangao\\templates\\Note\\edit.html"
         
         ,task=task
         ,id=task[0]
         ,title=task[3]
         ,content=task[4].replace("&nbsp"," ").replace("<br>","\n")
        	,status=task[5]
        	,address=task[6]
        	,challenge=task[11]
        	,photo1=task[10]
        	,photo2=task[11]
        	,photo3=task[12]
        	,type=task[7]
        	,impede=task[15]
        	
        	,impedes=impedes
        	,challenges=challenges
        	
        	)
        	
        	#在这对python和php对于模拟客户端发起http请求的处理方法的不同做一个说明
        	#php主要用作后端，一般不需要发起http请求，而是接收http请求。因此原生需要没有关于模拟浏览器发起http请求的功能是可以理解的。因此也就用到了curl这样的第三方类库
        	#而python是系统语言(或者用现在的说法是全栈语言)，可以需要对浏览器客户端进行开发，因此原生语言内置了模拟浏览器发起http请求的功能。就是client类。
        	#而它的使用和curl一样都是模拟了一个客户端类，用它的方法发起请求
    #@tornado.web.asynchronous
    def post(self):
        #print("post['address']:",self.get_arguments("address"))
        ##print("post数据:",self.get_argument())
       # url1   ="http://1.198.50.136:9000/task/index.php/Home/Index/edit/id/"+self.get_argument("id")
        url1   ="http://192.168.43.1:8000/task/Home/Index/edit?id="+self.get_argument("id")
        url123 ="http://127.0.0.1:8000/task/edit?id="+self.get_argument("id")
        url_test="http://192.168.43.1:8080/task/index.php?m=Home&c=index&a=doubleedit&id="+self.get_argument("id")
        
        #data={"id":self.get_arguments("id")}
        if self.get_argument("start_display_time_first_half") == time.strftime("%d"):
            start_display_time_day=self.get_argument("start_display_time_second_half")
        else:
            start_display_time_day=self.get_argument("start_display_time_first_half")
        if self.get_argument("start_display_time_morning")==time.strftime("%H"):
            start_display_time_hour=self.get_argument("start_display_time_afternoon")
        else:
            	start_display_time_hour=self.get_argument("start_display_time_morning")
        start_display_time = self.get_argument("start_display_time_year")+","+self.get_argument("start_display_time_month")+","+start_display_time_day+","+start_display_time_hour
        
        
        #data={'id':self.get_argument("id")}
        data={}
        data["start_display_time"] = str(int(time.mktime(time.strptime(start_display_time,"%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"]=self.get_argument("challenge")
        data["impede"]=self.get_argument("impede")
        data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")


        sql = "update task set title='"+data["title"]+"'"
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        sql=sql+",impede='"+self.get_argument("impede")+"' "
        sql=sql+",address='"+data["address"]+"'"
        #print("地点post数据",self.get_arguments("address"))
        sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        #print("sql语句:"+sql)
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        #print("result结果为:",result)
        
        res=requests.post(url1,data=data)
        ###print("http响应为:",res.content)
        self.write(res.content)
        
        
class selectHandler(tornado.web.RequestHandler):
    def get(self):
        #print("进入task_select_get方法了")

        impedes=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from impede where status = 'abled'")
        challenges=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        #print("challenges:",dir(challenges))
      
        self.render("sangao\\templates\\Note\\select.html"
        	
        	,impedes=impedes
        	,challenges=challenges
        	
        	)
        
    def post(self):
        #print("进入task_select_post方法了")
        #print("post数据:"+self.get_argument(status"))
        sql="select * from task where 1=1 "
        if self.get_argument("status","空值")!="空值":
            sql=sql+" and (status like '%"+self.get_argument("status")+"%')"
        if self.get_argument("impede","空值")!="空值":
            sql=sql+" and (impede like '%"+self.get_argument("impede")+"%')"
        if len(self.get_arguments("address[]","空值"))>0:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[0]+"%') "
        if len(self.get_arguments("address[]","空值"))>1:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[1]+"%')"
        if self.get_argument("keyword","空值")!="空值":
            sql=sql+" and (title like '%"+self.get_argument("keyword")+"%' or \
        	 content like '%"+self.get_argument("keyword")+"%' or \
        	 id like '%"+self.get_argument("keyword")+"%' \
        	)"
        if self.get_argument("keyword2","nullvalue")!="nullvalue":
            sql=sql+" and (title like '%"+self.get_argument("keyword2")+"%' or \
        		content like '%"+self.get_argument("keyword2")+"%' or \
        		id like '%"+self.get_argument("keyword2")+"%' \
        		)"
        		
        if len(self.get_arguments("type[]","nullvalue"))>0:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[0]+"%'")
        if len(self.get_arguments("type[]","nullvalue"))>1:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[1]+"%'")
        if self.get_argument("challenge","nullvalue")!="nullvalue":
            sql=sql+(" and challenge like '%"+self.get_argument("challenge")+"%'")
        sql=sql+" order by id asc"
        #print("sql is:",sql)
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        tasks=conn.cursor().execute(sql)
        result=conn.commit()
        self.render("sangao\\templates\\Note\\result.html"
        		,tasks=tasks)


class detailHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_select_get方法了")
        conn=sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        note=conn.cursor().execute("select * from note where id="+self.get_argument("id"))
        result=conn.commit
        self.render("sangao\\templates\\Note\\detail.html"
        	,note=note
        	)