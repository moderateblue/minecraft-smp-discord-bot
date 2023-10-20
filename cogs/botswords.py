import discord
from discord.ext import commands
import random
import json
import os
import collections
import asyncio

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = 'p!', intents = intents)

async def get_sword_data():
  with open('swords.json', 'r') as s:
    users = json.load(s)
  return users

async def open_profile_sword(user):
  users = await get_sword_data()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = collections.defaultdict(dict)
    users[str(user.id)]['sword'] = 'wooden'
    users[str(user.id)]['sharpness'] = 0
    users[str(user.id)]['poo shards'] = 0
    with open('swords.json', 'w') as s:
      json.dump(users, s)

class Forge(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(brief = 'check someone\'s sword')
  async def sword(self, ctx, person:discord.Member = None):
    if person is None:
      await open_profile_sword(ctx.author)
      user = ctx.author
      users = await get_sword_data()
      sword = users[str(user.id)]['sword']
      sharp = users[str(user.id)]['sharpness']
      shards = users[str(user.id)]['poo shards']
      em = discord.Embed(title = f'{ctx.author.name}\'s sword', color = discord.Color.blue())
      em.add_field(name = 'sword material', value = sword)
      em.add_field(name = 'sword sharpness level', value = sharp)
      em.add_field(name = 'poo shards', value = shards)
      em.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
      await ctx.send(embed = em)
    else:
      await open_profile_sword(person)
      user = person
      users = await get_sword_data()
      sword = users[str(user.id)]['sword']
      sharp = users[str(user.id)]['sharpness']
      shards = users[str(user.id)]['poo shards']
      em = discord.Embed(title = f'{person.name}\'s sword', color = discord.Color.blue())
      em.add_field(name = 'sword material', value = sword)
      em.add_field(name = 'sword sharpness level', value = sharp)
      em.add_field(name = 'poo shards', value = shards)
      em.set_footer(text = person.name, icon_url = person.avatar_url)
      await ctx.send(embed = em)

  @sword.error
  async def sword_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      em = discord.Embed(title = 'could not find the person you entered', color = discord.Color.red())
      await ctx.send(embed = em)
  
#  @commands.command(brief = 'get poo shards')
#  async def bruh(self, ctx):
#    await open_profile_sword(ctx.author)
#    user = ctx.author
#    userid = user.id
#    users = await get_sword_data()
#    users[str(userid)]['poo shards'] += 1
#    with open('swords.json', 'w') as s:
#      json.dump(users, s)

def setup(client):
  client.add_cog(Forge(client))