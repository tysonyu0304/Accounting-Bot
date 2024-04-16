#導入discord.py模組 並且使用commands模組
import discord
from discord.ext import commands

#導入其它所需的模組
import os
from dotenv import load_dotenv
import asyncio

#載入.env檔
load_dotenv()

#設定機器人的權限
intents = discord.Intents.all()

#建立機器人 並設定機器人的指令前綴
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)
bot.owner_id = os.getenv("Owner")

#當機器人完成啟動時
@bot.event
async def on_ready():
    #設定機器人狀態
    await bot.change_presence(activity=discord.Game(name="$help")) 
    print(f"bot is ready! {bot.user}")

#載入所有元件
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command()
@commands.is_owner()
#載入元件指令
async def load(ctx, *args):
    if len(args) == 0:
        await ctx.send("請輸入元件名稱")
        return
    for i in args:
        await bot.load_extension(f"cogs.{i}")
        await ctx.send(f"已載入 {i}")

@bot.command()
@commands.is_owner()
#卸載元件
async def unload(ctx, *args):
    if len(args) == 0:
        await ctx.send("請輸入元件名稱")
        return
    for i in args:
        await bot.unload_extension(f"cogs.{i}")
        await ctx.send(f"已卸載 {i}")

@bot.command()
@commands.is_owner()
#重新載入元件
async def reload(ctx, *args):
    if len(args) == 0:
        await ctx.send("請輸入元件名稱")
        return
    for i in args:
        await bot.reload_extension(f"cogs.{i}")
        await ctx.send(f"已重新載入 {i}")

#主程式
async def main():
    await load_cogs()
    #啟動機器人
    await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())