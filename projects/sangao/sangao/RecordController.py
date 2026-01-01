# RecordController.py
import os
import time
from pathlib import Path
import tornado.web
# from sangao_admin.AudioProcessService import AudioProcessService
import logging
from jobs.asr_client import transcribe_audio_file_sync 
from jobs.llm_client import polish_transcript_sync
from common.CommonModel import Common

logger = logging.getLogger(__name__)

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        records = Common.select("sangao", "SELECT * FROM record")
        self.render(
            os.path.join(Common.BASE_DIR, "sangao", "templates", "Record", "lists.html"),
            records=records
        )



class detailHandler(tornado.web.RequestHandler):
    def get(self):
        record = Common.find("sangao", "SELECT * FROM record where id="+self.get_argument("id"))
        self.render(
            os.path.join(Common.BASE_DIR, "sangao", "templates", "Record", "detail.html"),
            record=record
        )

