import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): #當機器人完成啟動時
        print("Ping is ready!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"ping : {round(self.bot.latency*1000)} ms")

async def setup(bot):
    await bot.add_cog(Ping(bot))