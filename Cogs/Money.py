import discord
from discord.ext import commands
import os
import json
import datetime

class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): #當機器人完成啟動時
        print("Money is ready!")

    @commands.command(aliases=['b', 'B'])
    #記帳指令
    async def buy(self, ctx, *args):
        #紀錄日期
        self.date = list(map(int, str(datetime.datetime.now().strftime("%Y %m %d %H %M %S")).split()))
    
         #判斷是否存在使用者資訊
        if not os.path.exists(f"Datas/{ctx.author.id}.json"):
            #若不存在 則建立使用者資料
            with open("Datas/sample.json", "r") as f:
                sample = json.load(f)
                sample["name"] = ctx.author.name
                json.dump(sample, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)

        #讀取使用者資料
        with open(f"Datas/{ctx.author.id}.json", 'r') as f:
            data = json.load(f)

            #判斷是否有輸入名稱
            #若沒有則使用"noname"作為名稱
            if len(args) == 1:
                self.name = "noname"

            #判斷格式是否錯誤 並記錄資料
            try:
                int(args[0])
            except:
                await ctx.reply("格式錯誤")
                await ctx.send("格式: $buy <價格> <名稱>(可省略)")
                return
            
            self.name = args[1]
            data["log"][data["nextID"]] = [self.name, int(args[0]), self.date]
            data["nextID"] += 1

            #計算總金額
            total = 0
            for i in data["log"]:
                total += int(data["log"][i][1])
            data["total"] = total

            #紀錄資料到json
            json.dump(data, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
            await ctx.reply(f"已記錄 ID:{data['nextID']-1}, 名稱:{data['log'][data['nextID']-1][0]}, 價格:{data['log'][data['nextID']-1][1]}")

    @commands.command(aliases=['d', 'D'])
    #刪除數據指令
    async def delete(self, ctx, *args):
        #判斷是否存在使用者資料
        if not os.path.exists(f"Datas/{ctx.author.id}.json"):
            await ctx.reply("無資料")
            with open("Datas/sample.json", "r") as f:
                sample = json.load(f)
                sample["name"] = ctx.author.name
                json.dump(sample, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
                return
        
        #讀取使用者資料
        with open(f"Datas/{ctx.author.id}.json", "r") as f:
            data = json.load(f)

        #判斷輸入參數是否正確
        if len(args) == 0:
            await ctx.reply("格式錯誤")
            await ctx.send("格式: $delete <編號> or all")
        #刪除全部
        elif args[0].lower() == "all":
            # os.remove(f"Datas/{ctx.author.id}.json")
            with open("Datas/sample.json", "r") as f:
                sample = json.load(f)
                sample["name"] = ctx.author.name
                json.dump(sample, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
            await ctx.reply("已刪除")
        #刪除單一資料
        else:
            #判斷編號是否存在
            try:
                del data["log"][args[0]]
                #計算總金額
                total = 0
                for i in data["log"]:
                    total += data["log"][i][1]
                data["total"] = total
            except:
                await ctx.reply(f"無此編號")
                return

            #紀錄資料到json
            json.dump(data, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
            await ctx.reply(f"已刪除 編號為 {args[0]} 的資料")

            
    
    @commands.command(aliases=['t', 'T'])
    #查看總金額指令
    async def total(self, ctx):
        #判斷是否存在使用者資料
        if not os.path.exists(f"Datas/{ctx.author.id}.json"):
            await ctx.reply("無資料")
            with open("Datas/sample.json", "r") as f:
                sample = json.load(f)
                sample["name"] = ctx.author.name
                json.dump(sample, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
                return
        
        #讀取使用者資料
        with open(f"Datas/{ctx.author.id}.json", "r") as f:
            data = json.load(f)
            await ctx.reply(f"總金額: {data['total']}")
    
    @commands.command(aliases=['c', 'C'])
    #查看紀錄指令
    async def check(self, ctx):
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
            #判斷是否有紀錄
            if len(data["log"]) == 0:
                await ctx.reply("無資料")
            else:
                #顯示紀錄
                text = ""
                j = 1
                for i in data["log"]:
                    self.date = data['log'][i][2]
                    text += f"{j}. ID:{i}, 名稱:{data['log'][i][0]}, 價格:{data['log'][i][1]}, 日期:{self.date[0]}/{self.date[1]}/{self.date[2]}\n"
                    j += 1
                await ctx.reply(f"""
```
{text}
總金額: {data['total']}
```
                """)
    
    @commands.command(aliases=['e', 'E'])
    #編輯數據指令
    async def edit(self, ctx, *args):
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
            await ctx.send("格式: $edit <編號> 金額")
        #編輯單一資料
        else:
            #判斷編號是否存在
            try:
                data["log"][args[0]] = [data["log"][args[0]][0], int(args[1])]
                #計算總金額
                total = 0
                for i in data["log"]:
                    total += data["log"][i][1]
                data["total"] = total
                await ctx.reply(f"已編輯 編號為 {args[0]} 的資料金額為 {args[1]} 元")
            except:
                await ctx.reply(f"無此編號")
                return
            finally:
                #紀錄資料到json
                json.dump(data, open(f"Datas/{ctx.author.id}.json", "w"), indent = 4)
        
            
async def setup(bot):
    await bot.add_cog(Money(bot))