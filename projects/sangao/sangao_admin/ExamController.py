import tornado
import sqlite3
import urllib
import requests
import warnings
import os

warnings.filterwarnings('ignore')
import time
import config
import common.CommonModel as Common

from sangao_admin.KnowledgeModel import Knowledge

class CommonHandler():
    def tongji(modulename):
        pass

class listsHandler(tornado.web.RequestHandler):
    def get(self):

        sql = "select * from exam_paper"
        exam_papers= Common.select("sangao",sql)
        print(exam_papers)
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Exam","exam_paper_lists.html"),exam_papers=exam_papers)

class examPaperAddHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        CommonHandler.tongji("exam_paper_add")
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Exam","exam_paper_add.html"))
    def post(self):
        sql="insert into exam_paper(title,author,ctime) values('"+self.get_argument("title")+"','"+self.get_argument("author")+"',"+str(int(time.time()))+")"
        if Common.execute("sangao",sql):
            self.write('<html><head><title>提示</title></head><body><script type="text/javascript">window.alert("加入成功！");window.location.href = "lists";</script></body></html>')



class selectQuestionHandler(tornado.web.RequestHandler):
    def get(self):
        konwledges=Knowledge.select()
        modules = Common.select("sangao","select * from module")        
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Exam","question_select.html"),knowledges=konwledges,modules=modules,exam_paper_id=self.get_argument("exam_paper_id"))

    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        # print("post_data:",post_data)
        data={}
        data["module"]=self.get_argument("module")
        data["difficult"]=self.get_argument("difficult")
        data["knowledge"]=self.get_argument("knowledge")
        data["keyword"]=self.get_argument("keyword")
        single_choice_questions={}
        true_false_questions={}
        operation_questions={}
        multiple_choice_questions={}
        fill_blank_questions={}
        if self.get_argument("type")=="single_choice":
            sql="select * from single_choice_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"                  
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                       
            single_choice_questions=Common.select("sangao",sql)
        if self.get_argument("type")=="true_false":
            sql="select * from tf_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"  
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                                   
            true_false_questions=Common.select("sangao",sql)
        if self.get_argument("type")=="operation":
            print("进入操作题")
            sql="select * from operation_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"             
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                                            
            operation_questions=Common.select("sangao",sql) 
            print(f"operation:{operation_questions}")
        if self.get_argument("type")=="multiple_choice":
            sql="select * from multiple_choice_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"             
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                 
            multiple_choice_questions=Common.select("sangao",sql)     
        if self.get_argument("type")=="fill_blank":
            print("进入填空题")
            sql="select * from fill_blank_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"             
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                 
            fill_blank_questions=Common.select("sangao",sql)  
        # print("结果集multiple_choice_questions",multiple_choice_questions)                                  
        # print("结果集single_choice_questions",single_choice_questions)       
        # print("结果集true_false_questions",true_false_questions)
        # print("结果集operation_questions",operation_questions)
        # print("结果集fill_blank_questions",fill_blank_questions)
        
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Exam","result.html")
        ,module=data["module"]
        ,exam_paper_id=self.get_argument("exam_paper_id")
        ,question_type=self.get_argument("type")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,multiple_choice_questions=multiple_choice_questions        
        ,fill_blank_questions=fill_blank_questions 
        ,single_choice_questions=single_choice_questions)

class joinExamPaperHandler(tornado.web.RequestHandler):
    def get(self):
        sql="insert into exam_plan(belong_exam_paper_id,question_type,question_id) values("+self.get_argument("exam_paper_id")+","+self.get_argument("question_type")+","+self.get_argument("question_id")+")"
        result=Common.execute("sangao",sql)
        if result:
            self.write('<html><head><title>提示</title></head><body><script type="text/javascript">window.alert("加入成功！");window.location.href = "lists";</script></body></html>')
            
    def post(self):
        pass


class addQuestionHandler(tornado.web.RequestHandler):
    def get(self):
        sql="insert into exam_plan(belong_exam_paper_id,question_type,question_id) values("+self.get_argument("exam_paper_id")+","+self.get_argument("question_type")+","+self.get_argument("question_id")+")"
        result=Common.execute("sangao",sql)
        if result:
            self.write('<html><head><title>提示</title></head><body><script type="text/javascript">window.alert("加入成功！");window.location.href = "lists";</script></body></html>')
            
    def post(self):
        pass

class editHandler(tornado.web.RequestHandler):
    def get(self):
        single_choice_questions={}
        true_false_questions={}
        operation_questions={}
        multiple_choice_questions={}
        fill_blank_questions={}
        single_choice_sql="select exam_plan.id,question.id as question_id,question.title,question.choice1,question.choice2,question.choice3,question.choice4,question.picture from exam_plan JOIN single_choice_question as question ON exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type =1"
        single_choice_questions = Common.select("sangao",single_choice_sql)
        print("single_choice_questions",single_choice_questions)

        multiple_choice_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.choice5 as choice5,question.choice6 as choice6 from exam_plan join multiple_choice_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 3"
        multiple_choice_questions = Common.select("sangao",multiple_choice_sql)

        true_false_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture from exam_plan join tf_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 2"
        true_false_questions = Common.select("sangao",true_false_sql)
        
        operation_sql = "select exam_plan.id as exam_plan_id,exam_plan.question_id as question_id,question.title,question.picture,question.material,question.material2 from exam_plan join operation_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 4"
        operation_questions= Common.select("sangao",operation_sql)

        fill_blank_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture from exam_plan join fill_blank_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 5"
        fill_blank_questions = Common.select("sangao",fill_blank_sql)
        print("结果集multiple_choice_questions",multiple_choice_questions)            
        if single_choice_questions[0]["question_id"]==None:
            single_choice_questions={}
        if true_false_questions[0]["question_id"]==None:
            true_false_questions={}        
        if multiple_choice_questions[0]["question_id"]==None:
            multiple_choice_questions={}              
        if operation_questions[0]["question_id"]==None:
            operation_questions={}     
        if fill_blank_questions[0]["question_id"]==None:
            fill_blank_questions={}                         
        print("结果集multiple_choice_questions",multiple_choice_questions)                                  
        print("结果集single_choice_questions",single_choice_questions)       
        print("结果集true_false_questions",true_false_questions)
        print("结果集operation_questions",operation_questions)
        print("结果集fill_blank_questions",fill_blank_questions)
        
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Exam","edit.html")
        ,exam_paper_id=self.get_argument("id")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,multiple_choice_questions=multiple_choice_questions        
        ,fill_blank_questions=fill_blank_questions 
        ,single_choice_questions=single_choice_questions)


    def post(self):
        # print("进入task_edit_post方法了")

        data = {}
        data["start_display_time"] = self.get_argument("start_display_time")
        # data["start_display_time"] = str(int(time.mktime(time.strptime(self.get_argument("start_display_time"),"%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"] = self.get_argument("challenge")
        data["impede"] = self.get_argument("impede")
        data["address"] = ",".join(self.get_arguments("address[]"))
        data["status"] = self.get_argument("status")

        sql = "update task set title='" + data["title"] + "'"
        sql = sql + ",content='" + data["content"].replace(" ", "&nbsp").replace("\n", "<br>").replace("'",
                                                                                                       "&apos") + "'"
        sql = sql + ",start_display_time=" + data["start_display_time"]
        sql = sql + ",status = '" + self.get_argument("status") + "'"
        sql = sql + ",impede='" + self.get_argument("impede") + "' "
        sql = sql + ",address='" + ",".join(self.get_arguments("address")) + "'"
        # print("地点post数据",self.get_arguments("address"))
        sql = sql + ",challenge='" + self.get_argument("challenge") + "'"
        sql = sql + " where id=" + str(data["id"])
        # print("sql语句:"+sql)
        conn = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        conn.cursor().execute(sql)
        result = conn.commit()
        conn.close()
        # print("result结果为:",result)
        self.write("")

        # task的编辑模块


class removeExamPaperHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        CommonHandler.tongji("exam_paper_remove")
        sql = "delete from exam_plan where id=" + self.get_argument("id")
        result= Common.execute("sangao",sql)
        if result:
            self.write('<html><head><title>提示</title></head><body><script type="text/javascript">window.alert("成功移除！");window.location.href = "lists";</script></body></html>')

class examPaperDelHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        CommonHandler.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()





class errorRankingHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        print(sql)
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        error_sum=[]
        sql="select * from student_answer"
        student_answers = Common.select("sangao",sql)
        for vo in student_answers:
            if vo["question_type"] == "true_false":
                sql = "select student_answer.answer as student_answer,tf_question.answer as question_answer from student_answer join tf_question on student_answer.question_id = tf_question.id where student_answer.question_id = "+vo["question_id"]
                student_answer = Common.find("sangao",sql)
                if student_answer["student_answer"] != student_answer["question_answer"]:
                   ++error_sum[vo["question_type"]+vo["question_id"]] 
            if vo["question_type"] == "single_choice":
                sql = "select student_answer.answer as student_answer,tf_question.answer as question_answer from student_answer join single_choice_question on student_answer.question_id = single_choice_question.id where student_answer.question_id = "+vo["question_id"]
                student_answer = Common.find("sangao",sql)
                if student_answer["student_answer"] != student_answer["question_answer"]:
                   ++error_sum[vo["question_type"]+vo["question_id"]]       
            if vo["question_type"] == "operation":
                ++error_sum[vo["question_type"]+vo["question_id"]]  
        self.render(os.path.join(config.BASE_DIR,"sangao","templates","Exam","error_ranking_list.html"),error_sum = error_sum)


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        # print("进入task_select_get方法了")

        impedes = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from impede where status = 'abled'")
        challenges = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        # print("challenges:",dir(challenges))

        self.render("sangao/Learn/templates/select.html"

                    , impedes=impedes
                    , challenges=challenges

                    )

    def post(self):
        # print("进入task_select_post方法了")
        # print("post数据:"+self.get_argument(status"))
        sql = "select * from task where 1=1 "
        if self.get_argument("status", "空值") != "空值":
            sql = sql + " and (status like '%" + self.get_argument("status") + "%')"
        if self.get_argument("impede", "空值") != "空值":
            sql = sql + " and (impede like '%" + self.get_argument("impede") + "%')"
        if len(self.get_arguments("address[]", "空值")) > 0:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[0] + "%') "
        if len(self.get_arguments("address[]", "空值")) > 1:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[1] + "%')"
        if self.get_argument("keyword", "空值") != "空值":
            sql = sql + " and (title like '%" + self.get_argument("keyword") + "%' or \
        	 content like '%" + self.get_argument("keyword") + "%' or \
        	 id like '%" + self.get_argument("keyword") + "%' \
        	)"
        if self.get_argument("keyword2", "nullvalue") != "nullvalue":
            sql = sql + " and (title like '%" + self.get_argument("keyword2") + "%' or \
        		content like '%" + self.get_argument("keyword2") + "%' or \
        		id like '%" + self.get_argument("keyword2") + "%' \
        		)"

        if len(self.get_arguments("type[]", "nullvalue")) > 0:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[0] + "%'")
        if len(self.get_arguments("type[]", "nullvalue")) > 1:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[1] + "%'")
        if self.get_argument("challenge", "nullvalue") != "nullvalue":
            sql = sql + (" and challenge like '%" + self.get_argument("challenge") + "%'")
        sql = sql + " order by id asc"
        # print("sql is:",sql)
        conn = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        tasks = conn.cursor().execute(sql)
        result = conn.commit()

        data = ({"id": 1, "title": "first", "content": "first_content"}
                , {"id": 2, "title": "second", "content": "second_content"}
                )

        self.render("sangao/Learn/templates/result.html"
                    , tasks=tasks)
