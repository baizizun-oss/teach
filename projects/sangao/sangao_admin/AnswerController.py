# sangao_admin/AnswerController.py
import tornado.web
import sqlite3
import myportal.common as common
import logging
import os
from tornado.web import HTTPError
import config


logger = logging.getLogger(__name__)




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

                sql = "select student_answer.question_id as question_id ,student_answer.question_type as question_type, student_answer.user_answer as student_answer,question.answer as question_answer,student_answer.student_id,question.title as question_title from student_answer join single_choice_question as question on question.id = student_answer.question_id where question.id= "+str(vo["question_id"])
                student_answer = common.select("sangao",sql)
                #将试题内容和类型保存在错题统计字典中
                if not single_choice_error_stats[vo["question_id"]]["question_title"]:
                    single_choice_error_stats[vo["question_id"]]["question_title"]=student_answer[0]["question_title"]
                # print("同一题的记录：",student_answer)
                if vo["user_answer"] != student_answer[0]["question_answer"]:
                    error_question.append(vo)
                    # #做错此题的人数加1
                    single_choice_error_stats[vo["question_id"]]["error_sum"]+=1
                    # print("single_choice:",single_choice_error_stats[vo["question_id"]])
            if vo["question_type"] == "true_false":
                #同样的，做过的+1
                tf_error_stats.setdefault(vo["question_id"],{"answer_sum":0,"error_sum":0,"question_type":"判断","question_title":""})
                tf_error_stats[vo["question_id"]]["answer_sum"]+=1
                sql = "select student_answer.question_id as question_id ,student_answer.question_type as question_type, student_answer.user_answer as student_answer,question.answer as question_answer,student_answer.student_id,question.title as question_title from student_answer join tf_question as question on question.id = student_answer.question_id where question.id= "+str(vo["question_id"]) 
                student_answer = common.select("sangao",sql)
                #将试题内容和类型保存在错题统计字典中
                if not tf_error_stats[vo["question_id"]]["question_title"]:
                    tf_error_stats[vo["question_id"]]["question_title"]=student_answer[0]["question_title"]
                #print("同一题的记录：",student_answer)                
                if vo["user_answer"] != student_answer[0]["question_answer"]:
                    error_question.append(vo)  
                    #错过的+1
                    # ++true_false_error_sum[student_answer["question_id"]]
                    tf_error_stats[vo["question_id"]]["error_sum"]+=1

        #两个统计字典合并
        merged_stats={}
        merged_stats.update({f"single_choice:{k}":v for k,v in single_choice_error_stats.items()})
        merged_stats.update({f"tf:{k}": v for k,v in tf_error_stats.items()})
        # print("合并后的字典：",merged_stats)
        #排序
        sorted_stats = sorted(merged_stats.items(),key= lambda x:(x[1]["answer_sum"],x[1]["error_sum"]/x[1]["answer_sum"]),reverse=True)
        # print("排序后的列表",sorted_stats)
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Answer","error_ranking_list.html"),
                    error_ranking= sorted_stats
                    )




class indexHandler(tornado.web.RequestHandler):

    #由于直接从数据库中取出错题信息（包括谁错的，哪道题，错误答案是啥，同错的有多少人，错误率多少（同错的人数除以做过的人数））比较复杂，可以分为两步来做。先将错题都取出来，再统计。由于处理麻烦，暂时不将操作题加入到错题中
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"sangao_admin","templates","Answer","index.html"))