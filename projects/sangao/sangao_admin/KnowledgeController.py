import tornado
import sqlite3
import urllib
import requests
import warnings
import os
import uuid

warnings.filterwarnings('ignore')
import time
import myportal.common as common




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


class addHandler(tornado.web.RequestHandler):
    def get(self):
        modules=common.select("sangao","select * from module")

        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Knowledge","add.html"),modules=modules)
    def post(self):
        sql="insert into knowledge(name,belong_module_id,difficult) values('"+self.get_argument("title")+"','"+self.get_argument("module")+"','"+self.get_argument("difficult")+"');"
        result = common.execute("sangao",sql)
        if result:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");window.location.href="index";</script></body></html>')  
        else:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加失败！");window.location.href="index";</script></body></html>')  



        
class editHandler(tornado.web.RequestHandler):
    def get(self):
        db_name = ""
        question_type = self.get_argument("question_type")
        if question_type == 'single_choice':
            db_name = "single_choice_question"
            sql = "select * from "+db_name+ " where id ="+self.get_argument("question_id")
            print("sql:",sql)
            question = common.find("sangao",sql)
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","single_choice_edit.html"),question=question)            
        if question_type == 'true_false':
            db_name = 'tf_question'
            sql = "select * from "+db_name+ " where id ="+self.get_argument("question_id")
            print("sql:",sql)
            question = common.find("sangao",sql)
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","true_false_edit.html"),question=question)                  
        if question_type == 'operation':
            db_name = 'opereation_question'
            sql = "select * from "+db_name+ " where id ="+self.get_argument("question_id")
            print("sql:",sql)
            question = common.find("sangao",sql)
            if question:
                self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","operation_edit.html"),question=question)                  
        


    def post(self):

        if self.get_argument("question_type")=='single_choice':
            data={}
            data["title"]=self.get_argument("title")
            data["choice1"]=self.get_argument("choice1")
            data["choice2"]=self.get_argument("choice2")
            data["choice3"]=self.get_argument("choice3")
            data["choice4"]=self.get_argument("choice4")
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
            data["answer"]=self.get_argument("correct_answer")
            data["difficult"]=self.get_argument("difficult")
            sql="update single_choice_question set title='"+data["title"]+"',choice1='"+data["choice1"]+"',choice2='"+data["choice2"]+"',choice3='"+data["choice3"]+"',choice4='"+data["choice4"]+"',module='"+data["module"]+"',answer='"+data["answer"]+"',difficult='"+data["difficult"]+"' where id = "+self.get_argument("question_id")
            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");window.location.href="select";</script></body></html>')  



class indexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Knowledge","index.html"))
    def post(self):
        pass


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","select.html"))

    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        print("post_data:",post_data)
        data={}
        data["module"]=self.get_argument("module")
        data["difficult"]=self.get_argument("difficult")
        single_choice_questions={}
        true_false_questions={}
        operation_questions={}
        multiple_choice_questions={}
        fill_blank_questions={}
        if self.get_argument("type")=="single_choice":
            sql="select * from single_choice_question where module='"+data["module"]+"' and difficult='"+data["difficult"]+"'"
            single_choice_questions=common.select("sangao",sql)
        if self.get_argument("type")=="true_false":
            sql="select * from tf_question where module='"+data["module"]+"'"
            true_false_questions=common.select("sangao",sql)
        if self.get_argument("type")=="operation":
            sql="select * from operation_question where module='"+data["module"]+"'"
            operation_questions=common.select("sangao",sql) 
        if self.get_argument("type")=="multiple_choice":
            sql="select * from multiple_choice_question"
            multiple_choice_questions=common.select("sangao",sql)     
        if self.get_argument("type")=="fill_blank":
            sql="select * from fill_blank_question"
            fill_blank_questions=common.select("sangao",sql)  
        print("结果集multiple_choice_questions",multiple_choice_questions)                                  
        print("结果集single_choice_questions",single_choice_questions)       
        print("结果集true_false_questions",true_false_questions)
        print("结果集operation_questions",operation_questions)
        print("结果集fill_blank_questions",fill_blank_questions)
        
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Question","result.html")
        ,module=data["module"]
        ,question_type=self.get_argument("type")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,multiple_choice_questions=multiple_choice_questions        
        ,fill_blank_questions=fill_blank_questions 
        ,single_choice_questions=single_choice_questions)

      
