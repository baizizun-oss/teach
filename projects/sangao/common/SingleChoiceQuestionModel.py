#common/SingleChoiceQuestionModel.py
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
        sql="""
            select question.id as question_id, 
            question.choice1 as choice1,
            question.choice2 as choice2,
            question.choice3 as choice3,
            question.choice4 as choice4,
            question.answer as correct_answer,
            question.picture as picture,
            question.explain as explain,
            question.module as module_id,
            question.knowledge as knowledge_id,
            module.name as module_name,
            knowledge.name as knowledge_name,
            question.difficult as difficult,
            question.score as max_score,
            question.source as source_id,
            question_source.publicer as source_name,
            question_source.public_year as public_year,
            question.title as title
            from single_choice_question as question join module on module.id=question.module join knowledge on knowledge.id=question.knowledge join question_source on question_source.id=question.source where question.id=?
        """
        question=Common.find("sangao",sql,(question_id,))
        if question is None:
            return None        
        self.correct_answer = question["correct_answer"]
        self.choice1=question["choice1"]
        self.choice2=question["choice2"]
        self.choice3=question["choice3"]
        self.choice4=question["choice4"]
        self.picture=question["picture"]
        self.question_id=question["question_id"]
        self.explain=question["explain"]
        self.module_id=question["module_id"]
        self.module_name=question["module_name"]
        self.knowledge_id = question["knowledge_id"]
        self.knowledge_name = question["knowledge_name"]
        self.difficult = question["difficult"]
        self.max_score= question["max_score"]
        self.source_id = question["source_id"]
        self.source_name = question["source_name"]
        self.public_year = question["public_year"]
        self.title = question["title"]

    

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "title": self.title,
            "choice1":self.choice1,
            "choice2":self.choice2,
            "choice3":self.choice3,
            "choice4":self.choice4,
            "picture": self.picture,
            "correct_answer": self.correct_answer,
            "module_id": self.module_id,
            "knowledge_id": self.knowledge_id,
            "knowledge_name":self.knowledge_name,
            "difficult":self.difficult,
            "max_score":self.max_score,
            "module_name":self.module_name,
            "publicer":self.source_name,
            "source_id":self.source_id,
            "public_year":self.public_year,
            "explain":self.explain
            
        }

