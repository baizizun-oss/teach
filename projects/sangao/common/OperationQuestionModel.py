# sangao/common/OperationQuestionModel.py

import logging
import os
import config
from common.CommonModel import Common

logger = logging.getLogger(__name__)





class OperationQuestionModel:

    score=15
    title=""
    material_path=""
    module_id=0
    question_id=0
    knowledge_id=0
    picture=""
    correct_answer=""
    score_rules= ""

    def __init__(self, question_id):
        if question_id is None:
            return
        sql = """
            select question.id as id
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

            from operation_question as question  join module on module.id = question.module join knowledge on knowledge.id = question.knowledge where question.id=?
            """
        question=Common.find("sangao",sql,(question_id,))
        self.question_id = question["id"]
        self.material_path = question["material"]
        self.picture = question["picture"]
        self.correct_answer = question["correct_answer"]
        self.title = question["title"]
        self.module_id = question["module_id"]
        self.score_rules = question["score_rules"]
        self.material2 = question["material2"]
        self.knowledge_id = question["knowledge_id"]
        self.knowledge_name = question["knowledge_name"]
        self.difficult = question["difficult"]
  
  
    def to_dict(self):
        return {
            "question_id": self.question_id,
            "title": self.title,
            "material": self.material_path,
            "material2": self.material2,
            "picture": self.picture,
            "correct_answer": self.correct_answer,
            "module_id": self.module_id,
            "knowledge_id": self.knowledge_id,
            "score_rules": self.score_rules,
            "knowledge_name":self.knowledge_name,
            "difficult":self.difficult
        }

