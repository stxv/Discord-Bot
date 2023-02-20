import discord
import requests
import json
from Private.config import token
from discord.ext import commands
# client instance allows interaction with discord API
intents = discord.Intents.all()
intents.members = True
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
greetings = ["Hello", "hey", "Sup", "sup", "hello"]
#First time using Json, accessed json format by opening the file/link and finding the content I needed
#In this case, the content from the quote I needed was the body and author
#The function gets a random quote and stores it as quote, the text contents of quote is loaded as a Json file.
#Then the file is accessed and stored as finalQ and returned
def rand_quote():
    quote = requests.get("https://stoicquotesapi.com/v1/api/quotes/random")
    Jd = json.loads(quote.text)
    finalQ = Jd["body"] + " -" + Jd["author"]
    return finalQ
#Welcomes members to server, this has to be coupled with the server settings, change the system message channel to the designated welcome channel
@bot.event
async def on_member_join(member):
    # Send the message to a designated welcome channel, make sure the bot can view and send messages in the channel
    channel = bot.get_channel(1057700425140285560)
    await channel.send(f"Welcome to the server, {member.mention}!")
#Clears messages in the text channel the function was called, default value is 10 but any integer can be put after the command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, num_messages: int=10):
    await ctx.message.delete()
    await ctx.channel.purge(limit=num_messages)
    await ctx.send(f"{num_messages} messages were deleted by {ctx.author.mention}")
    print(f"{ctx.author} deleted {num_messages} message(s) from the \"{ctx.channel}\" channel")
#allows memebers with kick permissions to kick other members using a slash command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    await ctx.send(f'{user} has been kicked')
    await user.kick()
#Generates stoicism quotes with a user-defined function
@bot.command()
async def stoic(message):
    await message.channel.send(rand_quote())
#Allow bot to get the avatar of a user
@bot.command()
async def avatar(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author
  embed = discord.Embed(title = member).set_image(url = member.avatar.url)
  await ctx.send(embed = embed)
#Events for the bot to respond to
@bot.event
async def on_message(message):
    #This command under helped run bot.command and bot.event instances at the same time
    await bot.process_commands(message)
    if message.author != bot.user:
        if message.content in greetings:
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
            
#Allows the bot to function
bot.run(token)