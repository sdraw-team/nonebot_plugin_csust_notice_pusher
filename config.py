from typing import List
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    notice_pusher_enable: List = []