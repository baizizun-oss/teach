from common.CommonModel import Common
import logging

logger = logging.getLogger(__name__)


class SingleChoiceQuestionModel:
    """
    单选题模型类，专注于数据库操作
    """

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


class MultipleChoiceQuestionModel:
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


class TrueFalseQuestionModel:
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


class FillBlankQuestionModel:
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


class OperationQuestionModel:
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