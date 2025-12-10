# sangao/AnswerController.py
import tornado.web
import sqlite3
import time
import json
import myportal.common as common
import logging
import os

logger = logging.getLogger(__name__)

DB_PATH = "your_database_path.db"  # 请替换为实际数据库路径，或从 config 引入


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 支持 dict-like 访问
    return conn




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