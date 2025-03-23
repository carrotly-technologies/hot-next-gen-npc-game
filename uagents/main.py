import os
import requests
import json

from asi1 import call_asi1_api, call_asi1_api_with_buildings
from dotenv import load_dotenv
from uagents import Agent, Context
from dtos import Request, Response, AreaRequest, AreaResponse

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

@agent.on_rest_post("/area", AreaRequest, AreaResponse)
async def create_dialogue_tree(_: Context, req: AreaRequest) -> AreaResponse:

  response = await call_asi1_api_with_buildings(dialogs=req.dialogs)


  print(response['choices'][0]['message']['content'])
  response_content = response['choices'][0]['message']['content']


  csv_string = response_content.strip("```csv").strip("`").strip().replace("\n", ",")
  return AreaResponse(content=csv_string)

if __name__ == "__main__":
  agent.run()
 