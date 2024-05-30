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
        date = list(map(int, str(datetime.datetime.now().strftime("%Y %m %d %H %M %S")).split()))
    
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
                name = "noname"

            #判斷格式是否錯誤 並記錄資料
            try:
                int(args[0])
            except:
                await ctx.reply("格式錯誤")
                await ctx.send("格式: $buy <價格> <名稱>(可省略)")
                return
            
            name = args[1]
            data["log"][data["nextID"]] = [name, int(args[0]), date]
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
            return
        
        #讀取使用者資料
        with open(f"Datas/{ctx.author.id}.json", "r") as f:
            data = json.load(f)
            #判斷是否有紀錄
            if len(data["log"]) == 0:
                await ctx.reply("無資料")
            else:
                #一個頁面顯示的資料數
                page_nums = data["page_nums"] 
                #當前顯示頁面
                current_page = 0 
                #將json的dict轉成list 方便使用數字做為標籤
                log_index = [] 
                for i in data["log"]:
                    temp = data['log'][i]
                    temp.insert(0, i)
                    log_index.append(temp)

                #算出總頁面數
                total_page = -(-len(log_index) // page_nums)

                #有多頁面時 處理不同頁數顯示的資料
                def show_list(embed, current_page, page_nums):
                    #算出當前頁面第一筆資料的標籤數字
                    start_index = current_page * page_nums
                    #為當前頁面上的資料排序
                    j = 1
                    #該頁總金額
                    page_total = 0
                    #處理該頁的embed訊息
                    for i in range(start_index, start_index + page_nums):
                        #縮短後續所需字數XD
                        log = log_index[i]
                        #依格式加入embed訊息
                        embed.add_field(name=j, value=f"ID:{log[0]}, 名稱:{log[1]}, 價格:{log[2]}, 日期:{log[3][0]}/{log[3][1]}/{log[3][2]}", inline=False)
                        #計算金額
                        page_total += log[2]
                        j += 1

                    #回傳embed訊息和頁面總金額
                    return embed, page_total
                    
                #總頁數大於1
                if total_page > 1:
                    embed = discord.Embed(title=f"{self.bot.get_user(ctx.author.id)} 的帳本")
                    print("before def")
                    embed, page_total = show_list(embed, current_page, page_nums)
                    print("After def")
                    embed.add_field(name="", value="", inline=False)
                    embed.add_field(name="總金額", value=page_total, inline=False)
                    print("After add")
                    await ctx.reply(embed=embed)
                    print("done") # for test

                else:
                    #顯示紀錄
                    embed = discord.Embed(title=f"{self.bot.get_user(ctx.author.id)} 的帳本")
                    j = 1
                    for i in range(len(log_index)):
                        log = log_index[i]
                        # embed.add_field(name="", value=f"{j}. 名稱:{log[1]}, 價格:{log[2]}, 日期:{log[3][0]}/{log[3][1]}/{log[3][2]}", inline=False)
                        embed.add_field(name=j, value=f"名稱:{log[1]}\n價格:{log[2]}\n日期:{log[3][0]}/{log[3][1]}/{log[3][2]}", inline=True)
                        # text += f"{j}. ID:{log[0]}, 名稱:{log[1]}, 價格:{log[2]}, 日期:{log[3][0]}/{log[3][1]}/{log[3][2]}\n"
                        j += 1
                    embed.add_field(name="", value="", inline=False)
                    embed.add_field(name="總金額", value=data["total"], inline=False)
                    await ctx.reply(embed=embed)
                
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