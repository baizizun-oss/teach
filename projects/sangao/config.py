#config.py

import os


BASE_DIR = os.path.join(os.path.dirname(__file__))

UPLOAD_FILE_BASE_DIR= os.path.join(BASE_DIR,"common","static","upload","file")

UPLOAD_BASE_DIR= os.path.join(BASE_DIR,"common","static","upload")
# 各种文件类型子目录
UPLOAD_PATHS = {
    'single_choice': os.path.join(UPLOAD_FILE_BASE_DIR, "single_choice_question","images"),
    'multiple_choice': os.path.join(UPLOAD_FILE_BASE_DIR, "multiple_choice_question"),
    'true_false': os.path.join(UPLOAD_FILE_BASE_DIR, "true_false_question"),
    'operation_files': os.path.join(UPLOAD_FILE_BASE_DIR, "operation_question","files"),
    'operation_images': os.path.join(UPLOAD_FILE_BASE_DIR, "operation_question","images"),
}

#确保各个上传目录存在
for path in UPLOAD_PATHS.values():
    os.makedirs(path, exist_ok=True)


STATIC_PATHS = {
    'single_choice_question_images': os.path.join(UPLOAD_BASE_DIR, "single_choice_question","images"),
    'multiple_choice': os.path.join(UPLOAD_BASE_DIR, "multiple_choice_question"),
    'true_false': os.path.join(UPLOAD_BASE_DIR, "true_false_question"),
    'operation_images': os.path.join(UPLOAD_BASE_DIR, "operation_question","images"),
    'operation_files': os.path.join(UPLOAD_BASE_DIR, "operation_question","files"),
    'fill_blank': os.path.join(UPLOAD_BASE_DIR, "fill_blank_question"),
    'board_pic': os.path.join(BASE_DIR,"sangao_admin","templates","TeachExam","upload")
}

# 定义多个静态文件目录的绝对路径
STATIC_PATH = os.path.join(BASE_DIR, "static")  # 通用静态资源
# SINGLE_CHOICE_QUESTION_UPLOAD_IMAGES_PATH = os.path.join(UPLOAD_FILE_BASE_DIR, "single_choice_question","images")
# UPLOAD_STUDENT_WORKS_PATH = os.path.join(BASE_DIR, "uploads", "student_works")
# UPLOAD_MATERIAL_ATTACHMENTS_PATH = os.path.join(BASE_DIR, "uploads", "material_attachments")

# 定义Tornado应用的settings字典
settings = {
    "static_path": STATIC_PATH,  # 默认静态路径
    #"template_path": os.path.join(BASE_DIR, "templates"),
    "debug": True,
}