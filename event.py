import discord
import random

intent = discord.Intents.all()
intent.message_content = True
client = discord.Client(intents=intent, help_command=None)

@client.event
async def on_ready():
    print("bot is ready!")

@client.event
# 當頻道有新訊息
async def on_message(message):
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    # 新訊息包含Hello，回覆Hello, world!
    if message.content.upper() == "HI":
        await message.channel.send("Hi")
    if message.content.startswith('你'):
        context = ["不是我", "我沒有", "我不要", "我不知道"]
        await message.channel.send(context[random.randint(0, len(context)-1)])
        #print(message.content)

client.run('MTE1ODY2NDIxMDQ5OTIzOTk3Ng.GqJ4Eu.B5z7b_qW-10SDqCyoeA7MY8cuKTxiVvQTaWJPM')