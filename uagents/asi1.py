import json
import requests
import os

from typing import Dict, List
from prompts import *
from dtos import Dialogue


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


async def call_asi1_api_with_buildings(dialogs: List[str]) -> Dict:
  url = "https://api.asi1.ai/v1/chat/completions"

  ret = ""

  for d in dialogs:
    ret += d
    ret += "\n"

  payload = json.dumps({
    "model": "asi1-mini",
    "messages": [
      {
        "role": "system",
        "content": ENV_PROMPT
      },
      {
        "role": "user",
        "content": ENV_PROMPT_TEMPLATE.format(dialogs=ret)
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