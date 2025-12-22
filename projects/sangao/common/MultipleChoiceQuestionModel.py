# sangao/common/MultipleChoiceQuestionModel.py


import logging
logger = logging.getLogger(__name__)


class MultipleChoiceQuestionModel:
    @staticmethod
    def calculate_score(student_answer, correct_answer):
        """
        对多选题进行评分
        :param student_answer: 学生答案
        :param correct_answer: 正确答案
        :return: (得分, 是否正确)
        """
        score = 0
        is_correct = 0
        
        def sort_choices(choice_string):
            """
            对选项进行排序处理
            :param choice_string: 选项字符串
            :return: 排序后的选项字符串
            """
            return ','.join(sorted([x.strip().upper() for x in choice_string.split(',') if x.strip()])) if choice_string else ""
        
        if sort_choices(student_answer) == sort_choices(correct_answer):
            score = 4
            is_correct = 1
            
        return score, is_correct