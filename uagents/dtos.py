from uagents import Model
from typing import List, Optional

class Request(Model):
  npc_name: str
  npc_desc: str
  last_events: List[str]
 
class DialogueOption(Model):
  text: str
  next: Optional[int] = None
  finish: Optional[bool] = None

class Dialogue(Model):
  message: str
  options: Optional[List[DialogueOption]] = None
  finish: Optional[bool] = None

class Response(Model):
  dialogue: List[Dialogue]
