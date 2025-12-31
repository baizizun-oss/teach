# TeachExamController.py
import os
import time
from pathlib import Path
import tornado.web
import myportal.common as common
# from sangao_admin.AudioProcessService import AudioProcessService
import logging
import json
from jobs.asr_client import transcribe_audio_file_sync 
from jobs.llm_client import polish_transcript_sync
import config
from sangao_admin.RecordService import extract_teaching_chain
import uuid


logger = logging.getLogger(__name__)


class listsHandler(tornado.web.RequestHandler):
    def get(self):

        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","lists.html")
        
                    )

class questionListsHandler(tornado.web.RequestHandler):
    def get(self):
        records = common.select("sangao", "SELECT * FROM teach_exam_question")
        self.render(
            os.path.join(common.BASE_DIR, "sangao_admin", "templates", "TeachExam", "question_lists.html"),
            records=records
        )

class questionDetailHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from teach_exam_question where id="+self.get_argument("id")
        question = common.find("sangao",sql)
        
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","question_detail.html"),
                    question=question
                    )

class teachDetailHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from teach_exam_teach where id="+self.get_argument("id")
        question = common.find("sangao",sql)
        
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","teach_detail.html"),
                    teach=question,
                    board_design=json.dumps(question["board_design"]),
                    design=json.dumps(question["design"]),
                    )

class teachListsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from teach_exam_teach"
        teaches=common.select("sangao",sql)

        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","teach_lists.html"),
                    teaches=teaches
                    )


class questionAddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","question_add.html"))
        
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["my_answer"]=self.get_argument("my_answer")
        data["my_logic"]=self.get_argument("my_logic")
        sql="insert into teach_exam_question(question,my_answer,my_logic,ctime) values(?,?,?,?)"
        result=common.execute("sangao",sql,(data["title"],data["my_answer"],data["my_logic"],int(time.time())))
        if result:
            self.write("增加成功！")

class questionEditHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from teach_exam_question where id = "+self.get_argument("id")
        question=common.find("sangao",sql)

        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","question_edit.html"),
                    question=question
                    )
        
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["my_answer"]=self.get_argument("my_answer")
        data["my_logic"]=self.get_argument("my_logic")
        data["reflection"]=self.get_argument("reflection")
        data["score"]=self.get_argument("score")
        sql="update teach_exam_question set question='"+data["title"]+"',score="+data["score"]+",my_answer='"+data["my_answer"]+"',my_logic='"+data["my_logic"]+"',reflection='"+data["reflection"]+"' where id="+self.get_argument("id")
        result=common.execute("sangao",sql)
        if result:
            self.write("增加成功！")

class teachEditHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from teach_exam_teach where id = "+self.get_argument("id")
        teach=common.find("sangao",sql)
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","teach_edit.html"),
                    teach=teach
                    )
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["my_answer"]=self.get_argument("my_answer")
        data["my_logic"]=self.get_argument("my_logic")
        data["reflection"]=self.get_argument("reflection")
        data["board_design"]=self.get_argument("my_board")
        data["design"]=self.get_argument("design")
        UPLOAD_FILE_PATH = STATIC_PATHS["board_pic"]
        if self.request.files.get('board_pic', None):
            uploadFile = self.request.files['board_pic'][0]
            # 生成新的文件名
            filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['board_pic'][0]['filename'])[1]
            fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename),'wb')
            fileObj.write(uploadFile['body'])
            data["board_pic"]=filename           
        else:
            sql="select * from teach_exam_teach where id="+self.get_argument("id")
            teach=common.find("sangao",sql)
            data["board_pic"]=teach["board_pic"]     
        if self.request.files.get('design_pic', None):
            uploadFile = self.request.files['design_pic'][0]
            # 生成新的文件名
            filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['design_pic'][0]['filename'])[1]
            fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename),'wb')
            fileObj.write(uploadFile['body'])
            data["design_pic"]=filename           
        else:
            sql="select * from teach_exam_teach where id="+self.get_argument("id")
            teach=common.find("sangao",sql)
            data["design_pic"]=teach["design_pic"]                              
        sql="update teach_exam_teach set title='"+data["title"]+"',my_answer='"+data["my_answer"]+"',my_logic='"+data["my_logic"]+"',reflection='"+data["reflection"]+"',board_design='"+data["board_design"]+"',design='"+data["design"]+"',board_pic='"+data["board_pic"]+"',design_pic='"+data["design_pic"]+"' where id="+self.get_argument("id")
        result=common.execute("sangao",sql)
        if result:
            self.write("增加成功！")



class teachAddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","TeachExam","teach_add.html"))
        
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["my_answer"]=self.get_argument("my_answer")
        data["my_logic"]=self.get_argument("my_logic")
        data["my_board"]=self.get_argument("my_board")
        UPLOAD_FILE_PATH = STATIC_PATHS["board_pic"]
        if self.request.files.get('board_pic', None):
            uploadFile = self.request.files['board_pic'][0]
            # 生成新的文件名
            filename = str(uuid.uuid4()) + os.path.splitext(self.request.files['board_pic'][0]['filename'])[1]
            fileObj = open(os.path.join(UPLOAD_FILE_PATH,filename),'wb')
            fileObj.write(uploadFile['body'])
            data["board_pic"]=filename           
        else:
            data["board_pic"]=""
        

        sql="insert into teach_exam_teach(title,my_answer,my_logic,ctime,board_design,board_pic) values(?,?,?,?,?,?)"
        result=common.execute("sangao",sql,(data["title"],data["my_answer"],data["my_logic"],int(time.time()),data["my_board"],data["board_pic"]))
        if result:
            self.write("增加成功！")