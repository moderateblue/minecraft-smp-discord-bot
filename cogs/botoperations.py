import discord
from discord.ext import commands
import random
import time

client = commands.Bot(command_prefix = 'bpb ')

def ownercheck(ctx):
  return ctx.author.id == 0 #redacted

class BotOperations(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(hidden = True)
  async def test(self, ctx):
    await ctx.send('tested')

  @commands.command(hidden = True)
  @commands.check(ownercheck)
  async def ownertest(self, ctx):
    await ctx.send('tested by owner')
  
  @commands.command(hidden = True)
  @commands.has_permissions(administrator = True)
  async def admintest(self, ctx):
    await ctx.send('tested by admin')

def setup(client):
  client.add_cog(BotOperations(client))
