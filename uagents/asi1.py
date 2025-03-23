import json
import requests
import os

from typing import Dict, List
from prompts import *

async def call_asi1_api(npc_name: str, npc_desc: str, last_events: List[str]) -> Dict:
  url = "https://api.asi1.ai/v1/chat/completions"

  payload = json.dumps({
    "model": "asi1-mini",
    "messages": [
      {
        "role": "system",
        "content": SYSTEM_PROMPT
      },
      {
        "role": "user",
        "content": NPC_PROMPT_TEMPLATE.format(npc_name=npc_name, npc_desc=npc_desc, last_events="\n".join(last_events))
      }
    ],
    "temperature": 0,
    "max_tokens": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f"Bearer {os.getenv('FETCHAI_API_KEY')}"
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  
  return response.json()