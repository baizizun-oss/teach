# sangao/common/TrueFalseQuestionModel.py


import logging
logger = logging.getLogger(__name__)


class TrueFalseQuestionModel:
    @staticmethod
    def calculate_score(student_answer, correct_answer):
        """
        对判断题进行评分
        :param student_answer: 学生答案
        :param correct_answer: 正确答案
        :return: (得分, 是否正确)
        """
        score = 0
        is_correct = 0
        
        if str(student_answer).strip() == str(correct_answer).strip():
            score = 2
            is_correct = 1
            
        return score, is_correct