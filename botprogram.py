import discord
# client instance allows interaction with discord API
client = discord.Client()
# discord.py revolves around the concept of events. 
# An event is something you listen to and then respond to.
# https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events 
@client.event
async def on_ready():
    print("hello")
