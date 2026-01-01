# sangao_admin/QuestionController.py





import tornado
import sqlite3
import warnings
import os
import uuid
import config
import json  # 确保已导入

warnings.filterwarnings('ignore')
from sangao_admin.KnowledgeModel import Knowledge
from sangao_admin.QuestionModel import SingleChoiceModel
from sangao_admin.QuestionModel import KnowledgeModel
import logging
logger = logging.getLogger(__name__)
from common.CommonModel import Common
from common.OperationQuestionModel import OperationQuestionModel
from common.SingleChoiceQuestionModel import SingleChoiceQuestionModel

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from single_choice_question"
        single_choice_questions=Common.select("sangao",sql)
        sql="select * from tf_question"
        true_false_questions=Common.select("sangao",sql)
        sql="select * from operation_question"
        operation_questions=Common.select("sangao",sql)         
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","lists.html")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,single_choice_questions=single_choice_questions)

class sourceListsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from question_source"
        sources=Common.select("sangao",sql)
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","source_lists.html"),sources=sources)



class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","add.html"))

def get_upload_path(question_type, file_type="images"):
    """统一获取上传路径"""
    mapping = {
        "single_choice": ("Question", "images", "single_choice"),
        "multiple_choice": ("Question", "images", "multiple_choice"),
        "fill_blank": ("Question", "images", "fill_blank"),
        "true_false": ("Question", "images", "true_false"),
        "operation": ("Question", file_type, "operation"),
    }
    if question_type in mapping:
        return config.get_path("sangao_admin", *mapping[question_type])
    return config.get_path("sangao_admin", "Question", "upload")


class delHandler(tornado.web.RequestHandler):
    def get(self):
        db_name = ""
        question_type = self.get_argument("question_type")
        #获取知识点分类
        sql="select * from knowledge"
        knowledges=Common.select("sangao",sql)

        if question_type == 'single_choice':
            db_name = "single_choice_question"
            sql = "select question.id as question_id,source.id as source_id,source.publicer as publicer,source.public_year as public_year,question.difficult as difficult,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge join question_source as source on source.id=question.source  where question.id ="+self.get_argument("question_id")            

            question = Common.find("sangao",sql)
            modules=Common.select("sangao","select * from module")
            knowledges=Common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))   
            sources=Common.select("sangao","select * from question_source")         
            if question:
                self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","single_choice_edit.html"),question=question,modules=modules,knowledges=knowledges,sources=sources)
            else:
                self.write("题目不存在！")            
        if question_type == 'true_false':
            table_name = 'tf_question'
            sql = "delete from "+table_name+" where id="+self.get_argument("question_id")
            reslut = Common.execute("sangao",sql)
            if reslut:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>')
        if question_type == 'operation':
            db_name = 'operation_question'
            sql = "select question.id as question_id,question.material as material,question.difficult as difficult,question.picture as picture,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            question = Common.find("sangao",sql)            
            modules=Common.select("sangao","select * from module")
            knowledges=Common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))                 
            # print("sql:",sql)
            question = Common.find("sangao",sql)
            if question:
                self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","operation_edit.html"),question=question,modules=modules,knowledges=knowledges)                  
        
        if question_type == 'multiple_choice':
            db_name = "multiple_choice_question"
            sql = "select question.id as question_id,question.difficult as difficult,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.choice5 as choice5,question.choice6 as choice6,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from "+db_name+ " as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+self.get_argument("question_id")            

            question = Common.find("sangao",sql)            
            modules=Common.select("sangao","select * from module")
            knowledges=Common.select("sangao","select * from knowledge where belong_module_id ="+str(question["module_id"]))            
            # print("sql:",sql)

            if question:
                self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","multiple_choice_edit.html"),question=question,modules=modules,knowledges=knowledges)   

        if question_type == 'fill_blank':
            table_name = 'fill_blank_question'
            sql = "delete from "+table_name+" where id="+self.get_argument("question_id")
            reslut = Common.execute("sangao",sql)
            if reslut:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>')



class editHandler(tornado.web.RequestHandler):

    # 👇 新增：预格式化数值为字符串（使用 %g 或其他格式）
    def format_score(self,val):
        return '%g' % float(val) if val is not None else '0' 


    def get(self):
        question_type = self.get_argument("question_type")
        question_id = self.get_argument("question_id")

        # 获取通用数据
        modules = Common.select("sangao", "SELECT * FROM module")
        knowledges_all = Common.select("sangao", "SELECT * FROM knowledge")

        def render_template(template, **kwargs):
            self.render(os.path.join(config.BASE_DIR, "sangao_admin", "templates", "Question", template), **kwargs)

        if question_type == 'single_choice':

            logging.info(f"question_id:{question_id}")
            Question = SingleChoiceQuestionModel(question_id)
            if Question is None:
                self.write("题目不存在！")
                return

            knowledges = Common.select("sangao", "SELECT * FROM knowledge WHERE belong_module_id = ?", (Question.to_dict()["module_id"],))
            sources = Common.select("sangao", "SELECT * FROM question_source")
            render_template("single_choice_edit.html", question=Question.to_dict(), modules=modules, knowledges=knowledges, sources=sources)

        elif question_type == 'true_false':
            sql = """
                SELECT tf.id AS question_id, tf.title, tf.answer, tf.knowledge, tf.difficult,
                       m.name AS module_name, tf.module AS module_id, k.name AS knowledge_name
                FROM tf_question tf
                JOIN module m ON m.id = tf.module
                JOIN knowledge k ON k.id = tf.knowledge
                WHERE tf.id = ?
            """
            question = Common.find("sangao", sql, (question_id,))
            if not question:
                self.write("题目不存在！")
                return
            knowledges = Common.select("sangao", "SELECT * FROM knowledge WHERE belong_module_id = ?", (question["module_id"],))
            render_template("true_false_edit.html", question=question, modules=modules, knowledges=knowledges)

        elif question_type == 'operation':
            Question = OperationQuestionModel(question_id)
            logger.info(f"question:{Question.to_dict()}")
            if not Question:
                self.write("题目不存在！")
                return
            knowledges = Common.select("sangao", "SELECT * FROM knowledge WHERE belong_module_id = ?", (Question.module_id,))


            render_template(
                "operation_edit.html",
                question=Question.to_dict(),
                modules=modules,
                knowledges=knowledges,
            )




        elif question_type == 'multiple_choice':
            sql = """
                SELECT q.id AS question_id, q.difficult, q.picture, q.choice1, q.choice2, q.choice3,
                       q.choice4, q.choice5, q.choice6, q.title, q.answer, q.knowledge,
                       m.name AS module_name, q.module AS module_id, k.name AS knowledge_name
                FROM multiple_choice_question q
                JOIN module m ON m.id = q.module
                JOIN knowledge k ON k.id = q.knowledge
                WHERE q.id = ?
            """
            question = Common.find("sangao", sql, (question_id,))
            if not question:
                self.write("题目不存在！")
                return
            knowledges = Common.select("sangao", "SELECT * FROM knowledge WHERE belong_module_id = ?", (question["module_id"],))
            render_template("multiple_choice_edit.html", question=question, modules=modules, knowledges=knowledges)

        elif question_type == 'fill_blank':
            sql = """
                SELECT q.id AS question_id, q.difficult, q.picture, q.title, q.answer, q.knowledge,
                       m.name AS module_name, q.module AS module_id, k.name AS knowledge_name
                FROM fill_blank_question q
                JOIN module m ON m.id = q.module
                JOIN knowledge k ON k.id = q.knowledge
                WHERE q.id = ?
            """
            question = Common.find("sangao", sql, (question_id,))
            if not question:
                self.write("题目不存在！")
                return
            knowledges = Common.select("sangao", "SELECT * FROM knowledge WHERE belong_module_id = ?", (question["module_id"],))
            render_template("fill_blank_edit.html", question=question, modules=modules, knowledges=knowledges)

    def post(self):
        question_type = self.get_argument("question_type")
        question_id = self.get_argument("question_id")

        def save_file(field_name, sub_dir="images"):
            if self.request.files.get(field_name):
                upload = self.request.files[field_name][0]
                ext = os.path.splitext(upload['filename'])[1]
                filename = str(uuid.uuid4()) + ext
                path = get_upload_path(question_type, file_type=sub_dir)
                os.makedirs(path, exist_ok=True)
                with open(os.path.join(path, filename), 'wb') as f:
                    f.write(upload['body'])
                return filename
            return None

        conn = sqlite3.connect(os.path.join(config.BASE_DIR, "db", "sangao.db"))
        cursor = conn.cursor()
        try:
            if question_type == 'single_choice':
                data = {
                    "title": self.get_argument("title"),
                    "choice1": self.get_argument("choice1"),
                    "choice2": self.get_argument("choice2"),
                    "choice3": self.get_argument("choice3"),
                    "choice4": self.get_argument("choice4"),
                    "answer": self.get_argument("correct_answer"),
                    "module": self.get_argument("module"),
                    "knowledge": self.get_argument("knowledge"),
                    "difficult": self.get_argument("difficult"),
                    "source": self.get_argument("source"),
                    "explain":self.get_argument("explain")
                }
                pic = save_file('photo1')
                if pic:
                    data["picture"] = pic
                cols = ", ".join(data.keys())
                placeholders = ", ".join(["?"] * len(data))
                set_clause = ", ".join([f"{k}=?" for k in data.keys()])
                # 更新题目
                cursor.execute(f"UPDATE single_choice_question SET {set_clause} WHERE id=?", list(data.values()) + [question_id])
                conn.commit()

            elif question_type == 'operation':
                data = {
                    "title": self.get_argument("title"),
                    "module": self.get_argument("module"),
                    "knowledge": self.get_argument("knowledge"),
                    "difficult": self.get_argument("difficult"),
                }
                # 文件处理
                if save_file('photo1'):
                    data["picture"] = save_file('photo1')
                if save_file('material', 'files'):
                    data["material"] = save_file('material', 'files')
                if save_file('material2', 'files'):
                    data["material2"] = save_file('material2', 'files')
                if save_file('correct_answer', 'files'):
                    data["answer"] = save_file('correct_answer', 'files')
                if save_file('explain', 'video'):
                    data["explain"] = save_file('explain', 'video')                    

                # 评分规则
                scoring_rules = {}
                # 👇 修改：增加 conditional_formatting
                for key in ["cell_values", "formulas", "chart", "merged_cells", "conditional_formatting"]:
                    if f"rule_enabled_{key}" in self.request.arguments:
                        try:
                            score = float(self.get_body_argument(f"rule_score_{key}", default="0"))
                            desc = self.get_body_argument(f"rule_desc_{key}", default=key)
                            if score > 0:
                                scoring_rules[key] = {"desc": desc, "max_score": score}
                        except ValueError:
                            pass
                compare_range = self.get_body_argument("compare_range", default="").strip()
                if compare_range:
                    scoring_rules["compare_range"] = compare_range
                data["score_rules"] = json.dumps(scoring_rules, ensure_ascii=False)





                set_clause = ", ".join([f"{k}=?" for k in data.keys()])
                cursor.execute(f"UPDATE operation_question SET {set_clause} WHERE id=?", list(data.values()) + [question_id])
                conn.commit()

            # 其他题型类似处理（略，按相同模式补充）

            self.write('<html><head><title>提醒</title></head><body><script> alert("修改成功！"); window.location.href="/sangao_admin/Question/select"; </script></body></html>')

        except Exception as e:
            logger.error(f"编辑题目失败: {e}")
            conn.rollback()
            self.write('<script>alert("修改失败！"); history.back();</script>')
        finally:
            conn.close()


# 其他 Handler（listsHandler, addHandler, selectHandler 等）保持不变，
# 但建议后续也将其 SQL 查询改为参数化形式。

class joinExamHandler(tornado.web.RequestHandler):
    def get(self):
        # Common.tongji("exam_paper_del")
        data={}
        data["belong_exam_paper_id"]
        sql="insert into exam_plan(belong_exam_paper_id,question_type,question_id) values()"


class examPaperDelHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        Common.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()




class handinHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入交卷模块")
        Common.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","index.html"))
    def post(self):
        pass



class sourceAddHandler(tornado.web.RequestHandler):
    def post(self):
        data={}
        data["source"]=self.get_argument("source")
        data["public_time"]=self.get_argument("public_time")


        sql="insert into question_source(public_year,publicer) values('"+data["public_time"]+"','"+data["source"]+"')"
        result= Common.execute("sangao",sql)
        if result:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");</script></body></html>')


    def get(self):
        
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","source_add.html"))



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
        modules=Common.select("sangao","select * from module")
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","single_choice_add.html"),knowledges=Knowledges,modules=modules)


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
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        Knowledges=Knowledge.select()
        modules=Common.select("sangao","select * from module")
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","multiple_choice_add.html"),knowledges=Knowledges,modules=modules)


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        konwledges=KnowledgeModel.select()
        modules = Common.select("sangao","select * from module")        
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","select.html"),knowledges=konwledges,modules=modules)

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
        
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","result.html")
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
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
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
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","true_false_add.html"),exam_papers=exam_papers)




class operationAddHandler(tornado.web.RequestHandler):
    def post(self):
        data = {}
        UPLOAD_FILE_PATH = config.get_path("sangao_admin", "Question", "files", "operation")
        os.makedirs(UPLOAD_FILE_PATH, exist_ok=True)

        # 处理素材文件 material
        if self.request.files.get('material', None):
            uploadFile = self.request.files['material'][0]
            filename = str(uuid.uuid4()) + os.path.splitext(uploadFile['filename'])[1]
            file_path = os.path.join(UPLOAD_FILE_PATH, filename)
            with open(file_path, 'wb') as f:
                f.write(uploadFile['body'])
            data["material"] = filename
        else:
            data["material"] = ""

        # 处理标准答案文件 correct_answer
        if self.request.files.get('correct_answer', None):
            uploadFile = self.request.files['correct_answer'][0]
            filename = str(uuid.uuid4()) + os.path.splitext(uploadFile['filename'])[1]
            file_path = os.path.join(UPLOAD_FILE_PATH, filename)
            with open(file_path, 'wb') as f:
                f.write(uploadFile['body'])
            data["correct_answer"] = filename
        else:
            data["correct_answer"] = ""

        # 处理图片 photo1
        if self.request.files.get('photo1', None):
            uploadFile = self.request.files['photo1'][0]
            filename = str(uuid.uuid4()) + os.path.splitext(uploadFile['filename'])[1]
            img_path = config.get_path("sangao_admin", "Question", "images", "operation")
            os.makedirs(img_path, exist_ok=True)
            file_path = os.path.join(img_path, filename)
            with open(file_path, 'wb') as f:
                f.write(uploadFile['body'])
            data["picture"] = filename
        else:
            data["picture"] = ""

        data["title"] = self.get_argument("title")
        data["module"] = self.get_argument("module")
        data["knowledge"] = self.get_argument("knowledge", default="12")
        data["difficult"] = self.get_argument("difficult", default="简单")


        # === 构建评分规则字典 ===
        scoring_rules = {}

        # 👇 修改：增加 conditional_formatting
        rule_keys = ["cell_values", "formulas", "chart", "merged_cells", "conditional_formatting"]
        for key in rule_keys:
            is_enabled = f"rule_enabled_{key}" in self.request.arguments
            if is_enabled:
                try:
                    max_score = float(self.get_body_argument(f"rule_score_{key}", default="0"))
                    desc = self.get_body_argument(f"rule_desc_{key}", default=key)
                    if max_score > 0:
                        scoring_rules[key] = {
                            "desc": desc,
                            "max_score": max_score
                        }
                except ValueError:
                    pass

        compare_range = self.get_body_argument("compare_range", default="").strip()
        if compare_range:
            scoring_rules["compare_range"] = compare_range

        score_rules_json = json.dumps(scoring_rules, ensure_ascii=False) if scoring_rules else ""





        # 可选：比对区域
        compare_range = self.get_body_argument("compare_range", default="").strip()
        if compare_range:
            scoring_rules["compare_range"] = compare_range

        # 序列化为 JSON 字符串（确保兼容 SQLite TEXT）
        score_rules_json = json.dumps(scoring_rules, ensure_ascii=False) if scoring_rules else ""

        # === 插入数据库 ===
        sql = """
        INSERT INTO operation_question 
        (title, material, answer, picture, module, knowledge, difficult, score_rules) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data["title"],
            data["material"],
            data["correct_answer"],
            data["picture"],
            data["module"],
            data["knowledge"],
            data["difficult"],
            score_rules_json
        )

        conn = sqlite3.connect(os.path.join(config.BASE_DIR, "db", "sangao.db"))
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("操作题添加成功！");window.location.href="/sangao_admin/Question/select";</script></body></html>')
        except Exception as e:
            logger.error(f"插入操作题失败: {e}")
            conn.rollback()
            self.write('<html><head><title>错误</title></head><body><script type="text/javascript">window.alert("添加失败，请重试！");history.back();</script></body></html>')
        finally:
            conn.close()
    def get(self):
            modules=Common.select("sangao","select * from module")
                            
            self.render(os.path.join(config.BASE_DIR,"sangao_admin","templates","Question","operation_add.html"),modules=modules)                  
                       