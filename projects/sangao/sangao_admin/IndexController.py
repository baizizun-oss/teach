# -*-coding:utf8;-*-
# qpy:console


import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import time
import random
import http.client
import json
import sqlite3
import config
import common.CommonModel as Common


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("administrator",None) !="admin":
            self.redirect("sangao_admin/login")
        else:
            self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","index.html"))

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Index","login.html"))
    def post(self):
        if self.get_argument("username") == "bgp1984" and self.get_argument("password") == "founder#021665":
            self.set_cookie("administrator", "admin")
            self.redirect("index")
        else:
            self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Index","login.html"))


class clickStatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        sql = "select click.id as id,click.click_time,click.click_action,user.name as name from click,user where click.user_id=user.id"
        clicks=Common.select("sangao",sql)
        self.render("sangao_admin/templates/click_statistics.html",clicks=clicks)



class quickSelectHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'quick_select')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        # self.render("myportal/templates/Index/quick_select.html")
        print("进入myportal_index_quickselect_get方法了")
        # tasks=sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db")).cursor().execute("select * from task where id="+self.get_argument("id"))
        # for vo in tasks:
        # task=vo

        # print("tasks字符集：",tasks)
        # print("task字符集:",task)
        impedes = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db")).cursor().execute(
            "select * from impede where status = 'abled'")
        # for vo in impedes:
        # print("impedes[0]:",vo[0])
        challenges = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db")).cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        # for vi in challenges:
        # print("challenges[0]:",vi[0])
        self.render("myportal/templates/Index/quick_select.html"
                    , impedes=impedes
                    , challenges=challenges
                    )

    def post(self):
        print("进入myportal_index_quick_select_post")
        '''
     		//用三个and并列质疑name中含有三个关键词的记录
    		//每个关键词的查询范围为标题和内容
        '''
        sql = "select * from task where 1=1 "

        if self.get_argument("status", "空值") != "空值":
            sql = sql + " and (status like '%" + self.get_argument("status") + "%')"
        if self.get_argument("impede", "空值") != "空值":
            sql = sql + " and (impede like '%" + self.get_argument("impede") + "%')"
        if len(self.get_arguments("address[]", "空值")) > 0:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[0] + "%') "
        if len(self.get_arguments("address[]", "空值")) > 1:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[1] + "%')"
        if self.get_argument("keyword1", "空值") != "空值":
            sql = sql + " and (title like '%" + self.get_argument("keyword1") + "%' or \
        	 content like '%" + self.get_argument("keyword1") + "%' or \
        	 id like '%" + self.get_argument("keyword1") + "%' \
        	)"
        if self.get_argument("keyword2", "nullvalue") != "nullvalue":
            sql = sql + " and (title like '%" + self.get_argument("keyword2") + "%' or \
        		content like '%" + self.get_argument("keyword2") + "%' or \
        		id like '%" + self.get_argument("keyword2") + "%' \
        		)"
        if self.get_argument("keyword3", "nullvalue") != "nullvalue":
            sql = sql + " and (title like '%" + self.get_argument("keyword3") + "%' or \
        		content like '%" + self.get_argument("keyword3") + "%' or \
        		id like '%" + self.get_argument("keyword3") + "%' \
        		)"
        if len(self.get_arguments("type[]", "nullvalue")) > 0:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[0] + "%'")
        if len(self.get_arguments("type[]", "nullvalue")) > 1:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[1] + "%'")
        if self.get_argument("challenge", "nullvalue") != "nullvalue":
            sql = sql + (" and challenge like '%" + self.get_argument("challenge") + "%'")
        sql_problem = sql + " order by id asc"
        sql_task = sql + " and start_display_time<" + str(int(time.time())) + " order by id asc "
        '''
        sql = "select * from task where 1=1 "
        sql = sql+" and (status like '%"+self.get_argument("status")+"%') "
        sql = sql+" and (impede like '%"+self.get_argument("status")+"%') "
        sql = sql+" and (challenge like '%"+self.get_argument("challenge")+"%') "
        sql = sql+" and (type like '%"+(self.get_arguments("type[]"))[0]+"%') "
        sql = sql+" AND (address like '%"+(self.get_arguments("address[]"))[0]+"%')"
        sql = sql+" and (title like '%"+self.get_argument("keyword1")+"%' \
        	 or content like '%"+self.get_argument("keyword1")+"%') "
        sql = sql+" and (title like '%"+self.get_argument("keyword2")+"%'\
        		 or content like '%"+self.get_argument("keyword2")+"%')"
        sql = sql+" and (title like '%"+self.get_argument("keyword3")+"%'\
        		 or content like '%"+self.get_argument("keyword3")+"%') "
        sql = sql+" and (start_display_time < "+time.time()+")"
        sql = sql+" order by status asc"
        print("sql:",sql)
        '''
        problems = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            sql + " order by id asc")
        tasks = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(sql_task)
        problem_develops = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            sql_problem)
        task_develops = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(sql_task)
        problem_develop_tests = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(sql_problem)
        task_develop_tests = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            sql_task)
        self.render("myportal/templates/Index/quick_select_result.html"
                    , problems=problems
                    , tasks=tasks
                    , problem_develops=problem_develops
                    , task_develops=task_develops
                    , problem_develop_tests=problem_develop_tests
                    , task_develop_tests=task_develop_tests
                    )
        '''
  		$task =M()->db(2,"mysql://baigaopeng:founder#021665@localhost:3306/baigaopeng_task")->query($sql);
    		$this->assign("task",$task);
    		$problem_develop=M()->db(3,"mysql://baigaopeng:founder#021665@localhost:3306/baigaopeng_problem_develop")->query($sql);
    		$this->assign("problem_develop",$problem_develop);
    		//$task_develop=M()->db(4,"mysql://baigaopeng:founder#021665@localhost:3306/baigaopeng_task_develop")->query($sql);
    		$task_develop=M()->db(4,"mysql://baigaopeng:founder#021665@localhost:3306/baigaopeng_task_develop")->query("select * from task where (status like '%".$_POST["status"]."%') and (impede like '%".$_POST["impede"]."%') and (challenge like '%".$_POST["challenge"]."%') and (type like '%".$_POST["type"]."%') AND (address like '%".$_POST['note_address'][0]."%') and (title like '%".$_POST["keyword1"]."%' or content like '%".$_POST["keyword1"]."%') and (title like '%".$_POST["keyword2"]."%' or content like '%".$_POST["keyword2"]."%') and (title like '%".$_POST["keyword3"]."%' or content like '%".$_POST["keyword3"]."%') and (start_display_time < ".\time().") order by status asc");
    		$this->assign("task_develop",$task_develop);
    		$problem_develop_test=M()->db(5,"mysql://baigaopeng:founder#021665@localhost:3306/baigaopeng_problem_develop_test")->query("select * from task where (status like '%".$_POST["status"]."%') and (impede like '%".$_POST["impede"]."%') and (challenge like '%".$_POST["challenge"]."%') and (type like '%".$_POST["type"]."%') AND (address like '%".$_POST['note_address'][0]."%') and (title like '%".$_POST["keyword1"]."%' or content like '%".$_POST["keyword1"]."%') and (title like '%".$_POST["keyword2"]."%' or content like '%".$_POST["keyword2"]."%') and (title like '%".$_POST["keyword3"]."%' or content like '%".$_POST["keyword3"]."%') and (start_display_time < ".\time().") order by status asc");
    		$this->assign("problem_develop_test",$problem_develop_test);
    		$task_develop_test=M()->db(6,"mysql://baigaopeng:founder#021665@localhost:3306/baigaopeng_task_develop_test")->query("select * from task where (status like '%".$_POST["status"]."%') and (impede like '%".$_POST["impede"]."%') and (challenge like '%".$_POST["challenge"]."%') and (type like '%".$_POST["type"]."%') AND (address like '%".$_POST['note_address'][0]."%') and (title like '%".$_POST["keyword1"]."%' or content like '%".$_POST["keyword1"]."%') and (title like '%".$_POST["keyword2"]."%' or content like '%".$_POST["keyword2"]."%') and (title like '%".$_POST["keyword3"]."%' or content like '%".$_POST["keyword3"]."%') and (start_display_time < ".\time().") order by status asc");
    		$this->assign("task_develop_test",$task_develop_test);

    		//除模版变量外，额外将三个关键词也传输到页面
    		$this->assign("keyword1",$_POST["keyword1"]);
    		$this->assign("keyword2",$_POST["keyword2"]);
    		$this->assign("keyword3",$_POST["keyword3"]);
    		$this->mydisplay("quick_select_result")       	
        	'''


class clickSelectHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'click_select')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        print("now is accessing myportal_index_click_select_get")
        self.render("myportal/templates/Index/click_select.html")

    def post(self):
        print("now is accessing myporta_index_click_select_post")
        data = {}
        # start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        # data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        # end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        # data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        # data["start_time"]=self.get_argument("start_time")
        # data["end_time"]=self.get_argument("end_time")

        # sql="insert into holiday(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        sql = "select count(*) as fangwen_num,click_action from click group by click_action"
        print("sql sentence:", sql)
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():  # 从fetchall中读取操作 print(row)
            print("result:", row)
            # self.write(row)
        conn.commit()
        conn.close()
        # self.write("添加成功！")
        # self.write(result)

    ###################
    ##
    # 一键执行运行秩序
    #
    ###################


class operationOrderHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'operation_order')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        self.render("myportal/templates/operation_order.html")

    def post(self):
        now_time = "上班期间"  # 默认为上班期间
        # sql="select * from holiday"
        # cursor=pymysql.connect(host="127.0.0.1",port=3306,user="baigaopeng",passwd='founder#021665',db="baigaopeng_myportal").cursor()
        # holidays=sqlite3.connect("")
        # result = cursor.execute(sql)
        # holidays = cursor.fetchall()
        holidays = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db")).cursor().execute(
            "select * from holiday")

        print("holidays字符集:", holidays)
        for vo in holidays:
            if (time.time() < vo[2] and time.time() > vo[1]):
                now_time = "下班期间"
        print("上班期间或者下班期间:", now_time)

        # 《问题笔记系统》中优先级为&^￥^,状态为”未处理“
        problem_10 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%'")
        task_10 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and status='未处理' and start_display_time< " + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        problem_develop_10 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_develop_10 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        problem_develop_test_10 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_develop_test_10 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")

        problem_11 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_11 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        problem_develop_11 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_develop_11 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        problem_develop_test_11 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_develop_test_11 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")

        problem_12 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_12 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        problem_develop_12 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_develop_12 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        problem_develop_test_12 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")
        task_develop_test_12 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^¥^%' ")

        problem_1 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%'")
        task_1 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and status='未处理' and start_display_time< " + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        problem_develop_1 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_develop_1 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        problem_develop_test_1 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_develop_test_1 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")

        problem_2 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_2 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        problem_develop_2 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_develop_2 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        problem_develop_test_2 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_develop_test_2 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")

        problem_3 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_3 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        problem_develop_3 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_develop_3 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        problem_develop_test_3 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")
        task_develop_test_3 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%&^%' ")

        problem_4 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%'")
        task_4 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and status='未处理' and start_display_time< " + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        problem_develop_4 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_develop_4 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        problem_develop_test_4 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_develop_test_4 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")

        problem_5 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_5 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        problem_develop_5 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_develop_5 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        problem_develop_test_5 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_develop_test_5 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")

        problem_6 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_6 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        problem_develop_6 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_develop_6 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        problem_develop_test_6 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")
        task_develop_test_6 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%¥^%' ")

        problem_7 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%'")
        task_7 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and status='未处理' and start_display_time< " + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        problem_develop_7 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_develop_7 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        problem_develop_test_7 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_develop_test_7 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='未处理' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")

        problem_8 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_8 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        problem_develop_8 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_develop_8 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        problem_develop_test_8 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_develop_test_8 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用') and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")

        problem_9 = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_9 = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        problem_develop_9 = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_develop_9 = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        problem_develop_test_9 = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(
            "select * from task where status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")
        task_develop_test_9 = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            "select * from task where title like '%" + now_time + "%' and  status='存疑' and start_display_time<" + str(
                int(time.time())) + " and address like '%" + self.get_arguments("address[]")[
                0] + "%' and title like '%%' ")

        self.render("myportal/templates/operation_order_result.html"
                    , problem_10=problem_10
                    , task_10=task_10
                    , problem_develop_10=problem_develop_10
                    , task_develop_10=task_develop_10
                    , problem_develop_test_10=problem_develop_test_10
                    , task_develop_test_10=task_develop_test_10
                    , problem_11=problem_11
                    , task_11=task_11
                    , problem_develop_11=problem_develop_11
                    , task_develop_11=task_develop_11
                    , problem_develop_test_11=problem_develop_test_11
                    , task_develop_test_11=task_develop_test_11
                    , problem_12=problem_12
                    , task_12=task_12
                    , problem_develop_12=problem_develop_12
                    , task_develop_12=task_develop_12
                    , problem_develop_test_12=problem_develop_test_12
                    , task_develop_test_12=task_develop_test_12
                    , problem_1=problem_1
                    , task_1=task_1
                    , problem_develop_1=problem_develop_1
                    , task_develop_1=task_develop_1
                    , problem_develop_test_1=problem_develop_test_1
                    , task_develop_test_1=task_develop_test_1
                    , problem_2=problem_2
                    , task_2=task_2
                    , problem_develop_2=problem_develop_2
                    , task_develop_2=task_develop_2
                    , problem_develop_test_2=problem_develop_test_2
                    , task_develop_test_2=task_develop_test_2
                    , problem_3=problem_3
                    , task_3=task_3
                    , problem_develop_3=problem_develop_3
                    , task_develop_3=task_develop_3
                    , problem_develop_test_3=problem_develop_test_3
                    , task_develop_test_3=task_develop_test_3
                    , problem_4=problem_4
                    , task_4=task_4
                    , problem_develop_4=problem_develop_4
                    , task_develop_4=task_develop_4
                    , problem_develop_test_4=problem_develop_test_4
                    , task_develop_test_4=task_develop_test_4
                    , problem_5=problem_5
                    , task_5=task_5
                    , problem_develop_5=problem_develop_5
                    , task_develop_5=task_develop_5
                    , problem_develop_test_5=problem_develop_test_5
                    , task_develop_test_5=task_develop_test_5
                    , problem_6=problem_6
                    , task_6=task_6
                    , problem_develop_6=problem_develop_6
                    , task_develop_6=task_develop_6
                    , problem_develop_test_6=problem_develop_test_6
                    , task_develop_test_6=task_develop_test_6
                    , problem_7=problem_7
                    , task_7=task_7
                    , problem_develop_7=problem_develop_7
                    , task_develop_7=task_develop_7
                    , problem_develop_test_7=problem_develop_test_7
                    , task_develop_test_7=task_develop_test_7
                    , problem_8=problem_8
                    , task_8=task_8
                    , problem_develop_8=problem_develop_8
                    , task_develop_8=task_develop_8
                    , problem_develop_test_8=problem_develop_test_8
                    , task_develop_test_8=task_develop_test_8
                    , problem_9=problem_9
                    , task_9=task_9
                    , problem_develop_9=problem_develop_9
                    , task_develop_9=task_develop_9
                    , problem_develop_test_9=problem_develop_test_9
                    , task_develop_test_9=task_develop_test_9

                    )


class allSelectHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'quick_select')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束

        impedes = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db")).cursor().execute(
            "select * from impede where status = 'abled'")
        challenges = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db")).cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        self.render("myportal/templates/Index/all_select.html"
                    , impedes=impedes
                    , challenges=challenges
                    )

    def post(self):
        print("进入myportal_index_quick_select_post")
        '''
     		//用三个and并列质疑name中含有三个关键词的记录
    		//每个关键词的查询范围为标题和内容
        '''
        sql = "select * from task where 1=1 "

        if self.get_argument("status", "空值") != "空值":
            sql = sql + " and (status like '%" + self.get_argument("status") + "%')"
        if self.get_argument("impede", "空值") != "空值":
            sql = sql + " and (impede like '%" + self.get_argument("impede") + "%')"
        if len(self.get_arguments("address[]", "空值")) > 0:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[0] + "%') "
        if len(self.get_arguments("address[]", "空值")) > 1:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[1] + "%')"
        if self.get_argument("keyword1", "空值") != "空值":
            sql = sql + " and (title like '%" + self.get_argument("keyword1") + "%' or \
        	 content like '%" + self.get_argument("keyword1") + "%' or \
        	 id like '%" + self.get_argument("keyword1") + "%' \
        	)"
        if self.get_argument("keyword2", "nullvalue") != "nullvalue":
            sql = sql + " and (title like '%" + self.get_argument("keyword2") + "%' or \
        		content like '%" + self.get_argument("keyword2") + "%' or \
        		id like '%" + self.get_argument("keyword2") + "%' \
        		)"
        if self.get_argument("keyword3", "nullvalue") != "nullvalue":
            sql = sql + " and (title like '%" + self.get_argument("keyword3") + "%' or \
        		content like '%" + self.get_argument("keyword3") + "%' or \
        		id like '%" + self.get_argument("keyword3") + "%' \
        		)"
        if len(self.get_arguments("type[]", "nullvalue")) > 0:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[0] + "%'")
        if len(self.get_arguments("type[]", "nullvalue")) > 1:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[1] + "%'")
        if self.get_argument("challenge", "nullvalue") != "nullvalue":
            sql = sql + (" and challenge like '%" + self.get_argument("challenge") + "%'")
        sql_problem = sql + " order by id asc"
        sql_task = sql + " order by id asc "

        problems = sqlite3.connect("/db/baigaopeng_problem.db").cursor().execute(
            sql + " order by id asc")
        tasks = sqlite3.connect("/db/baigaopeng_task.db").cursor().execute(sql_task)
        problem_develops = sqlite3.connect("/db/baigaopeng_problem_develop.db").cursor().execute(
            sql_problem)
        task_develops = sqlite3.connect("/db/baigaopeng_task_develop.db").cursor().execute(sql_task)
        problem_develop_tests = sqlite3.connect(
            "/db/baigaopeng_problem_develop_test.db").cursor().execute(sql_problem)
        task_develop_tests = sqlite3.connect("/db/baigaopeng_task_develop_test.db").cursor().execute(
            sql_task)
        self.render("myportal/templates/Index/all_select_result.html"
                    , problems=problems
                    , tasks=tasks
                    , problem_develops=problem_develops
                    , task_develops=task_develops
                    , problem_develop_tests=problem_develop_tests
                    , task_develop_tests=task_develop_tests
                    )

