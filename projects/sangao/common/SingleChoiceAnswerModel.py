#sangao_admin/SingleChoiceAnswerModel.py
from common.CommonModel import Common
from SingleChoiceQuestionModel import SingleChoiceQuestionModel
import logging
logger = logging.getLogger(__name__)


#单独一道题的作答模型
class SingleChoiceAnswerModel:
    score = 0
    is_correct = 0
    user_answer=""
    correct_answer=""

    @staticmethod
    def calculate_score(student_answer, correct_answer):
        """
        对单选题进行评分
        :param student_answer: 学生答案
        :param correct_answer: 正确答案
        :return: (得分, 是否正确)
        """
        
        if str(student_answer).strip() == str(correct_answer).strip():
            score = 2
            is_correct = 1
            
        return score, is_correct
    
    def get_question(id=None):
        if id==None:
            sql="select * from single_choice_question"
        else:
            sql="select * from single_choice_question where id="+str(id)
        return Common.select("sangao",sql)
    

