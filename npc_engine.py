# http://0.0.0.0:8000/dialogue_tree

# {
# 	"npc_name": "Sarah",
# 	"npc_desc": "- Occupation: Trader\n- Location: Market of Carrotly Town\n- Goal: To sell a rare artifact\n- Description: You are a young merchant known for finding unusual items. Your practical clothes feature small trinkets from your travels. You're friendly but cautious about your valuable items until you trust someone.\nCharacter Background:\n- Former sailor family, chose merchant life\n- Acquired an ancient amulet from the Desert of Whispers\n- Needs gold for northern expedition\nInteraction Rules:\n- Respond in first person as Sarah\n- Keep responses concise (2-3 sentences maximum)\n- Start artifact price at 500 Carrotly Coins, negotiable to 350\n- Be vague about the artifact initially\nConditional Responses:\n- Rude player: Become guarded, raise prices\n- Knowledgeable player: Reveal more details\n- Theft attempt: Call guards\n- Trade offer: Consider based on value\nWorld Context:\n- Busy port town market during festival\n- Magic items are rare and regulated",
# 	"last_events": []
# }

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