#sangao_admin/SingleChoiceQuestionModel.py
from common.CommonModel import Common
import logging
logger = logging.getLogger(__name__)


#单独一道选择题的model
class SingleChoiceQuestionModel:
    correct_answer=""
    choice1=""
    choice2=""
    choice3=""
    choice4=""
    title=""
    module=""
    knowledge=""
    question_id=""
    def __init__(self,question_id):
        sql="select * from single_choice_question where id="+str(question_id)
        question=Common.find("sangao",sql)
        self.correct_answer
    def get_question():

        sql="select * from single_choice_question where id="+str(id)
        return Common.select("sangao",sql)
    

