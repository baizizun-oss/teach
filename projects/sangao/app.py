#app.py
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

import config
import sangao.DesignController
import sangao.IndexController
import sangao.ExamController
import sangao.TeachController
import sangao.NoteController
import sangao.QuestionController
import sangao.FileController

import sangao_admin.DesignController
import sangao_admin.IndexController
import sangao_admin.ExamController
import sangao_admin.QuestionController
import sangao_admin.TeachController
import sangao_admin.QuestionController
import sangao_admin.UserController
import sangao_admin.KnowledgeController
import sangao_admin.RecordController
import sangao.RecordController
import sangao.AnswerController
import sangao_admin.TeachExamController

import myportal.common as common
from tornado.web import StaticFileHandler
import config

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)



if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', sangao.IndexController.loginHandler)
        , (r'/sangao', sangao.IndexController.loginHandler)
        , (r'/sangao/Index/login', sangao.IndexController.loginHandler)
        , (r'/sangao/Index/register', sangao.IndexController.registerHandler)
        , (r'/sangao/Design/edit', sangao.DesignController.editHandler)
        , (r'/sangao/Exam/exam_paper_lists', sangao.ExamController.examPaperListsHandler)
        , (r'/sangao/Exam/edit', sangao.ExamController.editHandler)
        , (r'/sangao/Exam/handin', sangao.ExamController.handinHandler)
        , (r'/sangao/Exam/exam_paper_add', sangao.ExamController.examPaperAddHandler)
        , (r'/sangao/Exam/exam_paper_edit', sangao.ExamController.examPaperEditHandler)            
        , (r'/sangao/Exam/exam_paper_del', sangao.ExamController.examPaperDelHandler)
        , (r'/sangao/Exam/error_ranking', sangao.ExamController.errorRankingHandler)
        , (r'/sangao/File/list', sangao.FileController.listHandler)
        , (r'/sangao/File/lists', sangao.FileController.listsHandler)
        , (r'/sangao/File/add', sangao.FileController.addHandler)
        , (r'/sangao/File/del', sangao.FileController.delHandler)
        , (r'/sangao/File/setPublic', sangao.FileController.setPublicHandler)
        , (r'/sangao/File/setPrivate', sangao.FileController.setPrivateHandler)
        , (r'/sangao/Teach/list', sangao.TeachController.listHandler)
        , (r'/sangao/Design/lists', sangao.DesignController.listsHandler)
        , (r'/sangao/Design/add', sangao.DesignController.addHandler)
        , (r'/sangao/Design/del', sangao.DesignController.delHandler)
        , (r'/sangao/Note/doubleEdit', sangao.NoteController.doubleEditHandler)
        , (r'/sangao/Note/edit', sangao.NoteController.editHandler)
        , (r'/sangao/Note/select', sangao.NoteController.selectHandler)
        , (r'/sangao/Note/doubleAdd', sangao.NoteController.doubleAddHandler)
        , (r'/sangao/Note/add', sangao.NoteController.addHandler)
        , (r'/sangao/Note/index', sangao.NoteController.indexHandler)
        , (r'/sangao/Note/detail', sangao.NoteController.detailHandler)
        , (r'/sangao/Question/select', sangao.QuestionController.selectHandler)
        , (r'/sangao/Question/add', sangao.QuestionController.addHandler)
        , (r'/sangao/Question/lists', sangao.QuestionController.listsHandler)
        , (r'/sangao/Question/handin', sangao.QuestionController.handinHandler)
        , (r'/sangao/Question/get_module_knowledge', sangao.QuestionController.getModuleKnowledge)
        , (r'/sangao/Question/change_batch', sangao.QuestionController.changeBatchHandler) 
        , (r'/sangao/Answer/practice_list', sangao.AnswerController.practiceListHandler)
        , (r'/sangao/Answer/practice_add', sangao.AnswerController.practiceAddHandler)
        , (r'/sangao/Answer/history', sangao.AnswerController.HistoryHandler)
        , (r'/sangao/Answer/exam_list', sangao.AnswerController.examListHandler)      
        , (r'/sangao/Answer/list', sangao.AnswerController.practiceListHandler)    
        , (r'/sangao/Answer/practice_detail', sangao.AnswerController.practiceDetailHandler)
        , (r'/sangao/Answer/question_answer_detail', sangao.AnswerController.questionAnswerDetailHandler)
        , (r'/sangao/Answer/download', sangao.AnswerController.downloadFileHandler)   
        , (r'/sangao/Answer/exam_detail', sangao.AnswerController.examDetailHandler)   
        , (r'/sangao/Record/lists', sangao.RecordController.listsHandler)
        , (r'/sangao/Record/detail', sangao.RecordController.detailHandler)
        , (r'/sangao_admin', sangao_admin.IndexController.indexHandler)
        , (r'/sangao_admin/login', sangao_admin.IndexController.loginHandler)
        , (r'/sangao_admin/index', sangao_admin.IndexController.indexHandler)
        , (r'/sangao_admin/TeachExam/question_lists', sangao_admin.TeachExamController.questionListsHandler)
        , (r'/sangao_admin/TeachExam/question_detail', sangao_admin.TeachExamController.questionDetailHandler)
        , (r'/sangao_admin/TeachExam/question_add', sangao_admin.TeachExamController.questionAddHandler)
        , (r'/sangao_admin/TeachExam/question_edit', sangao_admin.TeachExamController.questionEditHandler)
        , (r'/sangao_admin/TeachExam/teach_lists', sangao_admin.TeachExamController.teachListsHandler)
        , (r'/sangao_admin/TeachExam/teach_detail', sangao_admin.TeachExamController.teachDetailHandler)
        , (r'/sangao_admin/TeachExam/teach_add', sangao_admin.TeachExamController.teachAddHandler)
        , (r'/sangao_admin/TeachExam/teach_edit', sangao_admin.TeachExamController.teachEditHandler)
        , (r'/sangao_admin/TeachExam/lists', sangao_admin.TeachExamController.listsHandler)
        , (r'/sangao_admin/Design/edit', sangao_admin.DesignController.editHandler)
        , (r'/sangao_admin/Exam/lists', sangao_admin.ExamController.listsHandler)
        , (r'/sangao_admin/Exam/exam_paper_add', sangao_admin.ExamController.examPaperAddHandler)
        , (r'/sangao_admin/Exam/exam_paper_del', sangao_admin.ExamController.examPaperDelHandler)
        , (r'/sangao_admin/Exam/error_ranking', sangao_admin.ExamController.errorRankingHandler)
        , (r'/sangao_admin/Exam/edit', sangao_admin.ExamController.editHandler)
        , (r'/sangao_admin/Exam/select_question', sangao_admin.ExamController.selectQuestionHandler)
        , (r'/sangao_admin/Exam/join_exam_paper', sangao_admin.ExamController.joinExamPaperHandler)
        , (r'/sangao_admin/Exam/add_question', sangao_admin.ExamController.addQuestionHandler)
        , (r'/sangao_admin/Exam/remove_exam_paper', sangao_admin.ExamController.removeExamPaperHandler)
        , (r'/sangao_admin/Teach/list', sangao_admin.TeachController.listHandler)
        , (r'/sangao_admin/Design/lists', sangao_admin.DesignController.listsHandler)
        , (r'/sangao_admin/Design/add', sangao_admin.DesignController.addHandler)
        , (r'/sangao_admin/Design/del', sangao_admin.DesignController.delHandler)
        , (r'/sangao_admin/Design/check_pass', sangao_admin.DesignController.checkPassHandler)
        , (r'/sangao_admin/Question/add', sangao_admin.QuestionController.addHandler)
        , (r'/sangao_admin/Question/edit', sangao_admin.QuestionController.editHandler)
        , (r'/sangao_admin/Question/single_choice_add', sangao_admin.QuestionController.singleChoiceAddHandler)
        , (r'/sangao_admin/Question/multiple_choice_add', sangao_admin.QuestionController.multipleChoiceAddHandler)
        , (r'/sangao_admin/Question/operation_add', sangao_admin.QuestionController.operationAddHandler)
        , (r'/sangao_admin/Question/true_false_add', sangao_admin.QuestionController.trueFalseAddHandler)   
        , (r'/sangao_admin/Question/fill_blank_add', sangao_admin.QuestionController.fillBlankAddHandler)  
        , (r'/sangao_admin/Question/lists', sangao_admin.QuestionController.listsHandler)   
        , (r'/sangao_admin/Question/select', sangao_admin.QuestionController.selectHandler)       
        , (r'/sangao_admin/Question/index', sangao_admin.QuestionController.indexHandler)    
        , (r'/sangao_admin/Question/del', sangao_admin.QuestionController.delHandler)    
        , (r'/sangao_admin/Question/error_question', sangao_admin.QuestionController.errorQuestionHandler)    
        , (r'/sangao_admin/Knowledge/add', sangao_admin.KnowledgeController.addHandler)    
        , (r'/sangao_admin/Knowledge/index', sangao_admin.KnowledgeController.indexHandler)         
        , (r'/sangao_admin/Question/source_add', sangao_admin.QuestionController.sourceAddHandler)     
        , (r'/sangao_admin/Question/source_lists', sangao_admin.QuestionController.sourceListsHandler)     
        , (r'/sangao_admin/User/lists', sangao_admin.UserController.listsHandler)    
        , (r'/sangao_admin/Record/lists', sangao_admin.RecordController.listsHandler)
        , (r'/sangao_admin/Record/add', sangao_admin.RecordController.addHandler)    
        , (r'/sangao_admin/Record/logic_chain', sangao_admin.RecordController.getLogicChainHandler)                         
        , (r'/sangao_admin/Index/click_statistics', sangao_admin.IndexController.clickStatisticsHandler),
              # 配置多个静态目录路由
        (r'/static_single_choice_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","single_choice")}),
        (r'/static_multiple_choice_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","multiple_choice")}),
        (r'/static_fill_blank_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","fill_blank")}),
        (r'/static_operation_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","operation")}),
        (r'/static_tf_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","true_false")}),
        (r'/static_operation_question_files/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","files","operation")}),
        (r'/static_Answer_files/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Answer","files")}),
        (r'/board_pic/(.*)', StaticFileHandler, {'path': config.get_path("sangao_admin","TeachExam", "images","board")}),
        (r'/static_Question_js/(.*)',StaticFileHandler, {'path': config.get_path("sangao","Question", "js")}),
        (r'/static_js/(.*)',StaticFileHandler, {'path': config.get_path("sangao_admin", "TeachExam", "js")}),

        ],
        
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




