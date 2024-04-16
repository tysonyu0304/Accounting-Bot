import discord
from discord.ext import commands

import os

class Author(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): #當機器人完成啟動時
        print("Author is ready!")

    @commands.command()
    async def author(self, ctx):
        ID = os.getenv("Owner")
        name = self.bot.get_user(int(ID))
        embed = discord.Embed(title="作者", description=f"作者: {name}")
        embed.add_field(name="Profile", value=f"https://discordapp.com/users/{self.bot.owner_id}")
        embed.set_thumbnail(url = name.avatar)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Author(bot))
