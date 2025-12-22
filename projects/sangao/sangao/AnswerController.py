# sangao/AnswerController.py
import tornado
import sqlite3
import time
import os
import json
import logging
import xml.etree.ElementTree as ET
from common.CommonModel import Common
import config
from .AnswerService import SingleChoiceScorer, MultipleChoiceScorer, FillBlankScorer, TrueFalseScorer
from common.SingleChoiceQuestionModel import SingleChoiceQuestionModel
from common.OperationQuestionModel import OperationQuestionModel
import sangao.AnswerService as AnswerService

logger = logging.getLogger(__name__)



class practiceAddHandler(tornado.web.RequestHandler):
    def post(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return

        if self.get_argument("type")=="single_choice":
            logger.info(f"单选题：{self.get_body_arguments('question_id')}")
            for question_id in self.get_body_arguments("question_id"):
                question = SingleChoiceQuestionModel.get_question(question_id)
                
        if self.get_argument("type")=="multiple_choice":
            pass

        if self.get_argument("type")=="fill_blank":
            pass

        if self.get_argument("type")=="true_false":
            pass

        if self.get_argument("type")=="operation":
            logger.info(f"操作题：{self.get_body_arguments('question_id')}")
            logger.info(f"file:{self.request.files}")
            for key in range(len(self.get_body_arguments("question_id"))):
                #根据前端获取的question_id，获取题目信息
                Question = OperationQuestionModel(self.get_body_arguments("question_id")[key])
                logger.info(f"answer:{Question.correct_answer}")
                #调用上传文件保存函数获取保存的文件名（文件路径在config中配置过了）
                filename=AnswerService.get_upload_filepath(self.request.files.get("file")[key],user_id,Question.question_id)
                #调用计算分数函数
                score,score_details = AnswerService.calculateScore(filename, Question.question_id, Question.correct_answer)
                logger.info(f"score:{score},score_detail:{score_details}")
                #调用获取提交id函数
                submission_id=AnswerService.get_submission_id()
                Common.execute("sangao", "insert into student_answer (student_id,question_id,question_type,user_answer,score,score_details,ctime,submission_id) values (?,?,?,?,?,?,?,?)", 
                               (user_id, Question.question_id, "operation", filename, score, json.dumps(score_details), int(time.time()), submission_id))
                

class practiceListHandler(tornado.web.RequestHandler):
    def get(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return

        sql="select submission_id,ctime,sum(score) as total_score from student_answer where student_id="+self.get_cookie("user_id") + " and source='practice' group by submission_id order by ctime desc"
        practice_historys= Common.select("sangao",sql)
        for key in range(len(practice_historys)):
            if practice_historys[key]["total_score"] is None:
                practice_historys[key]["total_score"]="未批改"
            practice_historys[key]["ctime"] = time.strftime('%Y-%m-%d %H:%M',time.localtime(practice_historys[key]["ctime"]))
        self.render(
            os.path.join(config.BASE_DIR, "sangao", "templates", "Answer", "practice_list.html"),
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
        single_choice_answers=Common.select("sangao",single_choice_sql)
        multiple_choice_sql="select * from student_answer join multiple_choice_question on multiple_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'multiple_choice'"
        multiple_choice_answers = Common.select("sangao",multiple_choice_sql)
        tf_sql="select * from student_answer join tf_question on tf_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'true_false'"
        tf_answers=Common.select("sangao",tf_sql)
        for key in range(len(tf_answers)):
            if tf_answers[key]["user_answer"]=="right":
                tf_answers[key]["user_answer"]="对"
            if tf_answers[key]["user_answer"]=="wrong":
                tf_answers[key]["user_answer"]="错"


        fill_blank_sql="select * from student_answer join fill_blank_question on fill_blank_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'fill_blank'"
        fill_blank_answers=Common.select("sangao",fill_blank_sql)        
        operation_sql="select * from student_answer join operation_question on operation_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'operation'"
        operation_answers=Common.select("sangao",operation_sql)            

        # logger.info(f"single:{single_choice_answers}")
        # logger.info(f"multiple:{multiple_choice_answers}")
        # logger.info(f"tf:{tf_answers}")



        
        self.render(os.path.join(config.BASE_DIR,"sangao","templates","Answer","practice_detail.html"),
                    single_choice_answers=single_choice_answers,
                    multiple_choice_answers=multiple_choice_answers,
                    tf_answers=tf_answers,
                    fill_blank_answers=fill_blank_answers,
                    operation_answers=operation_answers
                    
                    )


class questionAnswerDetailHandler(tornado.web.RequestHandler):
    def get(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return
        if self.get_argument("question_type")=="operation":
            submission_id = self.get_argument("submission_id")
            question_type = self.get_argument("question_type")
            question_id = self.get_argument("question_id")
            
            operation_sql = """SELECT * FROM student_answer 
                              JOIN operation_question ON operation_question.id = student_answer.question_id 
                              WHERE submission_id=? AND question_type=? AND question_id=?"""
                              
            operation_answer = Common.find("sangao", operation_sql, (submission_id, question_type, question_id))
            
            # 如果有评分详情，将其添加到operation_answer中
            if operation_answer and operation_answer.get("score_details"):
                try:
                    import json
                    operation_answer["scoring_details"] = json.loads(operation_answer["score_details"])
                except Exception as e:
                    logger.error(f"解析评分详情失败: {e}")

            self.render(os.path.join(config.BASE_DIR,"sangao","templates","Answer","operation_answer_detail.html"),
                        operation_answer=operation_answer
                        )

import os
import urllib.parse
from tornado.web import HTTPError
import config

class downloadFileHandler(tornado.web.RequestHandler):
    def get(self):
        # 获取参数
        filename = self.get_argument("filename", None)
        file_type = self.get_argument("type", "answer")  # answer / material

        if not filename:
            raise HTTPError(400, "缺少文件名")

        # 安全校验：防止路径穿越（非常重要！）
        filename = os.path.basename(filename)  # 只取文件名，去掉路径
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPError(403, "非法文件名")

        # 根据 type 决定目录
        if file_type == "answer":
            base_dir = config.get_path("sangao","Question","files","operation")
        elif file_type == "material":
            base_dir = os.path.join(config.BASE_DIR, "sangao", "static_operation_question_files")
        else:
            raise HTTPError(400, "未知文件类型")

        file_path = os.path.join(base_dir, filename)

        if not os.path.exists(file_path):
            raise HTTPError(404, "文件不存在")

        # 设置响应头：强制下载 + 正确编码文件名
        # 对中文文件名进行 URL 编码（兼容 Safari、IE）
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header(
            'Content-Disposition',
            f'attachment; filename="{encoded_filename}"; filename*=UTF-8\'\'{encoded_filename}'
        )

        # 发送文件
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(8192)
                if not data:
                    break
                self.write(data)
        self.finish()


class errorQuestionHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        print(sql)
        conn = sqlite3.connect(os.path.join(config.BASE_DIR,"db","sangao.db"))
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
        student_answers=Common.select("sangao",sql)
        for vo in student_answers:
            if vo["question_type"]=="single_choice":
                #做过的加1
                single_choice_error_stats.setdefault(vo["question_id"],{"answer_sum":0,"error_sum":0,"question_type":"单选","question_title":""})
                single_choice_error_stats[vo["question_id"]]["answer_sum"]+=1

                sql = "select student_answer.question_id as question_id ,student_answer.question_type as question_type, student_answer.answer as student_answer,question.answer as question_answer,student_answer.student_id,question.title as question_title from student_answer join single_choice_question as question on question.id = student_answer.question_id where question.id= "+str(vo["question_id"])
                student_answer = Common.select("sangao",sql)
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
                student_answer = Common.select("sangao",sql)
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
            sql="select sum(score) as total_score,submission_id,exam_paper.title as exam_paper_title,student_answer.ctime as student_answer_ctime from student_answer join exam_paper on exam_paper.id = student_answer.exam_paper_id where student_id="+student_id+" and source='exam' group by submission_id order by student_answer_ctime deasc"
            student_answer = Common.select("sangao",sql)
            for key in range(len(student_answer)):
                student_answer[key]["student_answer_ctime"]=time.strftime('%Y-%m-%d %H:%M',time.localtime(student_answer[key]["student_answer_ctime"]))
            logger.info(f"student_answer:{student_answer}")
            self.render(os.path.join(config.BASE_DIR,"sangao","templates","Answer","exam_lists.html"),
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


class examDetailHandler(tornado.web.RequestHandler):
    """考试作答详情页面"""
    def get(self):
        # 检查登录状态
        user_id = self.get_cookie("user_id")
        if not user_id:
            self.write("未登录，请先<a href='/sangao/Index/login'>登录</a>！")
            return
        single_choice_sql="select * from student_answer join single_choice_question on single_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'single_choice'"
        single_choice_answers=Common.select("sangao",single_choice_sql)
        multiple_choice_sql="select * from student_answer join multiple_choice_question on multiple_choice_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'multiple_choice'"
        multiple_choice_answers = Common.select("sangao",multiple_choice_sql)
        tf_sql="select * from student_answer join tf_question on tf_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'true_false'"
        tf_answers=Common.select("sangao",tf_sql)
        for key in range(len(tf_answers)):
            if tf_answers[key]["user_answer"]=="right":
                tf_answers[key]["user_answer"]="对"
            if tf_answers[key]["user_answer"]=="wrong":
                tf_answers[key]["user_answer"]="错"


        fill_blank_sql="select * from student_answer join fill_blank_question on fill_blank_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'fill_blank'"
        fill_blank_answers=Common.select("sangao",fill_blank_sql)        
        operation_sql="select * from student_answer join operation_question on operation_question.id = student_answer.question_id where submission_id='"+self.get_argument("submission_id") + "' and question_type = 'operation'"
        operation_answers=Common.select("sangao",operation_sql)            

        logger.info(f"single:{single_choice_answers}")
        logger.info(f"multiple:{multiple_choice_answers}")
        logger.info(f"tf:{tf_answers}")
        self.render(os.path.join(config.BASE_DIR,"sangao","templates","Answer","exam_detail.html"),
                    single_choice_answers=single_choice_answers,
                    multiple_choice_answers=multiple_choice_answers,
                    tf_answers=tf_answers,
                    fill_blank_answers=fill_blank_answers,
                    operation_answers=operation_answers
                    )