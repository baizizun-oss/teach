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
import sqlite3
import os
import re
import subprocess
import tempfile
import openpyxl  # 需要 pip install openpyxl
import logging
logger = logging.getLogger(__name__)
class commonHandler():
    def tongji(modulename):
        # 统计模块开始
        conn = sqlite3.connect(
            os.path.join("db","baigaopeng_myportal.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'"+modulename+"')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束

class questionListsHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(
            os.path.join("db","baigaopeng_myportal.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'exam_lists')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        sql = "select * from exam_paper"
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        print(exam_papers)
        self.render("sangao\\templates\\Exam\\exam_paper_lists.html",exam_papers=exam_papers)

class examPaperListsHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"sangao","templates","Index","login.html"))
        else:

            # 统计模块开始
            # conn = sqlite3.connect(
            #     os.path.join("db","sangao.db"))
            # sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'exam_paper_lists')"
            # result = conn.cursor().execute(sql)
            # conn.commit()
            # conn.close()
            # 统计模块结束
            sql="select * from exam_paper"
            exam_papers=common.select("sangao",sql)

            print(f"你好：{exam_papers}")
            logger.info("exam_papers: %s", exam_papers)
            #计算出各个试卷的总分并赋给exam_papers
            for key in range(len(exam_papers)):
                exam_papers[key]["total"]=0 #总分赋初值
                sql="select * from exam_plan where belong_exam_paper_id = "+str(exam_papers[key]["id"])
                questions=common.select("sangao",sql)
                logger.info("questions: %s",questions)
                for question in questions:
                    if question["question_type"]==1:#单选
                        exam_papers[key]["total"]+=2
                    if question["question_type"]==2:#判断
                        exam_papers[key]["total"]+=2
                    if question["question_type"]==3:#多选
                        exam_papers[key]["total"]+=4
                    if question["question_type"]==4:#操作
                        exam_papers[key]["total"]+=15
                    if question["question_type"]==5:#填空
                        exam_papers[key]["total"]+=1
            logger.info("exam_papers: %s ",exam_papers)
            self.render(os.path.join(common.BASE_DIR,"sangao","templates","Exam","exam_paper_lists.html"),exam_papers=exam_papers)


class examPaperAddHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        commonHandler.tongji("exam_paper_add")
        self.render("sangao/templates/Exam/exam_paper_add.html")
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["ctime"]=int(time.time())
        data["author"]=self.get_argument("author")
        sql="insert into exam_paper(title,author,ctime) values('"+data["title"]+"','"+data["author"]+"',"+data["ctime"]+")"
        print("sql语句:" + sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        print("result:", result)

        conn.commit()
        conn.close()
        self.write("添加成功")

class examPaperEditHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from exam_plan where exam_paper_id="+self.get_argument("id")
        exam_plan=common.select("sangao",sql)
        self.render("sangao/templates/Exam/exam_paper_edit.html"
                    , questions=exam_plan
                    )

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


class examPaperDelHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        commonHandler.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"db","sangao.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()



class editHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"sangao","templates","Index","login.html"))
        else:        
            single_choice_questions={}
            true_false_questions={}
            operation_questions={}
            multiple_choice_questions={}
            fill_blank_questions={}
            single_choice_sql="select exam_plan.id,question.id as question_id,question.title,question.choice1,question.choice2,question.choice3,question.choice4,question.picture from exam_plan JOIN single_choice_question as question ON exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type =1"
            single_choice_questions = common.select("sangao",single_choice_sql)
            print("single_choice_questions",single_choice_questions)

            multiple_choice_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.choice5 as choice5,question.choice6 as choice6 from exam_plan join multiple_choice_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 3"
            multiple_choice_questions = common.select("sangao",multiple_choice_sql)

            true_false_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture from exam_plan join tf_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 2"
            true_false_questions = common.select("sangao",true_false_sql)
            
            operation_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture,question.material,question.material2 from exam_plan join operation_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 4"
            operation_questions= common.select("sangao",operation_sql)

            fill_blank_sql = "select exam_plan.id,exam_plan.question_id,question.title,question.picture from exam_plan join fill_blank_question as question on exam_plan.question_id = question.id where belong_exam_paper_id="+self.get_argument("id")+ " and question_type = 5"
            fill_blank_questions = common.select("sangao",fill_blank_sql)
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
            
            self.render(os.path.join(common.BASE_DIR,"sangao","templates","Exam","edit.html")
            ,user_id=self.get_cookie("user_id")
            ,exam_paper_id=self.get_argument("id")
            ,operation_questions=operation_questions
            ,true_false_questions=true_false_questions
            ,multiple_choice_questions=multiple_choice_questions        
            ,fill_blank_questions=fill_blank_questions 
            ,single_choice_questions=single_choice_questions)

    def post(self):
        data={}
        for i in range(len(self.get_arguments("question_id"))):
            if self.get_arguments("question_type")[i] == "operation":
                # 上传文件的处理
                UPLOAD_FILE_PATH = 'sangao\\templates\\Exam\\upload\\'
                # 获取所有同名文件
                files = self.request.files['file']  # 'file' 是表单中的input元素name属性值
                print("上传文件：",files)
                for i in range(len(files)):
                    # 生成新的文件名
                    filepath = str(uuid.uuid4()) + os.path.splitext(files[i]['filename'])[1]
                    # 保存文件到服务器
                    with open(os.path.join(UPLOAD_FILE_PATH, filepath), 'wb') as f:
                        f.write(files[i]['body'])
                        data["answer"]=filepath
                        print("answer:",data["answer"])
                #self.write("上传成功")

            elif self.get_arguments("question_type")[i] == "single_choice" or self.get_arguments("question_type")[i]=="true_false":
                data["answer"]=self.get_argument("answer["+self.get_arguments("question_id")[i]+"]")
            sql = "insert into student_answer(student_id,question_id,answer,ctime,question_type) values(" + self.get_argument("user_id") + "," + self.get_arguments("question_id")[i] + ",'" + data["answer"] + "','" + str(int(time.time())) + "','"+self.get_arguments("question_type")[i]+"')"
            result = common.execute("sangao",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("提交成功!");window.location.href="exam_paper_lists";</script></body></html>')                



import re
import os
import uuid
import time
import sqlite3
import logging
from tornado.web import RequestHandler

logger = logging.getLogger(__name__)

def normalize_code(code_str):
    """标准化代码：移除注释、空白字符，便于比对"""
    if not code_str:
        return ""
    # 移除单行注释（保留字符串内的 #）
    lines = []
    for line in code_str.splitlines():
        # 简单处理：从第一个 # 开始截断（不处理字符串内 #，因题目简单可接受）
        idx = line.find('#')
        if idx != -1:
            line = line[:idx]
        lines.append(line)
    no_comment = '\n'.join(lines)
    # 移除所有空白字符（空格、换行、制表符等）
    return re.sub(r'\s+', '', no_comment)


class handinHandler(RequestHandler):

    def post(self):
        student_id = self.get_argument("user_id")
        if not student_id:
            self.write("未登录，请先登录")
            return

        exam_paper_id = self.get_argument("exam_paper_id", None)
        if not exam_paper_id:
            self.write("缺少试卷ID")
            return

        # ✅ 生成本次提交的唯一 submission_id（UUID）
        submission_id = str(uuid.uuid4())

        total_score = 0
        answer_records = []

        # === 1. 单选题 ===
        sc_ids = self.get_arguments("single_choice_question_id")
        for qid in sc_ids:
            ans = self.get_argument(f"single_choice_answer[{qid}]", None)
            if ans is None:
                self.write(f"单选题 {qid} 未作答")
                return
            answer_records.append((int(qid), "single_choice", ans))

        # === 2. 判断题 ===
        tf_ids = self.get_arguments("tf_question_id")
        for qid in tf_ids:
            ans = self.get_argument(f"tf_answer[{qid}]", None)
            if ans is None:
                self.write(f"判断题 {qid} 未作答")
                return
            answer_records.append((int(qid), "true_false", ans))

        # === 3. 多选题 ===
        mc_ids = self.get_arguments("multiple_choice_question_id")
        for qid in mc_ids:
            answers = self.get_arguments(f"multiple_choice_answer[{qid}]")
            ans_str = ",".join(sorted(answers)) if answers else ""
            answer_records.append((int(qid), "multiple_choice", ans_str))

        # === 4. 填空题 ===
        fb_ids = self.get_arguments("fill_blank_question_id")
        for qid in fb_ids:
            ans = self.get_argument(f"fill_blank_answer[{qid}]", "").strip()
            if not ans:
                self.write(f"填空题 {qid} 未填写")
                return
            answer_records.append((int(qid), "fill_blank", ans))

        # === 5. 操作题 ===
        op_ids = self.get_arguments("operation_question_id")
        for qid in op_ids:
            files = self.request.files.get(f"file_{qid}", [])
            if not files:
                self.write(f"操作题 {qid} 未上传文件")
                return

            upload_dir = os.path.join(common.BASE_DIR, "sangao", "templates", "Exam", "upload")
            os.makedirs(upload_dir, exist_ok=True)
            filename = str(uuid.uuid4()) + os.path.splitext(files[0]['filename'])[1]
            file_path = os.path.join(upload_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(files[0]['body'])

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    student_code = f.read()
            except Exception as e:
                logger.error(f"读取操作题文件失败 {file_path}: {e}")
                student_code = ""

            answer_records.append((int(qid), "operation", student_code))

        # === 6. 逐题评分 + 保存（带 submission_id）===
        for qid, qtype, student_ans in answer_records:
            correct_ans = self.get_correct_answer("sangao", qtype, qid)
            if correct_ans is None:
                logger.error(f"未找到标准答案: 题目ID={qid}, 类型={qtype}")
                continue

            score = 0
            if qtype in ["single_choice", "true_false"]:
                if str(student_ans).strip() == str(correct_ans).strip():
                    score = 2
            elif qtype == "multiple_choice":
                def sort_choices(s):
                    if not s:
                        return ""
                    return ','.join(sorted([x.strip().upper() for x in s.split(',') if x.strip()]))
                if sort_choices(student_ans) == sort_choices(correct_ans):
                    score = 4
            elif qtype == "fill_blank":
                std_opts = [opt.strip().lower() for opt in correct_ans.split('|')]
                if student_ans.strip().lower() in std_opts:
                    score = 1
            elif qtype == "operation":
                if normalize_code(student_ans) == normalize_code(correct_ans):
                    score = 15

            total_score += score

            # ✅ 插入时带上 submission_id
            sql = """
            INSERT INTO student_answer(student_id, question_id, user_answer, ctime, question_type, score, exam_paper_id, submission_id,source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            """
            try:
                common.execute("sangao", sql, (
                    student_id, qid, student_ans[:1000], int(time.time()), qtype, score, exam_paper_id, submission_id,'exam'
                ))
                logger.debug("Executing SQL: %s with params: %s", sql, (student_id, qid, student_ans[:1000], int(time.time()), qtype, score, exam_paper_id, submission_id,'exam'))                
            except Exception as e:
                logger.error(f"保存答题记录失败 (qid={qid}): {e}")

        #self.write(f'<script>alert("提交成功！总分：{total_score},得分详情可在“我的作答”中查看"); window.location="/sangao/Answer/exam_list?user_id={student_id}";</script>')
        self.write(f'''
    <script type="text/javascript">
        if (confirm("提交成功！总分：{total_score}\\n得分详情可在“我的作答”中查看。\\n点击“确定”查看答题记录")) {{
            window.location.href = "/sangao/Answer/exam_list?user_id={student_id}";
        }} else {{
            window.history.back(); // 或者留在当前页，按需调整
        }}
    </script>
    ''')
    
    def get_correct_answer(self, db_name, question_type, question_id):
        """根据题型和ID获取标准答案"""
        table_map = {
            "single_choice": "single_choice_question",
            "true_false": "tf_question",
            "multiple_choice": "multiple_choice_question",
            "fill_blank": "fill_blank_question",
            "operation": "operation_question"
        }
        table = table_map.get(question_type)
        if not table:
            return None

        db_path = os.path.join(common.BASE_DIR, "db", f"{db_name}.db")
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(f"SELECT answer FROM {table} WHERE id = ?", (question_id,))
            row = cur.fetchone()
            conn.close()
            return row["answer"] if row else None
        except Exception as e:
            logger.error(f"查询标准答案失败: {e}")
            return None




class errorRankingHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
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
        self.render("sangao/templates/Exam/error_ranking_select.html",exam_papers=exam_papers)

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
        #	for name,value in taskset.items():
        # print('%s=%s'%(name,value))


        # print("tasks is:",tasks)
        ##print#print("data is:",data)
        self.render("sangao/Learn/templates/result.html"
                    , tasks=tasks)
        #	       #conn.

