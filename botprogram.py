import discord
from Private.config import token
# client instance allows interaction with discord API
intents = discord.Intents.all()
client = discord.Client(intents=intents)
# discord.py revolves around the concept of events. 
# An event is something you listen to and then respond to.
# https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events 
#Let's us know if the bot is online by printing a message
@client.event
async def on_ready():
    print(F"{client.user} has logged in")
#Allows the bot to respond to a specific message
badwords = ["213"]
Links = ["https://", "http://"]
@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith("X"):
            await message.channel.send(f"Hello {message.author.display_name}")
#Basic moderation code that deletes text in a given string
        for Bwords in badwords:
            if "G" not in str(message.author.roles) and Bwords in str(message.content.lower()):
                await message.delete()
                return
#Deletes links sent from users without admin roles
        for links in Links:
            if "G" not in str(message.author.roles) and links in str(message.content.lower()):
                await message.delete()
                await message.channel.send(f"{message.author.mention} No links!")
                return
#Allows the bot to function
client.run(token)