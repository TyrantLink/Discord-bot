import discord, json, os
from random import randint
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix = "dip!")
client.remove_command('help')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await autoResponse(message)
    await client.process_commands(message)
async def autoResponse(ctx):
    response = ""
    if ctx.author.bot: return
    if ctx.content in qa: await ctx.channel.send(qa[ctx.content])


@client.event
async def on_ready():
    print(f"{client.user.name} connected to Discord!\n")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Hentai'))
    await reload()

@client.command(name = "test")
async def test(ctx):
    await ctx.send(embed = discord.Embed(title = "Bot Commands", description = "WIP", color = 0xf40bd5))

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title='help',description='dip!help <command> for knowledge',color=0xf40bd5)
    embed.add_field(name='user commands',value='help \nfunny')
    embed.add_field(name='admin commands',value='reload')
    await ctx.send(embed=embed)

@help.command(name='reload')
async def help_reload(ctx): await ctx.send(embed=discord.Embed(title='reload',description='Reloads auto-responses',color=0xf40bd5).add_field(name='Syntax',value='dip!reload'))

@help.command(name='help')
async def help_help(ctx): await ctx.send(embed=discord.Embed(title='help',description='I think you already found out how to use this.',color=0xf40bd5).add_field(name='Syntax',value='dip!help'))

@help.command(name='funny')
async def help_funny(ctx): await ctx.send(embed=discord.Embed(title='funny',description='Sends a random image from the haha funny image folder.',color=0xf40bd5).add_field(name='Syntax',value='dip!funny'))

@client.command(name = "reload")
async def reload():
    global qa, hahaFunnyImages,hahaFunnyVideos, hahaFunnySounds
    with open('QA.json','r') as file:
        qa = json.loads(file.read())
    hahaFunnyImages = []
    for root, dirs, files in os.walk(fr"D:\haha funny image"):
        for filename in files:
            hahaFunnyImages.append(f'{root}\\{filename}')

    hahaFunnyVideos = []
    for root, dirs, files in os.walk(fr"D:\haha funny video"):
        for filename in files:
            hahaFunnyVideos.append(f'{root}\\{filename}')
    
    hahaFunnySounds = []
    for root, dirs, files in os.walk(fr"D:\haha funny sound"):
        for filename in files:
            hahaFunnySounds.append(f'{root}\\{filename}')

@client.group(invoke_without_command=True)
async def funny(ctx):
    await ctx.send(embed=discord.Embed(title='funny',description='dip!funny image\ndip!funny video\ndip!funny sound',color=0xf40bd5))

@funny.command(name="image")
async def funnyImage(ctx):
    await ctx.send(file=discord.File(hahaFunnyImages[randint(0,len(hahaFunnyImages))]))

@funny.command(name="video")
async def funnyVideo(ctx):
    await ctx.send(file=discord.File(hahaFunnyVideos[randint(0,len(hahaFunnyVideos))]))

@funny.command(name="sound")
async def funnySound(ctx):
    await ctx.send(file=discord.File(hahaFunnySounds[randint(0,len(hahaFunnySounds))]))

client.run(TOKEN)
