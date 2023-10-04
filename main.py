#導入discord.py模組 並且使用commands模組
import discord
from discord.ext import commands

#導入其它所需的模組
import os
import json
from dotenv import load_dotenv

#載入.env檔
load_dotenv()

#設定機器人的權限
intents = discord.Intents.all()

#建立機器人 並設定機器人的指令前綴
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

#當機器人完成啟動時
@bot.event
async def on_ready():
    #設定機器人狀態
    await bot.change_presence(activity=discord.Game(name="$help")) 
    print(f"bot is ready! {bot.user}")
"""
@bot.command()
#help指令
async def help(ctx):
    embed=discord.Embed(title="指令說明", description="$help")
    embed.add_field(name="記帳 $buy", value="用法: $buy <金額> <名稱>(若不輸入則顯示noname)", inline=False)
    embed.add_field(name="查帳 $check", value="用法: $check", inline=False)
    embed.add_field(name="刪除 $delete", value="用法: $delete <編號 or all>", inline=True)
    embed.add_field(name="總金額 $total", value="用法: $total", inline=False)
    await ctx.send(embed=embed)
"""
@bot.command()
#載入元件
async def load(ctx, *args):
    if ctx.author.id != bot.owner_id:
        return
    if len(args) == 0:
        await ctx.send("請輸入元件名稱")
        return
    for i in args:
        await bot.load_extension(f"cogs.{i}")
        await ctx.send(f"已載入 {i}")

@bot.command()
#卸載元件
async def unload(ctx, *args):
    if ctx.author.id != bot.owner_id:
        return
    if len(args) == 0:
        await ctx.send("請輸入元件名稱")
        return
    for i in args:
        await bot.unload_extension(f"cogs.{i}")
        await ctx.send(f"已卸載 {i}")

@bot.command()
#重新載入元件
async def reload(ctx, *args):
    if ctx.author.id != bot.owner_id:
        return
    if len(args) == 0:
        await ctx.send("請輸入元件名稱")
        return
    for i in args:
        await bot.reload_extension(f"cogs.{i}")
        await ctx.send(f"已重新載入 {i}")

@bot.command()
#顯示作者
async def author(ctx):
    name = bot.get_user(bot.owner_id)
    embed=discord.Embed(title="作者", description=f"作者: {name}")
    embed.add_field(name="Profile", value=f"https://discordapp.com/users/{bot.owner_id}")
    embed.set_thumbnail(url = name.avatar)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.reply("pong!")

@bot.command()
#記帳指令
async def buy(ctx, *args):
    #判斷是否有輸入參數
    if len(args) == 0:
        await ctx.reply("格式錯誤")
        await ctx.send("格式: $buy <價格> <名稱>(可省略)")
    else:
        #判斷是否存在使用者資料
        if not os.path.exists(f"Datas/{ctx.author.id}.json"):
            #若不存在 則建立使用者資料
            with open("Datas/sample.json", "r") as f:
                sample = json.load(f)
                sample["name"] = ctx.author.name
                json.dump(sample, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)

        #讀取使用者資料
        with open(f"Datas/{ctx.author.id}.json", "r") as f:
            data = json.load(f)
            data["log"]
            #判斷是否有輸入名稱
            #若沒有則使用"noname"作為名稱
            if len(args) == 1:
                data["log"][data["nextID"]] = ["noname", int(args[0])]
            else:
                data["log"][data["nextID"]] = [args[1], int(args[0])]
            data["nextID"] += 1
            #計算總金額
            total = 0
            for i in data["log"]:
                total += data["log"][i][1]
            data["total"] = total
            #紀錄資料到json
            json.dump(data, open(f"Data/{ctx.author.id}.json", "w"), indent = 4)
            await ctx.reply(f"已記錄 ID:{data['nextID']-1}, 名稱:{data['log'][data['nextID']-1][0]}, 價格:{data['log'][data['nextID']-1][1]}")

@bot.command()
#刪除數據指令
async def delete(ctx, *args):
    #判斷是否存在使用者資料
    if not os.path.exists(f"Datas/{ctx.author.id}.json"):
        await ctx.reply("無資料")
        with open("Datas/sample.json", "r") as f:
            sample = json.load(f)
            sample["name"] = ctx.author.name
            json.dump(sample, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
    
    #讀取使用者資料
    with open(f"Datas/{ctx.author.id}.json", "r") as f:
        data = json.load(f)

    #判斷輸入參數是否正確
    if len(args) == 0:
        await ctx.reply("格式錯誤")
        await ctx.send("格式: $delete <編號> or all")
    #刪除全部
    elif args[0].lower() == "all":
        os.remove(f"Datas/{ctx.author.id}.json")
        await ctx.reply("已刪除")
    #刪除指定編號
    elif args[0] in data["log"]:
        del data["log"][args[0]]
        json.dump(data, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
        await ctx.reply(f"已刪除 編號為 {args[0]} 的資料")

@bot.command()
#查看總金額指令
async def total(ctx):
    #判斷是否存在使用者資料 若存在則顯示總金額
    if os.path.exists(f"Datas/{ctx.author.id}.json"):
        with open(f"Datas/{ctx.author.id}.json", "r") as f:
            data = json.load(f)
            await ctx.reply(f"總金額: {data['total']}")
    else:
        await ctx.reply("無資料")

@bot.command()
#查看紀錄指令
async def check(ctx):
    #判斷是否存在使用者資料 若存在則顯示紀錄
    if os.path.exists(f"Datas/{ctx.author.id}.json"):
        with open(f"Datas/{ctx.author.id}.json", "r") as f:
            data = json.load(f)
            text = "" #輸出文字
            j = 1
            for i in data["log"]:
                text += f"{j}. ID:{i}, 名稱:{data['log'][i][0]}, 價格:{data['log'][i][1]}\n"
                j += 1
            await ctx.reply(f"```{text}```")
    else:
        await ctx.reply("無資料")

def main():
    bot.owner_id = int(os.getenv("Owner"))
    #啟動機器人
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    main()