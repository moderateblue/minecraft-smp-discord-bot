import discord
import json
import os
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = 'p!', intents = intents)

def ownercheck(ctx):
  return ctx.author.id == 0 #redacted

@client.event
async def on_ready():
  await client.change_presence(status = discord.Status.online, activity = discord.Game('PooCraft SMP'))
  print('We have logged in as {0.user}'.format(client))

@client.command(hidden = True)
@commands.check(ownercheck)
async def selfdestruct(ctx):
  exit()

@client.command(hidden = True)
@commands.check(ownercheck)
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f'loaded {extension}')

@client.command(hidden = True)
@commands.check(ownercheck)
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  await ctx.send(f'unloaded {extension}')

@client.command(hidden = True)
@commands.check(ownercheck)
async def reload(ctx, extension):
  client.reload_extension(f'cogs.{extension}')
  await ctx.send(f'reloaded {extension}')

for filename in os.listdir('0'): #redacted
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run('0') #redacted
