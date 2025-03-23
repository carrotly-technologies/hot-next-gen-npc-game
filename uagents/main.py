import os
import requests
import json

from uagents import Agent, Context, Model
from typing import List, Optional, Dict
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
  name="Sarah NPC",
  port=8000,
  seed="1158b220-d5e9-454f-a460-e84a857b4321",
  endpoint=["http://127.0.0.1:8000"],
)

@agent.on_rest_post("/dialogue_tree", Request, Response)
async def create_dialogue_tree(ctx: Context, req: Request) -> Response:
  response = await call_csi_api(sarah_npc)  
  dialogue = json.loads(response['choices'][0]['message']['content'])

  print(dialogue)

  return Response(dialogue=dialogue)

if __name__ == "__main__":
  agent.run()
 