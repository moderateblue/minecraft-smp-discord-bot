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
os.chdir('0') #redacted

async def get_storage_data():
  with open('currency.json', 'r') as f:
    users = json.load(f)
  return users

async def open_profile(user):
  users = await get_storage_data()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = 10
    with open('currency.json', 'w') as f:
      json.dump(users, f)

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

class Shop(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command(brief = 'opens shop menu')
  async def shop(self, ctx, page = 1):
    if page == 1:
      embed = discord.Embed(title = 'Buy Roles and More', description = 'no sale lol also ***__DO NOT ABUSE ANY OF THESE PERKS__***', color = discord.Color.gold())
      embed.set_author(name = 'POO SHOP', url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', icon_url = 'https://cdn.discordapp.com/icons/723346195996606524/c5d50a49c13d84326c74e491d6c7df7a.png?size=128')
      embed.add_field(name = '<:IronIngot:758382385191977010> VIP Rank - `20` Poo Tokens', value = 'Display separately, Send TTS messages, Move members in voice channel', inline = False)
      embed.add_field(name = '<:GoldIngot:758382288836100110> VIP+ Rank - `55` Poo Tokens', value = 'Perks of VIP, Mute members, Priority speaker', inline = False)
      embed.add_field(name = '<:Emerald:764586902593863690> MVP Rank - `70` Poo Tokens', value = 'Perks of VIP+, Access to audit logs, Deafen members', inline = False)
      embed.add_field(name = '<:Diamond:758382238747328563> MVP+ Rank - `85` Poo Tokens', value = 'Perks of MVP, Mention @everyone (@here and all roles)', inline = False)
      embed.add_field(name = '<:NetheriteIngot:740095830702293062> MVP++ Rank - `100` Poo Tokens', value = 'Perks of MVP+, Flex', inline = False)
      embed.set_footer(text = 'Page 1 of 2')
      await ctx.send(embed = embed)
    elif page == 2:
      embed = discord.Embed(title = 'Buy Roles and More', description = 'no sale lol', color = discord.Color.gold())
      embed.set_author(name = 'POO SHOP', url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', icon_url = 'https://cdn.discordapp.com/icons/723346195996606524/c5d50a49c13d84326c74e491d6c7df7a.png?size=128')
      embed.add_field(name = '`100` Poo Shards - `1` Poo Token', value = 'Poo shards are for upgrading your sword', inline = False)
      embed.add_field(name = '`1` Poo Token - `100` Poo Shards', value = 'Poo tokens are for ranks and cosmetics', inline = False)
      embed.set_footer(text = 'Page 2 of 2')
      await ctx.send(embed = embed)

  @commands.command(brief = 'buy stuff (p!shop 2 for menu)(p!help buy)')
  async def buy(self, ctx, item, amount = 1):
    pass

def setup(client):
  client.add_cog(Shop(client))
