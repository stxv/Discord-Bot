import discord
import requests
import json
from Private.config import token
# client instance allows interaction with discord API
intents = discord.Intents.all()
client = discord.Client(intents=intents)
# discord.py revolves around the concept of events. 
# https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events 

#Let's us know if the bot is online by printing a message
@client.event
async def on_ready():
    print(F"{client.user} has logged in")
#Allows the bot to respond to a specific message
badwords = ["213"]
Links = ["https://", "http://"]
#First time using Json, accessed json format by opening the file/link and finding the content I needed
#In this case, the content from the quote I needed was the body and author
#The function gets a random quote and stores it as quote, the text contents of quote is loaded as a Json file.
#Then the file is accessed and stored as finalQ and returned
def rand_quote():
    quote = requests.get("https://stoicquotesapi.com/v1/api/quotes/random")
    Jd = json.loads(quote.text)
    finalQ = Jd["body"] + " -" + Jd["author"]
    return finalQ

@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith("X"):
            await message.channel.send(f"Hello {message.author.display_name}")
#Basic moderation code that deletes text in a given list
        for Bwords in badwords:
            if "G" not in str(message.author.roles) and Bwords in str(message.content):
                await message.delete()
                return
#Deletes links sent from users without admin roles
        for links in Links:
            if "G" not in str(message.author.roles) and links in str(message.content):
                await message.delete()
                await message.channel.send(f"{message.author.mention} No links!")
                return
        if message.content == ("!stoic"):
            await message.channel.send(rand_quote())
#Allows the bot to function
client.run(token)