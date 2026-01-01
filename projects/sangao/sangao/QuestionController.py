import tornado
import sqlite3
import warnings
import os
import uuid
import config

warnings.filterwarnings('ignore')
import time
import json
from common.CommonModel import Common
from .QuestionModel import (
    SingleChoiceQuestionModel,
    MultipleChoiceQuestionModel,
    TrueFalseQuestionModel,
    FillBlankQuestionModel,
    OperationQuestionModel
)



class listsHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(
            "D:\\projects3\\db\\baigaopeng_myportal.db")
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'exam_lists')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
        sql = "select * from single_choice_question"
        single_choice_questions=Common.select("sangao", sql)
        print(single_choice_questions)
        sql = "select * from tf_question"
        tf_questions=Common.select("sangao", sql)
        print(tf_questions)
        self.render("sangao\\templates\\Question\\lists.html",single_choice_questions=single_choice_questions,tf_questions=tf_questions)



class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("暂无权限！请联系管理员!")

    

import uuid
import os
import time
import re
import sqlite3
import logging
from tornado.web import RequestHandler

logger = logging.getLogger(__name__)

def normalize_code(code_str):
    """标准化代码：移除注释、空白字符，便于比对"""
    if not code_str:
        return ""
    lines = []
    for line in code_str.splitlines():
        idx = line.find('#')
        if idx != -1:
            line = line[:idx]
        lines.append(line)
    no_comment = '\n'.join(lines)
    return re.sub(r'\s+', '', no_comment)



class handinHandler(RequestHandler):

    def post(self):
        student_id = self.get_cookie("user_id")
        if not student_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>")
            return

        question_type = self.get_argument("type", None)
        module = self.get_argument("module", None)
        if not question_type or not module:
            self.write("缺少题型或模块参数")
            return

        submission_id = str(uuid.uuid4())
        total_score = 0
        answer_records = []

        # 收集答案
        qids = self.get_arguments("question_id")
        if question_type == "single_choice":
            for qid in qids:
                ans = self.get_argument(f"answer[{qid}]", None)
                if ans is None:
                    self.write(f"单选题 {qid} 未作答")
                    return
                answer_records.append((int(qid), "single_choice", ans))
        elif question_type == "true_false":
            for qid in qids:
                ans = self.get_argument(f"answer[{qid}]", None)
                if ans is None:
                    self.write(f"判断题 {qid} 未作答")
                    return
                answer_records.append((int(qid), "true_false", ans))
        elif question_type == "multiple_choice":
            for qid in qids:
                answers = self.get_arguments(f"answer[{qid}]")
                ans_str = ",".join(sorted(answers)) if answers else ""
                answer_records.append((int(qid), "multiple_choice", ans_str))
        elif question_type == "fill_blank":
            for qid in qids:
                ans = self.get_argument(f"answer[{qid}]", "").strip()
                if not ans:
                    self.write(f"填空题 {qid} 未填写")
                    return
                answer_records.append((int(qid), "fill_blank", ans))
        elif question_type == "operation":
            upload_dir = os.path.join(config.BASE_DIR, "sangao", "templates", "Question", "upload")
            os.makedirs(upload_dir, exist_ok=True)
            for qid in qids:
                files = self.request.files.get(f"file_{qid}", [])
                if not files:
                    self.write(f"操作题 {qid} 未上传文件")
                    return
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
        else:
            self.write("不支持的题型")
            return

        # 评分并保存
        for qid, qtype, student_ans in answer_records:
            # 使用模型层获取正确答案
            if qtype == "single_choice":
                correct_ans = SingleChoiceQuestionModel.get_correct_answer(qid)
            elif qtype == "multiple_choice":
                correct_ans = MultipleChoiceQuestionModel.get_correct_answer(qid)
            elif qtype == "true_false":
                correct_ans = TrueFalseQuestionModel.get_correct_answer(qid)
            elif qtype == "fill_blank":
                correct_ans = FillBlankQuestionModel.get_correct_answer(qid)
            elif qtype == "operation":
                correct_ans = OperationQuestionModel.get_correct_answer(qid)
            else:
                correct_ans = None

            if correct_ans is None:
                logger.error(f"未找到标准答案: 题目ID={qid}, 类型={qtype}")
                continue

            # 评分逻辑保留在Controller中
            score = 0
            is_correct = 0

            if qtype in ["single_choice", "true_false"]:
                if str(student_ans).strip() == str(correct_ans).strip():
                    score = 2
                    is_correct = 1
            elif qtype == "multiple_choice":
                def sort_choices(s):
                    return ','.join(sorted([x.strip().upper() for x in s.split(',') if x.strip()])) if s else ""
                if sort_choices(student_ans) == sort_choices(correct_ans):
                    score = 4
                    is_correct = 1
            elif qtype == "fill_blank":
                std_opts = [opt.strip().lower() for opt in correct_ans.split('|')]
                if student_ans.strip().lower() in std_opts:
                    score = 1
                    is_correct = 1
            elif qtype == "operation":
                if normalize_code(student_ans) == normalize_code(correct_ans):
                    score = 15
                    is_correct = 1

            total_score += score

            Common.execute("sangao", """
                INSERT INTO student_answer(
                    student_id, question_id, answer, ctime, question_type, 
                    score, exam_paper_id, submission_id, source, is_correct
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                qid,
                student_ans[:1000],
                int(time.time()),
                qtype,
                score,
                None,
                submission_id,
                'practice',
                is_correct
            ))

        # 获取题目详情用于展示
        qids_list = [r[0] for r in answer_records]
        questions = self.fetch_submitted_questions(question_type, qids_list)

        # 特殊处理操作题代码内容
        if question_type == "operation":
            upload_dir = os.path.join(config.BASE_DIR, "sangao", "templates", "Question", "upload")
            for q in questions:
                try:
                    with open(os.path.join(upload_dir, q["student_answer"]), 'r', encoding='utf-8') as f:
                        q["student_code"] = f.read()
                except:
                    q["student_code"] = ""
                q["correct_code"] = q["correct_answer"]

        # # 渲染结果
        # self.render(
        #     os.path.join(config.BASE_DIR, "sangao", "templates", "Question", "answer_lists.html"),
        #     module=module,
        #     question_type=question_type,
        #     single_choice_questions=questions if question_type == "single_choice" else [],
        #     true_false_questions=questions if question_type == "true_false" else [],
        #     multiple_choice_questions=questions if question_type == "multiple_choice" else [],
        #     fill_blank_questions=questions if question_type == "fill_blank" else [],
        #     operation_questions=questions if question_type == "operation" else [],
        #     total_score=total_score
        # )

        self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("提交成功!请去"我的作答"中查看作答情况");</script></body></html>') 


    def fetch_submitted_questions(self, qtype, qids):
        if not qids:
            return []
        
        qids_str = ','.join(str(qid) for qid in qids)
        table_map = {
            "single_choice": "single_choice_question",
            "true_false": "tf_question",
            "multiple_choice": "multiple_choice_question",
            "fill_blank": "fill_blank_question",
            "operation": "operation_question"
        }
        table = table_map[qtype]

        # 获取题目
        questions = Common.select("sangao", f"SELECT * FROM {table} WHERE id IN ({qids_str})")
        
        # 获取学生答案
        student_id = self.get_cookie("user_id")
        student_answers = Common.select("sangao", f"""
            SELECT question_id, answer AS student_answer 
            FROM student_answer 
            WHERE question_id IN ({qids_str}) AND student_id = '{student_id}'
            ORDER BY ctime DESC
        """)

        ans_map = {row["question_id"]: row["student_answer"] for row in student_answers}
        for q in questions:
            q["student_answer"] = ans_map.get(q["id"], "")
        return questions



class getModuleKnowledge(tornado.web.RequestHandler):

    def _make_serializable(self, data):
        """递归清洗数据，确保所有bytes对象被转换为字符串"""
        if isinstance(data, bytes):
            # 假设bytes是UTF-8编码的文本
            return data.decode('utf-8', errors='ignore')
        elif isinstance(data, dict):
            return {key: self._make_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._make_serializable(item) for item in data]
        else:
            return data


    
    def get(self):
        
        # 查询任务数据
        try:
            module=self.get_argument("module")
            knowledges=Common.select("sangao","select * from knowledge where belong_module_id="+module)
            print(f"knowledges:{knowledges}")
            serializable_data = self._make_serializable(knowledges)
            print(f"json_data:{serializable_data}")
            # 设置JSON响应头并返回数据
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(json.dumps(serializable_data))
            
        except Exception as e:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(json.dumps({"success": False, "error": str(e)}))



class changeBatchHandler(tornado.web.RequestHandler):
    """
    处理"换一批"的AJAX请求
    """
    def get(self):
        logger.info(self.get_argument("module"))
        # 获取请求参数
        module = self.get_argument("module", "")
        question_type = self.get_argument("type", "")
        number = self.get_argument("number", "5")  # 默认每次获取5道题
        
        # 确保number是有效的数字且不超过20
        try:
            number = int(number)
            if number <= 0 or number > 20:
                number = 5
        except ValueError:
            number = 5
            
        # 根据不同的题型查询不同的题目
        single_choice_questions={}
        true_false_questions={}
        operation_questions={}
        multiple_choice_questions={}
        fill_blank_questions={}
        
        if question_type == "single_choice":
            if module == "all":
                sql = f"SELECT * FROM single_choice_question ORDER BY RANDOM() LIMIT {number}"
            else:
                sql = f"SELECT * FROM single_choice_question WHERE module='{module}' ORDER BY RANDOM() LIMIT {number}"
            single_choice_questions = Common.select("sangao", sql)
            
        elif question_type == "true_false":
            if module == "all":
                sql = f"SELECT * FROM tf_question ORDER BY RANDOM() LIMIT {number}"
            else:
                sql = f"SELECT * FROM tf_question WHERE module='{module}' ORDER BY RANDOM() LIMIT {number}"
            true_false_questions = Common.select("sangao", sql)
            
        elif question_type == "multiple_choice":
            if module == "all":
                sql = f"SELECT * FROM multiple_choice_question ORDER BY RANDOM() LIMIT {number}"
            else:
                sql = f"SELECT * FROM multiple_choice_question WHERE module='{module}' ORDER BY RANDOM() LIMIT {number}"
            multiple_choice_questions = Common.select("sangao", sql)
            
        elif question_type == "fill_blank":
            if module == "all":
                sql = f"SELECT * FROM fill_blank_question ORDER BY RANDOM() LIMIT {number}"
            else:
                sql = f"SELECT * FROM fill_blank_question WHERE module='{module}' ORDER BY RANDOM() LIMIT {number}"
            fill_blank_questions = Common.select("sangao", sql)
            
        elif question_type == "operation":
            if module == "all":
                sql = f"SELECT * FROM operation_question ORDER BY RANDOM() LIMIT {number}"
            else:
                sql = f"SELECT * FROM operation_question WHERE module='{module}' ORDER BY RANDOM() LIMIT {number}"
            operation_questions = Common.select("sangao", sql)
        
        # # 返回JSON格式的数据
        # self.set_header("Content-Type", "application/json; charset=utf-8")
        # self.write({
        #     "questions": questions,
        #     "question_type": question_type
        # })
        logger.info(f"single_choice_questions:{single_choice_questions}")
        self.render(os.path.join(config.BASE_DIR,"sangao","templates","Question","result_ajax.html"),
                    single_choice_questions=single_choice_questions,
                    true_false_questions=true_false_questions,
                    multiple_choice_questions=multiple_choice_questions,
                    fill_blank_questions=fill_blank_questions,
                    operation_questions=operation_questions,

                    question_type=question_type)



class errorRankingHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
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
        self.render("sangao/templates/Exam/error_ranking_select.html",exam_papers=exam_papers)


class singleChoiceAddHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        sql="insert into single_choice_question()"
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
        self.render("sangao/templates/Question/single_choice_add.html",exam_papers=exam_papers)


class getModuleKnowledge(tornado.web.RequestHandler):

    def _make_serializable(self, data):
        """递归清洗数据，确保所有bytes对象被转换为字符串"""
        if isinstance(data, bytes):
            # 假设bytes是UTF-8编码的文本
            return data.decode('utf-8', errors='ignore')
        elif isinstance(data, dict):
            return {key: self._make_serializable(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._make_serializable(item) for item in data]
        else:
            return data


    
    def get(self):
        
        # 查询任务数据
        try:
            module=self.get_argument("module")
            knowledges=Common.select("sangao","select * from knowledge where belong_module_id="+module)
            print(f"knowledges:{knowledges}")
            serializable_data = self._make_serializable(knowledges)
            print(f"json_data:{serializable_data}")
            # 设置JSON响应头并返回数据
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(json.dumps(serializable_data))
            
        except Exception as e:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(json.dumps({"success": False, "error": str(e)}))


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")
        else:
            #获取所有知识点
            knowledges=Common.select("sangao","select * from knowledge")
            modules = Common.select("sangao","select * from module")
            self.render(os.path.join(config.BASE_DIR,"sangao","templates","Question","select.html"),knowledges=knowledges,modules=modules)

    def post(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")        
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        print("post_data:",post_data)
        data={}
        data["module"]=self.get_argument("module")
        data["knowledge"]=self.get_argument("knowledge")
        data["difficult"]=self.get_argument("difficult")
        data["number"]=self.get_argument("number")

        single_choice_questions={}
        true_false_questions={}
        operation_questions={}
        multiple_choice_questions={}
        fill_blank_questions={}
        if self.get_argument("type")=="single_choice":
            if data["module"] == "all":
                sql = "select * from single_choice_question where difficult='" + data["difficult"] + "' order by random() limit "+data["number"]
            else:
                sql = "select * from single_choice_question where module='" + data["module"] + "' and difficult='" + data["difficult"] + "' order by random() limit "+data["number"]            
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"            

            single_choice_questions=Common.select("sangao",sql)
        if self.get_argument("type")=="true_false":
            if data["module"]=="all":
                sql="select * from tf_question"
            else:
                sql="select * from tf_question where module='"+data["module"]+"'"
            if data["knowledge"]!="所有":
                sql=sql+" and knowledge='"+data["knowledge"]+"'"  
            true_false_questions=Common.select("sangao",sql)
        if self.get_argument("type")=="operation":
            sql="select * from operation_question where difficult='"+data["difficult"]+"'"
            if data["module"]!="all":
                sql=sql+"and module='"+data["module"]+"'"
            sql=sql+" order by random() limit "+data["number"]
            operation_questions=Common.select("sangao",sql) 
        if self.get_argument("type")=="multiple_choice":
            if data["module"]=="all":
                sql="select * from multiple_choice_question"
            else:
                sql="select * from multiple_choice_question where module='"+data["module"]+"'"
            multiple_choice_questions=Common.select("sangao",sql)     
        if self.get_argument("type")=="fill_blank":
            if data["module"]=="all":
                sql="select * from fill_blank_question"
            else:
                sql="select * from fill_blank_question where module='"+data["module"]+"'"
            fill_blank_questions=Common.select("sangao",sql)  

        print("结果集multiple_choice_questions",multiple_choice_questions)                                  
        print("结果集single_choice_questions",single_choice_questions)       
        print("结果集true_false_questions",true_false_questions)
        print("结果集operation_questions",operation_questions)
        print("结果集fill_blank_questions",fill_blank_questions)
        
        self.render(os.path.join(config.BASE_DIR,"sangao","templates","Question","result.html")
        ,module=data["module"]
        ,question_type=self.get_argument("type")
        ,number=data["number"]
        ,knowledge=data["knowledge"]
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,multiple_choice_questions=multiple_choice_questions        
        ,fill_blank_questions=fill_blank_questions 
        ,single_choice_questions=single_choice_questions)

