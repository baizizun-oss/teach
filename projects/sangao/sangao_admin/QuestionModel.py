from common.CommonModel import Common
import sqlite3
import os
import re
from config import BASE_DIR
import logging

logger = logging.getLogger(__name__)


class SingleChoiceModel():
    @staticmethod
    def select(id=""):
        if id=="":
            sql="select * from single_choice_question"
        else:
            sql = f"select question.id as question_id,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from single_choice_question as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id = {id}"
        
        single_choice_questions = Common.select("sangao", sql)
        return single_choice_questions
    
    @staticmethod
    def add(title,choice1,choice2,choice3,choice4,answer,source,exam_year,difficult,picture,module,knowledge):
        data={}
        data["title"]=title
        data["choice1"]=choice1
        data["choice2"]=choice2
        data["choice3"]=choice3
        data["choice4"]=choice4
        data["answer"]=answer
        data["source"]=source
        data["exam_year"]=exam_year
        data["difficult"]=difficult
        data["picture"]=picture
        data["module"]=module
        data["knowledge"]=knowledge

        sql="insert into single_choice_question(title,choice1,choice2,choice3,choice4,answer,source,public_year,difficult,picture,module,knowledge) values('"+data["title"]+"','"+data["choice1"]+"','"+data["choice2"]+"','"+data["choice3"]+"','"+data["choice4"]+"','"+data["answer"]+"','"+data["source"]+"',"+str(data["exam_year"])+",'"+data["difficult"]+"','"+data["picture"]+"','"+data["module"]+"','"+data["knowledge"]+"');"
        result=Common.execute("sangao",sql)
        return result

    @staticmethod
    def get_by_id(question_id):
        """
        根据题目ID获取单选题
        :param question_id: 题目ID
        :return: 题目信息
        """
        rows = Common.select("sangao", f"SELECT * FROM single_choice_question WHERE id = {question_id}")
        return rows[0] if rows else None

    @staticmethod
    def get_correct_answer(question_id):
        """
        获取单选题的正确答案
        :param question_id: 题目ID
        :return: 正确答案
        """
        rows = Common.select("sangao", f"SELECT answer FROM single_choice_question WHERE id = {question_id}")
        return rows[0]["answer"] if rows and rows[0]["answer"] is not None else None


class MultipleChoiceModel:
    """
    多选题模型类，专注于数据库操作
    """

    @staticmethod
    def get_by_id(question_id):
        """
        根据题目ID获取多选题
        :param question_id: 题目ID
        :return: 题目信息
        """
        rows = Common.select("sangao", f"SELECT * FROM multiple_choice_question WHERE id = {question_id}")
        return rows[0] if rows else None

    @staticmethod
    def get_correct_answer(question_id):
        """
        获取多选题的正确答案
        :param question_id: 题目ID
        :return: 正确答案
        """
        rows = Common.select("sangao", f"SELECT answer FROM multiple_choice_question WHERE id = {question_id}")
        return rows[0]["answer"] if rows and rows[0]["answer"] is not None else None


class TrueFalseModel:
    """
    判断题模型类，专注于数据库操作
    """

    @staticmethod
    def get_by_id(question_id):
        """
        根据题目ID获取判断题
        :param question_id: 题目ID
        :return: 题目信息
        """
        rows = Common.select("sangao", f"SELECT * FROM tf_question WHERE id = {question_id}")
        return rows[0] if rows else None

    @staticmethod
    def get_correct_answer(question_id):
        """
        获取判断题的正确答案
        :param question_id: 题目ID
        :return: 正确答案
        """
        rows = Common.select("sangao", f"SELECT answer FROM tf_question WHERE id = {question_id}")
        return rows[0]["answer"] if rows and rows[0]["answer"] is not None else None


class FillBlankModel:
    """
    填空题模型类，专注于数据库操作
    """

    @staticmethod
    def get_by_id(question_id):
        """
        根据题目ID获取填空题
        :param question_id: 题目ID
        :return: 题目信息
        """
        rows = Common.select("sangao", f"SELECT * FROM fill_blank_question WHERE id = {question_id}")
        return rows[0] if rows else None

    @staticmethod
    def get_correct_answer(question_id):
        """
        获取填空题的正确答案
        :param question_id: 题目ID
        :return: 正确答案
        """
        rows = Common.select("sangao", f"SELECT answer FROM fill_blank_question WHERE id = {question_id}")
        return rows[0]["answer"] if rows and rows[0]["answer"] is not None else None


class OperationModel:
    """
    操作题模型类，专注于数据库操作
    """

    @staticmethod
    def get_by_id(question_id):
        """
        根据题目ID获取操作题
        :param question_id: 题目ID
        :return: 题目信息
        """
        rows = Common.select("sangao", f"SELECT * FROM operation_question WHERE id = {question_id}")
        return rows[0] if rows else None

    @staticmethod
    def get_correct_answer(question_id):
        """
        获取操作题的正确答案
        :param question_id: 题目ID
        :return: 正确答案
        """
        rows = Common.select("sangao", f"SELECT answer FROM operation_question WHERE id = {question_id}")
        return rows[0]["answer"] if rows and rows[0]["answer"] is not None else None


class KnowledgeModel():
    @staticmethod
    def select(id=""):
        if id=="":
            sql="select * from knowledge"
        else:
            sql=f"select * from knowledge where id={id}"
        knowledge=Common.select("sangao",sql)
        return knowledge