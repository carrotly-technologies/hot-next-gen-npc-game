
from uagents import Agent, Bureau, Context, Model

class Message(Model):
    message: str

npc1 = Agent(name="NPC1", seed="sigmar recovery phrase", port=8000, endpoint=["http://localhost:8000/submit"])
npc2 = Agent(name="NPC2", seed="slaanesh recovery phrase", port=8001, endpoint=["http://localhost:8001/submit"])
npc3 = Agent(name="NPC2", seed="slaanesh recovery phrase", port=8001, endpoint=["http://localhost:8001/submit"])

@npc1.on_interval(period=3.0)
async def send_message(ctx: Context):
    await ctx.send(npc1.address, Message(message="hello there slaanesh, how are you"))

@ncp2.on_message(model=Message)
async def sigmar_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

@npc3.on_message(model=Message)
async def slaanesh_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(npc2.address, Message(message="hello there sigmar"))

bureau = Bureau()
bureau.add(sigmar)
bureau.add(slaanesh)

if __name__ == "__main__":
    bureau.run()
