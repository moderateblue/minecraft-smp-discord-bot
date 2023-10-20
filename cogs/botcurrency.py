import discord
from discord.ext import commands
import random
import json
import os
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

class Currency(commands.Cog):
  def __init__(self, client):
    self.client = client
    self._cd = commands.CooldownMapping.from_cooldown(1.0, 604800.0, commands.BucketType.user)
    self._cd2 = commands.CooldownMapping.from_cooldown(1.0, 60.0, commands.BucketType.user)
    self._cd3 = commands.CooldownMapping.from_cooldown(1.0, 10.0, commands.BucketType.user)

  @commands.command(brief = 'check how many poo tokens a person has')
  async def storage(self, ctx, person:discord.Member = None):
    if person is None:
      await open_profile(ctx.author)
      user = ctx.author
      users = await get_storage_data()
      storage_amt = users[str(user.id)]
      em = discord.Embed(title = f'{ctx.author.name}\'s storage', color = discord.Color.blue())
      em.add_field(name = 'poo tokens', value = storage_amt)
      em.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
      await ctx.send(embed = em)
    else:
      await open_profile(person)
      user = person
      users = await get_storage_data()
      storage_amt = users[str(user.id)]
      em = discord.Embed(title = f'{person.name}\'s storage', color = discord.Color.blue())
      em.add_field(name = 'poo tokens', value = storage_amt)
      em.set_footer(text = person.name, icon_url = person.avatar_url)
      await ctx.send(embed = em)

  @storage.error
  async def storage_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      em = discord.Embed(title = 'could not find the person you entered', color = discord.Color.red())
      await ctx.send(embed = em)
  
  @commands.command(brief = 'pay other users poo tokens', usage = '<amount> <person>')
  async def pay(self, ctx, amount:int, receiver:discord.Member = None):
    await open_profile(ctx.author)
    user = ctx.author
    userid = user.id
    users = await get_storage_data()
    receiverid = receiver.id
    amount = amount
    if amount < 0:
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'you tryna rob people bruh')
      await ctx.send(embed = em)
    elif amount > users[str(userid)]:
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'you don\'t have enough poo tokens for this payment bruh')
      await ctx.send(embed = em)
    elif userid == int(receiverid):
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'why u tryna pay yourself bruh')
      await ctx.send(embed = em)
    elif amount == 0:
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'you cannot pay nothing bruh')
      await ctx.send(embed = em)
    else:
      users[str(userid)] -= amount
      users[str(receiverid)] += amount
      with open('currency.json', 'w') as f:
        json.dump(users, f)
      em = discord.Embed(title = 'payment successful', color = discord.Color.green())
      em.add_field(name = 'amount', value = amount)
      em.add_field(name = 'to', value = f'<@{receiverid}>')
      em.add_field(name = 'from', value = f'<@{userid}>')
      await ctx.send(embed = em)

  @pay.error
  async def pay_error(self, ctx, error):
    if isinstance(error, commands.UserInputError):
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'bad input bruh')
      await ctx.send(embed = em)
  
  @commands.command(aliases = ['claimreward','weekly'], brief = 'free poo token every week')
  @commands.cooldown(1, 604800, commands.BucketType.user)
  async def claim(self, ctx):
    await open_profile(ctx.author)
    user = ctx.author
    userid = user.id
    users = await get_storage_data()
    users[str(userid)] += 1
    with open('currency.json', 'w') as f:
      json.dump(users, f)
    em = discord.Embed(title = 'claim successful', color = discord.Color.green(), description = 'you claimed your weekly poo token')
    await ctx.send(embed = em)
    bucket = self._cd.get_bucket(ctx.message)
    global retry_after
    retry_after = bucket.update_rate_limit()

  @claim.error
  async def claim_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      bucket = self._cd.get_bucket(ctx.message)
      retry_after = bucket.update_rate_limit()
      retry_after = round(retry_after)
      minutes, seconds = divmod(retry_after, 60)
      hours, minutes = divmod(minutes, 60)
      days, hours = divmod(hours, 24)
      if retry_after:
        em = discord.Embed(title = 'claim unsuccessful', color = discord.Color.red(), description = f'you can use this command again after {days}d {hours}h {minutes}m {seconds}s')
        await ctx.send(embed = em)
  
  @commands.command(aliases = ['slots'], brief = 'use slot machine, p!help slotmachine for more info', help = '0 symbols match = lose bet\n2 symbols match = give back bet\n3 symbols match = double bet', description = 'This command is very good at stealing your poo tokens')
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def slotmachine(self, ctx, bet: int):
    await open_profile(ctx.author)
    global retry_after2
    if bet == 0:
      em = discord.Embed(title = 'wager unsuccessful', color = discord.Color.red(), description = 'you can\'t wager nothing bruh')
      await ctx.send(embed = em)
      bucket = self._cd2.get_bucket(ctx.message)
      retry_after2 = bucket.update_rate_limit()
    elif bet < 0:
      em = discord.Embed(title = 'wager unsuccessful', color = discord.Color.red(), description = 'you can\'t wager negative bruh')
      await ctx.send(embed = em)
      bucket = self._cd2.get_bucket(ctx.message)
      retry_after2 = bucket.update_rate_limit()
    else:
      user = ctx.author
      userid = user.id
      users = await get_storage_data()
      symbols = [
        '<:RedstoneDust:764588709529780285>',
        '<:NetheriteIngot:740095830702293062>',
        '<:LapisLazuli:764586917735563264>',
        '<:IronIngot:758382385191977010>',
        '<:GoldIngot:758382288836100110>',
        '<:Emerald:764586902593863690>',
        '<:Diamond:758382238747328563>',
        '<:Coal:764586875989786625>',
        '<:CopperIngot:773681066367909940>',
        '<:NetherQuartz:764590221479641088>']
      reels = [random.choice(symbols), random.choice(symbols), random.choice(symbols)]
      if reels[0] == reels[1] or reels[0] == reels[2] or reels[1] == reels[2]:
        if reels[0] == reels[1] == reels[2]:
          users[str(userid)] += bet * 2
          with open('currency.json', 'w') as f:
            json.dump(users, f)
          em = discord.Embed(title = 'you won the jackpot!', color = discord.Color.gold(), description = 'you got 3 matching icons')
          em.add_field(name = 'slots', value = f'{reels[0]} {reels[1]} {reels[2]}')
          await ctx.send(embed = em)
          bucket = self._cd2.get_bucket(ctx.message)
          retry_after2 = bucket.update_rate_limit()
        else:
          users[str(userid)] += bet
          with open('currency.json', 'w') as f:
            json.dump(users, f)
          em = discord.Embed(title = 'you won!', color = discord.Color.orange(), description = 'you got 2 matching icons')
          em.add_field(name = 'slots', value = f'{reels[0]} {reels[1]} {reels[2]}')
          await ctx.send(embed = em)
          bucket = self._cd2.get_bucket(ctx.message)
          retry_after2 = bucket.update_rate_limit()
      else:
        users[str(userid)] -= bet
        with open('currency.json', 'w') as f:
          json.dump(users, f)
        em = discord.Embed(title = 'you lost!', color = discord.Color.red(), description = 'you got no matching icons')
        em.add_field(name = 'slots', value = f'{reels[0]} {reels[1]} {reels[2]}')
        await ctx.send(embed = em)
        bucket = self._cd2.get_bucket(ctx.message)
        retry_after2 = bucket.update_rate_limit()

  @slotmachine.error
  async def slotmachine_error(self, ctx, error):
    if isinstance(error, commands.UserInputError):
      em = discord.Embed(title = 'wager unsuccessful', color = discord.Color.red(), description = 'what are you wagering bruh')
      await ctx.send(embed = em)
      bucket = self._cd2.get_bucket(ctx.message)
      retry_after2 = bucket.update_rate_limit()
    elif isinstance(error, commands.CommandOnCooldown):
      bucket = self._cd2.get_bucket(ctx.message)
      retry_after2 = bucket.update_rate_limit()
      retry_after2 = round(retry_after2)
      if retry_after2:
        em = discord.Embed(title = 'wager unsuccessful', color = discord.Color.red(), description = f'you can use this command again after {retry_after2}s')
        await ctx.send(embed = em)
  
  @commands.command(aliases = ['beg'], brief = 'send prayers to god or something idk bruh', help = 'is god even real are u sending prayers to a random number generator dumb dumb')
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def pray(self, ctx):
    global retry_after3
    prayers = [
      f'{ctx.author} sent a prayer to god',
      f'{ctx.author} prayed to god',
      f'{ctx.author} prayed to notch, thinking it was god',
      f'{ctx.author} prayed to herobrine, thinking it was notch',
      f'{ctx.author} has no idea what they are doing'
    ]
    prayer = random.choice(prayers)
    await ctx.send(prayer)
    await asyncio.sleep(1)
    if prayer == prayers[2]:
      notchprayer = random.choices(['notch gave you a poo token', 'notch ignored you'], [1, 60], k = 1)
      await ctx.send(notchprayer[0])
      if notchprayer[0] == 'notch gave you a poo token':
        await open_profile(ctx.author)
        user = ctx.author
        userid = user.id
        users = await get_storage_data()
        users[str(userid)] += 1
        with open('currency.json', 'w') as f:
          json.dump(users, f)
        bucket = self._cd3.get_bucket(ctx.message)
        retry_after3 = bucket.update_rate_limit()
    elif prayer == prayers[3]:
      await ctx.send('herobrine tried to kill you for disturbing him')
      bucket = self._cd3.get_bucket(ctx.message)
      retry_after3 = bucket.update_rate_limit()
    elif prayer == prayers[4]:
      await ctx.send('nobody received your "prayer" because you literally just prayed to an RNG')
      bucket = self._cd3.get_bucket(ctx.message)
      retry_after3 = bucket.update_rate_limit()
    else:
      received = random.choices([0, 1], [50, 1], k = 1)
      if received[0] == 0:
        await ctx.send('god did not give you anything')
        bucket = self._cd3.get_bucket(ctx.message)
        retry_after3 = bucket.update_rate_limit()
      else:
        await ctx.send('god gave you 1 poo token')
        await open_profile(ctx.author)
        user = ctx.author
        userid = user.id
        users = await get_storage_data()
        users[str(userid)] += 1
        with open('currency.json', 'w') as f:
          json.dump(users, f)
        bucket = self._cd3.get_bucket(ctx.message)
        retry_after3 = bucket.update_rate_limit()
  
  @pray.error
  async def pray_error(self, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      bucket = self._cd3.get_bucket(ctx.message)
      retry_after3 = bucket.update_rate_limit()
      retry_after3 = round(retry_after3)
      if retry_after3:
        em = discord.Embed(title = 'pray unsuccessful', color = discord.Color.red(), description = f'you can use this command again after {retry_after3}s')
        await ctx.send(embed = em)
  
  @commands.group(hidden = True, aliases = ['token'])
  @commands.has_permissions(administrator = True)
  async def tokens(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send('you need to type a p!tokens subcommand')

  @tokens.command()
  async def give(self, ctx,  amount: int, receiver:discord.Member):
    users = await get_storage_data()
    receiverid = receiver.id
    if amount == 0:
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'you cannot give nothing bruh')
      await ctx.send(embed = em)
    else:
      users[str(receiverid)] += amount
      with open('currency.json', 'w') as f:
        json.dump(users, f)
      em = discord.Embed(title = 'payment successful', color = discord.Color.green())
      em.add_field(name = 'amount', value = amount)
      em.add_field(name = 'to', value = f'<@{receiverid}>')
      await ctx.send(embed = em)
  
  @give.error
  async def give_error(self, ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
      em = discord.Embed(title = 'payment unsuccessful', color = discord.Color.red(), description = 'bad input bruh')
      await ctx.send(embed = em)

  @tokens.command()
  async def remove(self, ctx, amount:int, receiver:discord.Member):
    users = await get_storage_data()
    receiverid = receiver.id
    if amount == 0:
      em = discord.Embed(title = 'removal unsuccessful', color = discord.Color.red(), description = 'you cannot remove nothing bruh')
      await ctx.send(embed = em)
    else:
      users[str(receiverid)] -= amount
      with open('currency.json', 'w') as f:
        json.dump(users, f)
      em = discord.Embed(title = 'removal successful', color = discord.Color.green())
      em.add_field(name = 'amount', value = amount)
      em.add_field(name = 'from', value = f'<@{receiverid}>')
      await ctx.send(embed = em)
  
  @remove.error
  async def remove_error(self, ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
      em = discord.Embed(title = 'removal unsuccessful', color = discord.Color.red(), description = 'bad input bruh')
      await ctx.send(embed = em)

def setup(client):
  client.add_cog(Currency(client))
