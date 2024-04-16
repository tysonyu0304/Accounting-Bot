import discord
from discord.ext import commands
import datetime

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def time(self, ctx):
        current_time = datetime.datetime.now().strftime("%y/%m/%d")
        await ctx.send(current_time)

async def setup(bot):
    await bot.add_cog(Test(bot))