from common.CommonModel import Common
import sqlite3
import os
from config import BASE_DIR

class SingleChoiceModel():
    def select(id=""):
        if id=="":
            sql="select * from single_choice_question"
        else:
            sql="select * from single_choice_question where id="+id
            sql = "select question.id as question_id,question.picture as picture,question.choice1 as choice1,question.choice2 as choice2,question.choice3 as choice3,question.choice4 as choice4,question.title as title,question.answer as answer,question.knowledge as knowledge,module.name as module_name,question.module as module_id,question.knowledge as knowledge_id,knowledge.name as knowledge_name from single_choice_question as question join module on module.id = question.module join knowledge on knowledge.id= question.knowledge  where question.id ="+id
        
        
        
        single_choice_questions=Common.select("sangao",sql)
        conn=sqlite3.connect(os.path.join(BASE_DIR,"db","sangao.db"))
        cursor=conn.cursor()
        result=cursor.execute(sql)
        conn.commit()
        resultset= cursor.fetchall()        
        
        return single_choice_questions
    
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
    

        

class KnowledgeModel():
    def select(id=""):
        if id=="":
            sql="select * from knowledge"
        else:
            sql="select * from knowledge where id="+id
        knowledge=Common.select("sangao",sql)
        return knowledge