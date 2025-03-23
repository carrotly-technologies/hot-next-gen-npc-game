import json
import requests

def call_npc_engine_api(npc_name: str, npc_desc: str, last_events: list) -> dict:
  url = "http://0.0.0.0:8000/dialogue_tree"

  payload = json.dumps({
    "npc_name": npc_name,
    "npc_desc": npc_desc,
    "last_events": last_events
  })

  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  dialogue = response.json()

  return dialogue['dialogue']