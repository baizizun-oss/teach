#sangao_admin/SingleChoiceAnswerModel.py
from common.CommonModel import Common
import logging
logger = logging.getLogger(__name__)


#单独一道题的作答模型
class OperationAnswerModel:
    score = 0
    is_correct = 0
    user_answer=""

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
    

    

    def __init__(self, answer_id):
        if answer_id is None :
            return
        sql = """
            select question.id as question_id
            ,question.material as material 
            ,question.material2 as material2
            ,question.picture as picture
            ,question.answer as correct_answer
            ,question.title as title
            ,question.module as module_id
            ,question.score_rules as score_rules
            ,question.knowledge as knowledge_id
            ,knowledge.name as knowledge_name
            ,module.name as module_name
            ,knowledge.name as knowledge_name
            ,question.difficult as difficult
            ,student_answer.score as score
            from operation_question as question join module on module.id = question.module join knowledge on knowledge.id = question.knowledge join student_answer on student_answer.question_id = question.id where student_answer.id=?
            """
        answer=Common.find("sangao",sql,(answer_id))
        self.question_id = answer["question_id"]
        self.material_path = answer["material"]
        self.picture = answer["picture"]
        self.correct_answer = answer["correct_answer"]
        self.title = answer["title"]
        self.module_id = answer["module_id"]
        self.score_rules = answer["score_rules"]
        self.material2 = answer["material2"]
        self.knowledge_id = answer["knowledge_id"]
        self.knowledge_name = answer["knowledge_name"]
        self.difficult = answer["difficult"]
        self.score = answer["score"]