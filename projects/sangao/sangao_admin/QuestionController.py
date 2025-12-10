#sangao_admin/QuestionController.py


import tornado
import sqlite3
import requests
import warnings
import os
import uuid

warnings.filterwarnings('ignore')
import time
import myportal.common as common
from sangao_admin.KnowledgeModel import Knowledge
from sangao_admin.QuestionModel import SingleChoiceModel
from config import UPLOAD_PATHS
from sangao_admin.QuestionModel import KnowledgeModel
from config import UPLOAD_BASE_DIR,STATIC_PATHS
import logging
logger = logging.getLogger(__name__)



class listsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from single_choice_question"
        single_choice_questions=common.select("sangao",sql)
        sql="select * from tf_question"
        true_false_questions=common.select("sangao",sql)
        sql="select * from operation_question"
        operation_questions=common.select("sangao",sql)         
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","lists.html")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,single_choice_questions=single_choice_questions)

class sourceListsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from question_source"
        sources=common.select("sangao",sql)
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","source_lists.html"),sources=sources)



class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","add.html"))

        
class editHandler(tornado.web.RequestHandler):
    def get(self):
        db_name = ""
        question_type = self.get_argument("question_type")
        #获取知识点分类
        sql="select * from knowledge"
        knowledges=common.select("sangao",sql)

        if question_type == 'single_choice':
            db_name = "single_choice_question"
            sql = "select question.id as question_id,source.id as source_id,source.publicer as publicer,source.public_year as public_year,question.difficult as difficult,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge join question_source as source on source.id=question.source  where question.id ="+self.get_argument("question_id")            
            #sql="select id as question_id,module as module_id,title,choice1,choice2,choice3,choice4,picture,answer,source as source_id,difficult,knowledge as knowledge_id from single_choice_question where id ="+ self.get_argument("question_id") 
            logger.info(f"sql:{sql}")
            question = common.find("sangao",sql)
            if question["question_id"]:
                logger.info(f"question:{question}")
                modules=common.select("sangao","select * from module")
                knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))   
                sources=common.select("sangao","select * from question_source")         
                sql="select * from module where id="+str(question["module_id"])
                module=common.find("sangao",sql)
                question["module_name"]=module["name"]
                sql="select * from knowledge where id = "+str(question["knowledge_id"])
                knowledge=common.find("sangao",sql)
                question["knowledge_name"]=knowledge["name"]
                sql="select * from question_source where id="+str(question["source_id"])
                logger.info(f"source_sql:{sql}")
                source=common.find("sangao",sql)
                question["public_year"] = source["public_year"]
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","single_choice_edit.html"),question=question,modules=modules,knowledges=knowledges,sources=sources)
            else:
                self.write("题目不存在！")            
        if question_type == 'true_false':
            db_name = 'tf_question'
            sql = "select tf.id as question_id,tf.title as title,tf.answer as answer,tf.knowledge as knowledge,module.name as module_name,tf.module as module_id,tf.difficult as difficult,tf.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as tf join module on module.id = tf.module join knowledge on knowledge.id= tf.knowledge  where tf.id ="+self.get_argument("question_id")
            # print("sql:",sql)
            question = common.find("sangao",sql)
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","true_false_edit.html"),question=question,modules=modules,knowledges=knowledges)                  
        if question_type == 'operation':
            db_name = 'operation_question'
            sql = "select question.id as question_id,question.material as material,question.difficult as difficult,question.picture as picture,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            question = common.find("sangao",sql)            
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))                 
            # print("sql:",sql)
            question = common.find("sangao",sql)
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","operation_edit.html"),question=question,modules=modules,knowledges=knowledges)                  
        
        if question_type == 'multiple_choice':
            db_name = "multiple_choice_question"
            sql = "select question.id as question_id,question.difficult as difficult,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.choice5 as choice5,question.choice6 as choice6,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            question = common.find("sangao",sql)            
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))            
            # print("sql:",sql)

            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","multiple_choice_edit.html"),question=question,modules=modules,knowledges=knowledges)   

        if question_type == 'fill_blank':
            db_name = 'fill_blank_question'
            sql = "select question.id as question_id,question.difficult as difficult,question.picture as picture,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            # print("sql:",sql)
            question = common.find("sangao",sql)
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))               
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","fill_blank_edit.html"),question=question,modules=modules,knowledges=knowledges)   
        
    def post(self):
        print("进入post")
        
        if self.get_argument("question_type")=='single_choice':
            data={}
            data["title"]=self.get_argument("title")
            data["choice1"]=self.get_argument("choice1")
            data["choice2"]=self.get_argument("choice2")
            data["choice3"]=self.get_argument("choice3")
            data["choice4"]=self.get_argument("choice4")
            data["knowledge"]=self.get_argument("knowledge")
            data["module"]=self.get_argument("module")
            data["answer"]=self.get_argument("correct_answer")
            data["difficult"]=self.get_argument("difficult")            
            sql="update single_choice_question set title='"+data["title"]+"',choice1='"+data["choice1"]+"',choice2='"+data["choice2"]+"',choice3='"+data["choice3"]+"',choice4='"+data["choice4"]+"',module='"+data["module"]+"',answer='"+data["answer"]+"',difficult='"+data["difficult"]+"',knowledge='"+data["knowledge"]+"'"
            UPLOAD_FILE_PATH = STATIC_PATHS["single_choice_question_images"]
            if self.request.files.get('photo1', None):
                uploadFile = self.request.files['photo1'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
                fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename),'wb')
                fileObj.write(uploadFile['body'])
                data["photo1"]=filename
                sql+=",picture='"+data["photo1"]+"'"
           
            sql=sql+" where id="+self.get_argument("question_id")

            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");window.location.href="select";</script></body></html>')  
        if self.get_argument("question_type")=="true_false":
            data={}
            data["title"]=self.get_argument("title")
            data["answer"]=self.get_argument("answer")
            data["module"]=self.get_argument("module")
            data["knowledge"]=self.get_argument("knowledge")
            data["difficult"]=self.get_argument("difficult")
            sql="update tf_question set title='"+data["title"]+"',module='"+data["module"]+"',answer='"+data["answer"]+"',difficult='"+data["difficult"]+"',knowledge='"+data["knowledge"]+"'"
            UPLOAD_FILE_PATH = STATIC_PATHS[self.get_argument("question_type")]
            if self.request.files.get('photo1', None):
                uploadFile = self.request.files['photo1'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
                fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
                fileObj.write(uploadFile['body'])
                data["photo1"]=filename           
                sql+=" picture='"+data["photo1"]+"'"
           
            sql=sql+" where id="+self.get_argument("question_id")
            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");window.location.href="select";</script></body></html>')  

        if self.get_argument("question_type")=="multiple_choice":
            print("进入multiple_choice")
            data={}
            data["title"]=self.get_argument("title")
            data["answer"]=self.get_argument("answer")
            data["module"]=self.get_argument("module")
            data["knowledge"]=self.get_argument("knowledge")
            data["choice1"]=self.get_argument("choice1")
            data["choice2"]=self.get_argument("choice2")
            data["choice3"]=self.get_argument("choice3")
            data["choice4"]=self.get_argument("choice4")
            data["choice5"]=self.get_argument("choice5")
            data["choice6"]=self.get_argument("choice6")
            data["difficult"]=self.get_argument("difficult")
            sql="update multiple_choice_question set title='"+data["title"]+"',answer='"+data["answer"]+"',module="+data["module"]+",knowledge="+data["knowledge"]

            UPLOAD_FILE_PATH = STATIC_PATHS[self.get_argument("question_type")]
            if self.request.files.get('photo1', None):
                uploadFile = self.request.files['photo1'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
                fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
                fileObj.write(uploadFile['body'])
                data["photo1"]=filename
                sql+=" picture='"+data["photo1"]+"'"
           
            sql=sql+" where id="+self.get_argument("question_id")
            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");window.location.href="select";</script></body></html>')  

        if self.get_argument("question_type")=="fill_blank":
            print("进入fill_blank")
            data={}
            data["title"]=self.get_argument("title")
            data["answer"]=self.get_argument("answer")
            data["module"]=self.get_argument("module")
            data["knowledge"]=self.get_argument("knowledge")
            data["difficult"]=self.get_argument("difficult")
            sql="update fill_blank_question set title='"+data["title"]+"',answer='"+data["answer"]+"',module="+data["module"]+",knowledge="+data["knowledge"]

            UPLOAD_FILE_PATH = STATIC_PATHS["fill_blank"]
            if self.request.files.get('photo1', None):
                uploadFile = self.request.files['photo1'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
                fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
                fileObj.write(uploadFile['body'])
                data["photo1"]=filename
                sql+=" picture='"+data["photo1"]+"'"
        
            sql=sql+" where id="+self.get_argument("question_id")
            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");window.location.href="select";</script></body></html>')  

        if self.get_argument("question_type")=="operation":
            print("进入operation")
            data={}
            data["title"]=self.get_argument("title")
            data["module"]=self.get_argument("module")
            data["knowledge"]=self.get_argument("knowledge")
            data["difficult"]=self.get_argument("difficult")
            sql="update operation_question set title='"+data["title"]+"',module="+data["module"]+",knowledge="+data["knowledge"]

            UPLOAD_FILE_PATH = STATIC_PATHS["operation_files"]
            UPLOAD_IMAGE_PATH = STATIC_PATHS["operation_images"]
            if self.request.files.get('photo1', None):
                uploadFile = self.request.files['photo1'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
                fileObj = open(os.path.join(UPLOAD_IMAGE_PATH,filename), 'wb')
                fileObj.write(uploadFile['body'])
                data["photo1"]=filename
                sql+=", picture='"+data["photo1"]+"'"

            if self.request.files.get('material', None):
                uploadFile = self.request.files['material'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['material'][0]['filename'])[1]
                fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename), 'wb')
                fileObj.write(uploadFile['body'])
                data["material"]=filename
                sql+=", material='"+data["material"]+"'"        

            if self.request.files.get('material2', None):
                uploadFile = self.request.files['material2'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['material2'][0]['filename'])[1]
                fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename), 'wb')
                fileObj.write(uploadFile['body'])
                data["material2"]=filename
                sql+=", material2='"+data["material2"]+"'"        

            if self.request.files.get('correct_answer', None):
                uploadFile = self.request.files['correct_answer'][0]
                # 生成新的文件名
                filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['correct_answer'][0]['filename'])[1]
                fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename), 'wb')
                fileObj.write(uploadFile['body'])
                data["answer"]=filename
                sql+=", answer='"+data["answer"]+"'"         


            sql=sql+" where id="+self.get_argument("question_id")
            logger.info("sql: %s",sql)
            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");window.location.href="select";</script></body></html>')  

class joinExamHandler(tornado.web.RequestHandler):
    def get(self):
        # common.tongji("exam_paper_del")
        data={}
        data["belong_exam_paper_id"]
        sql="insert into exam_plan(belong_exam_paper_id,question_type,question_id) values()"


class examPaperDelHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        common.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()

class delHandler(tornado.web.RequestHandler):
    def get(self):
        db_name = ""
        question_type = self.get_argument("question_type")
        #获取知识点分类
        sql="select * from knowledge"
        knowledges=common.select("sangao",sql)

        if question_type == 'single_choice':
            db_name = "single_choice_question"
            sql = "select question.id as question_id,source.id as source_id,source.publicer as publicer,source.public_year as public_year,question.difficult as difficult,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge join question_source as source on source.id=question.source  where question.id ="+self.get_argument("question_id")            

            question = common.find("sangao",sql)
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))   
            sources=common.select("sangao","select * from question_source")         
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","single_choice_edit.html"),question=question,modules=modules,knowledges=knowledges,sources=sources)
            else:
                self.write("题目不存在！")            
        if question_type == 'true_false':
            table_name = 'tf_question'
            sql = "delete from "+table_name+" where id="+self.get_argument("question_id")
            reslut = common.execute("sangao",sql)
            if reslut:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>')
        if question_type == 'operation':
            db_name = 'operation_question'
            sql = "select question.id as question_id,question.material as material,question.difficult as difficult,question.picture as picture,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            question = common.find("sangao",sql)            
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))                 
            # print("sql:",sql)
            question = common.find("sangao",sql)
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","operation_edit.html"),question=question,modules=modules,knowledges=knowledges)                  
        
        if question_type == 'multiple_choice':
            db_name = "multiple_choice_question"
            sql = "select question.id as question_id,question.difficult as difficult,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.choice5 as choice5,question.choice6 as choice6,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            question = common.find("sangao",sql)            
            modules=common.select("sangao","select * from module")
            knowledges=common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))            
            # print("sql:",sql)

            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","multiple_choice_edit.html"),question=question,modules=modules,knowledges=knowledges)   

        if question_type == 'fill_blank':
            table_name = 'fill_blank_question'
            sql = "delete from "+table_name+" where id="+self.get_argument("question_id")
            reslut = common.execute("sangao",sql)
            if reslut:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>')

class handinHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入交卷模块")
        common.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","index.html"))
    def post(self):
        pass

class errorQuestionHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    #由于直接从数据库中取出错题信息（包括谁错的，哪道题，错误答案是啥，同错的有多少人，错误率多少（同错的人数除以做过的人数））比较复杂，可以分为两步来做。先将错题都取出来，再统计。由于处理麻烦，暂时不将操作题加入到错题中
    def get(self):
        #将错题取出保存为列表,错误信息（同错的人数，做过的人数等）单独保存为字典single_choice_error_stats和tf_error_stats

        error_question = []
        single_choice_error_stats = {}
        tf_error_stats = {}
        sql = "select * from student_answer"
        student_answers=common.select("sangao",sql)
        for vo in student_answers:
            if vo["question_type"]=="single_choice":
                #做过的加1
                single_choice_error_stats.setdefault(vo["question_id"],{"answer_sum":0,"error_sum":0,"question_type":"单选","question_title":""})
                single_choice_error_stats[vo["question_id"]]["answer_sum"]+=1

                sql = "select student_answer.question_id as question_id ,student_answer.question_type as question_type, student_answer.answer as student_answer,question.answer as question_answer,student_answer.student_id,question.title as question_title from student_answer join single_choice_question as question on question.id = student_answer.question_id where question.id= "+str(vo["question_id"])
                student_answer = common.select("sangao",sql)
                #将试题内容和类型保存在错题统计字典中
                if not single_choice_error_stats[vo["question_id"]]["question_title"]:
                    single_choice_error_stats[vo["question_id"]]["question_title"]=student_answer[0]["question_title"]
                # print("同一题的记录：",student_answer)
                if vo["answer"] != student_answer[0]["question_answer"]:
                    error_question.append(vo)
                    # #做错此题的人数加1
                    single_choice_error_stats[vo["question_id"]]["error_sum"]+=1
                    # print("single_choice:",single_choice_error_stats[vo["question_id"]])
            if vo["question_type"] == "true_false":
                #同样的，做过的+1
                tf_error_stats.setdefault(vo["question_id"],{"answer_sum":0,"error_sum":0,"question_type":"判断","question_title":""})
                tf_error_stats[vo["question_id"]]["answer_sum"]+=1
                sql = "select student_answer.question_id as question_id ,student_answer.question_type as question_type, student_answer.answer as student_answer,question.answer as question_answer,student_answer.student_id,question.title as question_title from student_answer join tf_question as question on question.id = student_answer.question_id where question.id= "+str(vo["question_id"]) 
                student_answer = common.select("sangao",sql)
                #将试题内容和类型保存在错题统计字典中
                if not tf_error_stats[vo["question_id"]]["question_title"]:
                    tf_error_stats[vo["question_id"]]["question_title"]=student_answer[0]["question_title"]
                #print("同一题的记录：",student_answer)                
                if vo["answer"] != student_answer[0]["question_answer"]:
                    error_question.append(vo)  
                    #错过的+1
                    # ++true_false_error_sum[student_answer["question_id"]]
                    tf_error_stats[vo["question_id"]]["error_sum"]+=1

        #最后将错题的统计信息单独保存为一个字典
        #对列表进行去重
        # new_error_question = list(set(error_question))
        # for vi in new_error_question:
        #     if vi["question_type"] == "single_choice":
        #         vi["answer_sum"] = single_choice_answer_sum[vi["question_id"]]
        #         vi["error_sum"] = single_choice_error_sum[vi["question_id"]]
        #     if vi["question_type"] == "true_false":
        #         vi["answer_sum"] = true_false_answer_sum[vi["question_id"]]
        #         vi["error_sum"] = true_false_error_sum[vi["question_id"]]
        # print("单选列表：",single_choice_error_stats)
        # print("single_choice_error_stats:",single_choice_error_stats[3])
        # print("判断列表：",tf_error_stats)
        #两个统计字典合并
        merged_stats={}
        merged_stats.update({f"single_choice:{k}":v for k,v in single_choice_error_stats.items()})
        merged_stats.update({f"tf:{k}": v for k,v in tf_error_stats.items()})
        # print("合并后的字典：",merged_stats)
        #排序
        sorted_stats = sorted(merged_stats.items(),key= lambda x:(x[1]["answer_sum"],x[1]["error_sum"]/x[1]["answer_sum"]),reverse=True)
        # print("排序后的列表",sorted_stats)

        self.render("sangao_admin/templates/Question/error_ranking_list.html",error_ranking= sorted_stats)


class sourceAddHandler(tornado.web.RequestHandler):
    def post(self):
        data={}
        data["source"]=self.get_argument("source")
        data["public_time"]=self.get_argument("public_time")


        sql="insert into question_source(public_year,publicer) values('"+data["public_time"]+"','"+data["source"]+"')"
        result= common.execute("sangao",sql)
        if result:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");</script></body></html>')


    def get(self):
        
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","source_add.html"))



class singleChoiceAddHandler(tornado.web.RequestHandler):
    def post(self):
        #sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        data={}
        data["title"]=self.get_argument("title")
        data["choice1"]=self.get_argument("choice1")
        data["choice2"]=self.get_argument("choice2")
        data["choice3"]=self.get_argument("choice3")
        data["choice4"]=self.get_argument("choice4")
        if self.request.files.get('photo1', None):
            uploadFile = self.request.files['photo1'][0]
            # 生成新的文件名
            filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
            fileObj = open(os.path.join(UPLOAD_PATHS["single_choice"] , filename), 'wb')
            fileObj.write(uploadFile['body'])
            data["photo1"]=filename
        else:
            data["photo1"]=""
        data["module"]=self.get_argument("module")
        data["answer"]=self.get_argument("correct_answer")
        data["knowledge"]=self.get_argument("knowledge")
        data["source"]=self.get_argument("source")
        data["exam_year"]=self.get_argument("exam_year")
        data["difficult"]=self.get_argument("difficult")
        if SingleChoiceModel.add(data["title"],data["choice1"],data["choice2"],data["choice3"],data["choice4"],data["answer"],data["source"],data["exam_year"],data["difficult"],data["photo1"],data["module"],data["knowledge"]):
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");</script></body></html>')
        
    def get(self):
        Knowledges=Knowledge.select()
        modules=common.select("sangao","select * from module")
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","single_choice_add.html"),knowledges=Knowledges,modules=modules)


class multipleChoiceAddHandler(tornado.web.RequestHandler):
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["choice1"]=self.get_argument("choice1")
        data["choice2"]=self.get_argument("choice2")
        data["choice3"]=self.get_argument("choice3")
        data["choice4"]=self.get_argument("choice4")
        data["choice5"]=self.get_argument("choice5")
        data["choice6"]=self.get_argument("choice6")
        UPLOAD_FILE_PATH = 'sangao\\templates\\Question\\upload\\'
        if self.request.files.get('photo1', None):
            uploadFile = self.request.files['photo1'][0]
            # 生成新的文件名
            filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["photo1"]=filename
        else:
            data["photo1"]=""
        data["module"]=self.get_argument("module")
        data["answer"]=','.join(self.get_arguments("answer"))
        print(data["answer"])
        sql="insert into multiple_choice_question(title,choice1,choice2,choice3,choice4,choice5,choice6,picture,module,answer) values('"+data["title"]+"','"+data["choice1"]+"','"+data["choice2"]+"','"+data["choice3"]+"','"+data["choice4"]+"','"+data["choice5"]+"','"+data["choice6"]+"','"+data["photo1"]+"','"+data["module"]+"','"+data["answer"]+"')"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        Knowledges=Knowledge.select()
        modules=common.select("sangao","select * from module")
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","multiple_choice_add.html"),knowledges=Knowledges,modules=modules)


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        konwledges=KnowledgeModel.select()
        modules = common.select("sangao","select * from module")        
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","select.html"),knowledges=konwledges,modules=modules)

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
            single_choice_questions=common.select("sangao",sql)
        if self.get_argument("type")=="true_false":
            sql="select * from tf_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"  
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                                   
            true_false_questions=common.select("sangao",sql)
        if self.get_argument("type")=="operation":
            print("进入操作题")
            sql="select * from operation_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"             
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                                            
            operation_questions=common.select("sangao",sql) 
            print(f"operation:{operation_questions}")
        if self.get_argument("type")=="multiple_choice":
            sql="select * from multiple_choice_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"             
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                 
            multiple_choice_questions=common.select("sangao",sql)     
        if self.get_argument("type")=="fill_blank":
            print("进入填空题")
            sql="select * from fill_blank_question where difficult='"+data["difficult"]+"' and title like '%"+data["keyword"]+"%' "
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"             
            if data["module"]!="所有":
                sql=sql+" and module='"+data["module"]+"'"                 
            fill_blank_questions=common.select("sangao",sql)  
        # print("结果集multiple_choice_questions",multiple_choice_questions)                                  
        # print("结果集single_choice_questions",single_choice_questions)       
        # print("结果集true_false_questions",true_false_questions)
        # print("结果集operation_questions",operation_questions)
        # print("结果集fill_blank_questions",fill_blank_questions)
        
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","result.html")
        ,module=data["module"]
        ,question_type=self.get_argument("type")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,multiple_choice_questions=multiple_choice_questions        
        ,fill_blank_questions=fill_blank_questions 
        ,single_choice_questions=single_choice_questions)

class fillBlankAddHandler(tornado.web.RequestHandler):
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        UPLOAD_FILE_PATH = 'sangao\\templates\\Question\\upload\\'
        if self.request.files.get('photo1', None):
            uploadFile = self.request.files['photo1'][0]
            # 生成新的文件名
            filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['photo1'][0]['filename'])[1]
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["photo1"]=filename
        else:
            data["photo1"]=""
        data["module"]=self.get_argument("module")
        data["answer"]=self.get_argument("answer")
        print(data["answer"])
        sql="insert into fill_blank_question(title,picture,module,answer) values('"+data["title"]+"','"+data["photo1"]+"','"+data["module"]+"','"+data["answer"]+"')"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("sangao_admin/templates/Question/fill_blank_add.html",exam_papers=exam_papers)      
        
class trueFalseAddHandler(tornado.web.RequestHandler):
    def post(self):
        #sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        data={}
        data["title"]=self.get_argument("title")
        data["answer"]=self.get_argument("answer")
        data["picture"]=self.get_argument("picture","")
        data["module"]=self.get_argument("module")
        sql="insert into tf_question(title,answer,picture,module) values('"+data["title"]+"','"+data["answer"]+"','"+data["picture"]+"','"+data["module"]+"')"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","true_false_add.html"),exam_papers=exam_papers)

class operationAddHandler(tornado.web.RequestHandler):
    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        print("post_data:",post_data)

        data = {}        
        # 素材文件的处理
        UPLOAD_FILE_PATH = 'sangao\\templates\\Question\\upload\\'
        # username = self.get_argument('username', 'anonymous')
        if self.request.files.get('material', None):
            uploadFile = self.request.files['material'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["material"] =  filename

        # 标准答案文件的处理
        UPLOAD_FILE_PATH = 'sangao\\templates\\Question\\answer\\'
        if self.request.files.get('correct_answer', None):
            uploadFile = self.request.files['correct_answer'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["correct_answer"] =  filename            
        self.write("上传成功")             
        
        if self.request.files.get('photo1', None):
            uploadFile = self.request.files['photo1'][0]
            photo_url = uploadFile['filename']
            print(photo_url)
            fileObj = open(UPLOAD_FILE_PATH + photo_url, 'wb')
            fileObj.write(uploadFile['body'])
        else:
            photo_url=""

       
        data["title"]=self.get_argument("title")
        data["picture"]=photo_url
        data["module"]=self.get_argument("module")

        sql="insert into operation_question(title,material,answer,picture,module) values('"+data["title"]+"','"+data["material"]+"','"+data["correct_answer"]+"','"+data["picture"]+"','"+data["module"]+"')"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("sangao_admin/templates/Question/operation_add.html",exam_papers=exam_papers)        

