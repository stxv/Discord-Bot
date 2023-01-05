import discord
import requests
import json
from Private.config import token
from discord.ext import commands
# client instance allows interaction with discord API
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
# discord.py revolves around the concept of events. 
# https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events 

#Let's us know if the bot is online by printing a message
@bot.event
async def on_ready():
    print(F"{bot.user} has logged in")
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

@bot.event
async def on_message(message):
    if message.author != bot.user:
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
                await message.channel.send(f"{message.author.mention} You cannot send links because you do not have permssions.")
                return
        if message.content == ("!stoic"):
            await message.channel.send(rand_quote())
#Members with kick perms will be able to kick other members
        if message.content.startswith('!kick') and message.author.guild_permissions.kick_members:
            user_mention = message.content.split(" ")[1]
            user = message.guild.get_member(int(user_mention.strip("<@!>")))
            message.channel.send(f"{user} has been kicked")
            await user.kick()
#Welcomes members to server, this has to be coupled with the server settings, change the system message channel to the designated welcome channel
@bot.event
async def on_member_join(member):
    # Send the message to a designated welcome channel
    channel = bot.get_channel(1057700425140285560)
    await channel.send(f"Welcome to the server, {member.mention}!")
#Allows the bot to function
bot.run(token)