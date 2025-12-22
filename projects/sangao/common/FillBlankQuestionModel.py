# sangao/common/FillBlankQuestionModel.py


import logging
logger = logging.getLogger(__name__)


class FillBlankQuestionModel:
    @staticmethod
    def calculate_score(student_answer, correct_answer):
        """
        对填空题进行评分
        :param student_answer: 学生答案
        :param correct_answer: 正确答案
        :return: (得分, 是否正确)
        """
        score = 0
        is_correct = 0
        
        # 将正确答案按 | 分割成多个可接受的答案选项
        acceptable_options = [option.strip().lower() for option in correct_answer.split('|')]
        
        # 检查学生答案是否在可接受的选项中
        if student_answer.strip().lower() in acceptable_options:
            score = 1
            is_correct = 1
            
        return score, is_correct