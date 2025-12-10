# sangao/AnswerController.py
import tornado.web
import sqlite3
import time
import json
import myportal.common as common
import logging
import os
import uuid
import re

logger = logging.getLogger(__name__)

DB_PATH = "your_database_path.db"  # 请替换为实际数据库路径，或从 config 引入


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 支持 dict-like 访问
    return conn

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



class practiceAddHandler(tornado.web.RequestHandler):

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
            upload_dir = os.path.join(common.BASE_DIR, "sangao", "templates", "Question", "upload")
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
            correct_ans = self.get_correct_answer("sangao", qtype, qid)
            if correct_ans is None:
                logger.error(f"未找到标准答案: 题目ID={qid}, 类型={qtype}")
                continue

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

            common.execute("sangao", """
                INSERT INTO student_answer(
                    student_id, question_id, user_answer, ctime, question_type, 
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
            upload_dir = os.path.join(common.BASE_DIR, "sangao", "templates", "Question", "upload")
            for question in questions:
                try:
                    with open(os.path.join(upload_dir, question["student_answer"]), 'r', encoding='utf-8') as f:
                        question["student_code"] = f.read()
                except:
                    question["student_code"] = ""
                question["correct_code"] = question["answer"]



        self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("提交成功!请去“我的作答”中查看作答情况");</script></body></html>') 


    def get_correct_answer(self, db_name, question_type, question_id):
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

        rows = common.select(db_name, f"SELECT answer FROM {table} WHERE id ={question_id}")
        return rows[0]["answer"] if rows and rows[0]["answer"] is not None else None

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
        questions = common.select("sangao", f"SELECT * FROM {table} WHERE id IN ({qids_str})")
        logger.info(f"获取题目: {questions}")
        # 获取学生答案
        student_id = self.get_cookie("user_id")
        student_answers = common.select("sangao", f"""
            SELECT question_id, user_answer AS student_answer 
            FROM student_answer 
            WHERE question_id IN ({qids_str}) AND student_id = '{student_id}'
            ORDER BY ctime DESC
        """)

        ans_map = {row["question_id"]: row["student_answer"] for row in student_answers}
        for q in questions:
            q["student_answer"] = ans_map.get(q["id"], "")
        return questions

        


class practiceListHandler(tornado.web.RequestHandler):
    def get(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return

        sql="select submission_id,ctime,sum(score) as total_score from student_answer where student_id="+self.get_cookie("user_id") + " and source='practice' group by submission_id order by ctime"
        practice_historys= common.select("sangao",sql)
        for key in range(len(practice_historys)):
            if practice_historys[key]["total_score"] is None:
                practice_historys[key]["total_score"]="未批改"
            practice_historys[key]["ctime"] = time.strftime('%Y-%m-%d %H:%M',time.localtime(practice_historys[key]["ctime"]))
        self.render(
            os.path.join(common.BASE_DIR, "sangao", "templates", "Answer", "practice_list.html"),
            practice_historys = practice_historys
        )

class practiceDetailHandler(tornado.web.RequestHandler):
    def get(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return
        single_choice_sql="select * from student_answer join single_choice_question on single_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'single_choice'"
        single_choice_answers=common.select("sangao",single_choice_sql)
        multiple_choice_sql="select * from student_answer join multiple_choice_question on multiple_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'multiple_choice'"
        multiple_choice_answers = common.select("sangao",multiple_choice_sql)
        tf_sql="select * from student_answer join tf_question on tf_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'true_false'"
        tf_answers=common.select("sangao",tf_sql)
        for key in range(len(tf_answers)):
            if tf_answers[key]["user_answer"]=="right":
                tf_answers[key]["user_answer"]="对"
            if tf_answers[key]["user_answer"]=="wrong":
                tf_answers[key]["user_answer"]="错"


        fill_blank_sql="select * from student_answer join fill_blank_question on fill_blank_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'fill_blank'"
        fill_blank_answers=common.select("sangao",fill_blank_sql)        
        operation_sql="select * from student_answer join operation_question on operation_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'operation'"
        operation_answers=common.select("sangao",operation_sql)            

        logger.info(f"single:{single_choice_answers}")
        logger.info(f"multiple:{multiple_choice_answers}")
        logger.info(f"tf:{tf_answers}")
        self.render(os.path.join(common.BASE_DIR,"sangao","templates","Answer","practice_detail.html"),
                    single_choice_answers=single_choice_answers,
                    multiple_choice_answers=multiple_choice_answers,
                    tf_answers=tf_answers,
                    fill_blank_answers=fill_blank_answers,
                    operation_answers=operation_answers
                    
                    )

class HistoryHandler(tornado.web.RequestHandler):
    """查询某题的历史作答记录（用于错题本、复习）"""
    def get(self):
        student_id = self.get_argument("student_id")
        question_id = self.get_argument("question_id", None)

        conn = get_db()
        cursor = conn.cursor()

        if question_id:
            cursor.execute("""
                SELECT id, answer, is_correct, ctime, source, duration_seconds, exam_paper_id
                FROM student_answer
                WHERE student_id = ? AND question_id = ?
                ORDER BY ctime DESC
            """, (student_id, question_id))
        else:
            # 查询所有作答（可分页）
            cursor.execute("""
                SELECT id, question_id, question_type, answer, is_correct, ctime, source
                FROM student_answer
                WHERE student_id = ?
                ORDER BY ctime DESC
                LIMIT 100
            """, (student_id,))

        records = [dict(row) for row in cursor.fetchall()]
        for r in records:
            try:
                r["answer"] = json.loads(r["answer"])
            except:
                pass

        conn.close()
        self.write({"code": 200, "data": records})




class examListHandler(tornado.web.RequestHandler):
    """查询某次考试的所有作答（用于教师查看学生答卷）"""
    def get(self):
        student_id=self.get_cookie("user_id",None)
        conn = get_db()
        cursor = conn.cursor()

        if student_id:
            # 查某学生在某试卷的作答
            # cursor.execute("""
            #     SELECT sa.*, q.title
            #     FROM student_answer sa
            #     LEFT JOIN (
            #         SELECT id, title FROM single_choice_question
            #         UNION ALL
            #         SELECT id, title FROM multiple_choice_question
            #         UNION ALL
            #         SELECT id, title FROM fill_blank_question
            #         UNION ALL
            #         SELECT id, title FROM operation_question
            #         UNION ALL
            #         SELECT id, title FROM tf_question
            #     ) q ON sa.question_id = q.id
            #     WHERE sa.exam_paper_id = ? AND sa.student_id = ?
            #     ORDER BY sa.ctime
            # """, (exam_paper_id, student_id))
            sql="select sum(score) as total_score,submission_id,exam_paper.title as exam_paper_title,student_answer.ctime as student_answer_ctime from student_answer join exam_paper on exam_paper.id = student_answer.exam_paper_id where student_id="+student_id+" and source='exam' group by submission_id order by student_answer_ctime"
            student_answer = common.select("sangao",sql)
            for key in range(len(student_answer)):
                student_answer[key]["student_answer_ctime"]=time.strftime('%Y-%m-%d %H:%M',time.localtime(student_answer[key]["student_answer_ctime"]))
            logger.info(f"student_answer:{student_answer}")
            self.render(os.path.join(common.BASE_DIR,"sangao","templates","Answer","exam_lists.html"),
                        student_answer= student_answer
                        )
        else:
            # 查该试卷所有学生的作答（汇总）
            # cursor.execute("""
            #     SELECT sa.student_id, u.nickname, COUNT(*) as total,
            #            SUM(sa.is_correct) as correct_count
            #     FROM student_answer sa
            #     JOIN user u ON sa.student_id = u.id
            #     WHERE sa.exam_paper_id = ?
            #     GROUP BY sa.student_id
            # """, (exam_paper_id,))
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")
        # data = [dict(row) for row in cursor.fetchall()]
        # conn.close()
        # self.write({"code": 200, "data": data})







class listHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao","templates","Answer","list.html"))



class examDetailHandler(tornado.web.RequestHandler):
    def get(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return
        single_choice_sql="select * from student_answer join single_choice_question on single_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'single_choice'"
        single_choice_answers=common.select("sangao",single_choice_sql)
        multiple_choice_sql="select * from student_answer join multiple_choice_question on multiple_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'multiple_choice'"
        multiple_choice_answers = common.select("sangao",multiple_choice_sql)
        tf_sql="select * from student_answer join tf_question on tf_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'true_false'"
        tf_answers=common.select("sangao",tf_sql)
        for key in range(len(tf_answers)):
            if tf_answers[key]["user_answer"]=="right":
                tf_answers[key]["user_answer"]="对"
            if tf_answers[key]["user_answer"]=="wrong":
                tf_answers[key]["user_answer"]="错"


        fill_blank_sql="select * from student_answer join fill_blank_question on fill_blank_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'fill_blank'"
        fill_blank_answers=common.select("sangao",fill_blank_sql)        
        operation_sql="select * from student_answer join operation_question on operation_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'operation'"
        operation_answers=common.select("sangao",operation_sql)            

        logger.info(f"single:{single_choice_answers}")
        logger.info(f"multiple:{multiple_choice_answers}")
        logger.info(f"tf:{tf_answers}")
        self.render(os.path.join(common.BASE_DIR,"sangao","templates","Answer","practice_detail.html"),
                    single_choice_answers=single_choice_answers,
                    multiple_choice_answers=multiple_choice_answers,
                    tf_answers=tf_answers,
                    fill_blank_answers=fill_blank_answers,
                    operation_answers=operation_answers
                    
                    )