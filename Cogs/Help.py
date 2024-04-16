import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self): #當機器人完成啟動時
        print("Help is ready!")

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed=discord.Embed(title="指令說明", description="$help")
        embed.add_field(name="記帳 $buy", value="用法: $buy <金額> <名稱>(若不輸入則顯示noname)", inline=False)
        embed.add_field(name="查帳 $check", value="用法: $check", inline=False)
        embed.add_field(name="刪除 $delete", value="用法: $delete <編號 or all>", inline=True)
        embed.add_field(name="編輯 $edit", value="用法: $edit <編號> <金額>")
        embed.add_field(name="總金額 $total", value="用法: $total", inline=False)
        embed.add_field(name="作者 $author", value="用法: $author")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))