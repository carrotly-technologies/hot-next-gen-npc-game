import os
import requests
import json

from asi1 import call_asi1_api
from dotenv import load_dotenv
from uagents import Agent, Context
from dtos import Request, Response

load_dotenv()

agent = Agent(
  name="NPC Engine",
  port=8000,
  seed="1158b220-d5e9-454f-a460-e84a857b4327",
  endpoint=["http://127.0.0.1:8000"],
)

@agent.on_rest_post("/dialogue_tree", Request, Response)
async def create_dialogue_tree(_: Context, req: Request) -> Response:
  response = await call_asi1_api(npc_name=req.npc_name, npc_desc=req.npc_desc, last_events=req.last_events)  
  dialogue = json.loads(response['choices'][0]['message']['content'])

  return Response(dialogue=dialogue)

if __name__ == "__main__":
  agent.run()
 