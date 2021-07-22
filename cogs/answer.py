from discord.ext import commands
from typing import TYPE_CHECKING
from submits import *
import discord

if TYPE_CHECKING:
    from bot import Bot

class Answer(commands.Cog):

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command()
    async def todo(self, ctx, query: int):
        if query <= 0:
            return await ctx.send('올바른 값을 입력해주세요.')

        def add_submitted(i, submitted):
            embed.add_field(name=f'**{i+1}. {submitted.id}**', value=f'{datetime.fromtimestamp(submitted.date)}\n[초대 링크](https://discord.com/oauth2/authorize?client_id={submitted.id}&scope=bot&guild_id=653083797763522580)', inline=False)

        embed = discord.Embed(title=':rocket: ToDo List', color=discord.Color.green(), description='_ _')
        
        if query is None: # query가 입력 받지 않았을 경우
            for i, submitted in enumerate(submits):
                add_submitted(i, submitted)
        
        else:
            for i, submitted in enumerate(submits):
                if submitted.id == query:
                    add_submitted(i, submitted)
                    break
                if i == len(submits)-1: # query가 일치하는 id가 없을 경우 인덱스로 인식
                    if query > len(submits):
                        return await ctx.send('해당 쿼리를 인덱스 또는 ID로 가진 봇을 찾을 수 없습니다.')
                    add_submitted(query-1, submits[query-1])

        await ctx.send(embed=embed)

    @commands.command()
    async def approve(self, ctx, query: int):
        for submitted in submits:
            if submitted.id == query:
                approved_submits.append(submits.pop(submits.index(submitted)))
                return await ctx.send(f'**봇 {query}**가 정상적으로 승인되었습니다.')

        await ctx.send(f'**봇 {query}**를 찾을 수 없습니다.')

    @commands.command()
    async def deny(self, ctx, query: int):
        for submitted in submits:
            if submitted.id == query:
                submits.remove(submitted)
                return await ctx.send(f'**봇 {query}**가 정상적으로 거부되었습니다.') 

        await ctx.send(f'**봇 {query}**를 찾을 수 없습니다.')
        
        
def setup(bot: "Bot"):
    bot.add_cog(Answer(bot))
