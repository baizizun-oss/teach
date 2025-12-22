# RecordController.py
import os
import time
from pathlib import Path
import tornado.web
import myportal.common as common
# from sangao_admin.AudioProcessService import AudioProcessService
import logging
from jobs.asr_client import transcribe_audio_file_sync 
from jobs.llm_client import polish_transcript_sync

logger = logging.getLogger(__name__)

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        records = common.select("sangao", "SELECT * FROM record")
        self.render(
            os.path.join(common.BASE_DIR, "sangao", "templates", "Record", "lists.html"),
            records=records
        )



class detailHandler(tornado.web.RequestHandler):
    def get(self):
        record = common.find("sangao", "SELECT * FROM record where id="+self.get_argument("id"))
        self.render(
            os.path.join(common.BASE_DIR, "sangao", "templates", "Record", "detail.html"),
            record=record
        )

