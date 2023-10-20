import discord
import random
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix = 'p!')

class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send('This command does not exist')

  @commands.command(aliases=['8ball'], brief = 'it\'s just 8ball', usage = '<question>')
  async def eightball(self, ctx, *, question):
    responses = [
      'It is certain.',
      'It is decidedly so.',
      'Without a doubt.',
      'Yes - definitely.',
      'You may rely on it.',
      'As I see it, yes.',
      'Most likely.',
      'Outlook good.',
      'Yes.',
      'Signs point to yes.',
      'Reply hazy, try again.',
      'Ask again later.',
      'Better not tell you now.',
      'Cannot predict now.',
      'Concentrate and ask again.',
      'Don\'t count on it.',
      'My reply is no.',
      'My sources say no.',
      'Outlook not so good.',
      'Very doubtful.'
    ]
    await ctx.send(random.choice(responses))
  
  @eightball.error
  async def eightball_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send('You need to ask a question, dummy')

  @commands.command(brief = 'roast someone with a crap roast lol')
  async def roast(self, ctx, person):
    iq = random.randint(1, 1000)
    roasts = [
      ', your mom gae',
      f' have -{iq}iq',
      ' is a dumb dumb',
      ' got a mending book from an enchantment table',
      ' thinks netherite is poop found in the nether'
    ]
    roastchoice = random.choice(roasts)
    await ctx.send(f'{person}{roastchoice}')
  
  @roast.error
  async def roast_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send('You need someone to roast, dummy')

  @commands.command(aliases = ['cf', 'flipcoin', 'fc'], brief = 'it\'s just coinflip')
  async def coinflip(self, ctx, amount = 1):
    if str(amount).startswith('-'):
      await ctx.send('no')
    elif amount == 0:
      await ctx.send('no')
    else:
      coinsides = ['heads', 'tails']
      if amount <= 10:
        coins = [
          str(random.choice(coinsides))
          for _ in range(amount)
        ]
        await ctx.send(', '.join(coins))
      else:
        await ctx.send('why you flippin\' so many coins man')
  
  @coinflip.error
  async def coinflip_error(self, ctx, error):
    if isinstance(error, commands.UserInputError):
      await ctx.send('no')
  
  @commands.command(brief = 'death note but no one actually dies because i can\'t do that :(')
  async def kill(self, ctx, *, player):
    author = ctx.author
    deathmsg = [
      f'{player} was slain by Arrow',
      f'{player} was shot by Arrow',
      f'{player} was pricked to death',
      f'{player} drowned',
      f'{player} experienced kinetic energy',
      f'{player} blew up',
      f'{player} was blown up by {author}',
      f'{player} hit the ground too hard',
      f'{player} fell from a high place',
      f'{player} was squashed by a falling anvil',
      f'{player} was squashed by a falling block',
      f'{player} went up in flames',
      f'{player} burned to death',
      f'{player} went off with a bang',
      f'{player} tried to swim in lava',
      f'{player} was struck by lightning',
      f'{player} discovered floor was lava',
      f'{player} was killed by magic',
      f'{player} was killed by {author} using magic',
      f'{player} was slain by {author}',
      f'{player} was slain by Small Fireball',
      f'{player} starved to death',
      f'{player} suffocated in a wall',
      f'{player} was killed trying to hurt {author}',
      f'{player} was impaled to death by {author}',
      f'{player} fell out of the world',
      f'{player} withered away',
      f'{player} died',
      f'{player} was sniped by {author}',
      f'{player} was spitballed by {author}'
    ]
    await ctx.send(random.choice(deathmsg))

  @commands.command(brief = 'roll dice/die', usage = '[number of dice (default 1)] [number of sides for each dice (default 6)]')
  async def roll(self, ctx, number_of_dice = 1, number_of_sides = 6):
    dice = [
      str(random.choice(range(1, number_of_sides + 1)))
      for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

  @commands.command(brief = 'tell bot to send emoji')
  async def emoji(self, ctx, emojiname):
    emoji = discord.utils.get(ctx.message.guild.emojis, name = emojiname)
    if emoji == None:
      await ctx.send(':' + emojiname + ':')
    else:
      await ctx.send(emoji)

  @commands.command(hidden = True)
  @commands.has_permissions(administrator = True)
  async def say(self, ctx, channelname, *, message):
    channel = discord.utils.get(ctx.guild.channels, name = channelname)
    await channel.send(message)
  
  @commands.command(hidden = True)
  @commands.has_permissions(administrator = True)
  async def edit(self, ctx, channelname, messageid, *, newcontent):
    channel = discord.utils.get(ctx.guild.channels, name = channelname)
    message = await channel.fetch_message(messageid)
    await message.edit(content = newcontent)
  
  @commands.group(aliases = ['calc'], brief = 'calculate stuff i think', help = 'gay: calculate someone\'s gayness\nlove: calculate 2 people\'s relationship success\nsimp: calculate someone\'s simpness')
  async def calculate(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send('you need to calculate something')

  @calculate.command()
  async def gay(self, ctx):
    await ctx.send('type the name of the person')
    channel = ctx.message.channel
    author = ctx.author
    def check(m):
      return m.channel == channel and m.author == author
    try:
      msg = await self.client.wait_for('message', timeout = 10, check = check)
    except asyncio.TimeoutError:
      await channel.send('command timed out')
    else:
      msg_ = msg.content
      calcprocess = await channel.send('calculating')
      await asyncio.sleep(0.333)
      await calcprocess.edit(content = 'calculating.')
      await asyncio.sleep(0.333)
      await calcprocess.edit(content = 'calculating..')
      await asyncio.sleep(0.333)
      await calcprocess.edit(content = 'calculating...')
      percent = str(round(random.uniform(0, 100), 2)) + '%'
      await calcprocess.edit(content = f'{msg_} is {percent} gay!')

  @calculate.command()
  async def love(self, ctx):
    await ctx.send('type the name of the first person')
    channel = ctx.message.channel
    author = ctx.author
    def check(m):
      return m.channel == channel and m.author == author
    try:
      msg_one = await self.client.wait_for('message', timeout = 10, check = check)
    except asyncio.TimeoutError:
      await channel.send('command timed out')
    else:
      msg1 = msg_one.content
      await channel.send('type the name of the second person')
      try:
        msg_two = await self.client.wait_for('message', timeout = 10, check = check)
      except asyncio.TimeoutError:
        await channel.send('command timed out')
      else:
        msg2 = msg_two.content
        calcprocess = await channel.send('calculating')
        await asyncio.sleep(0.333)
        await calcprocess.edit(content = 'calculating.')
        await asyncio.sleep(0.333)
        await calcprocess.edit(content = 'calculating..')
        await asyncio.sleep(0.333)
        await calcprocess.edit(content = 'calculating...')
        percent = str(round(random.uniform(0, 100), 2)) + '%'
        await calcprocess.edit(content = f'the chance for {msg1} and {msg2}\'s relationship to succeed is {percent}!')
  
  @calculate.command()
  async def simp(self, ctx):
    await ctx.send('type the name of the person')
    channel = ctx.message.channel
    author = ctx.author
    def check(m):
      return m.channel == channel and m.author == author
    try:
      msg = await self.client.wait_for('message', timeout = 10, check = check)
    except asyncio.TimeoutError:
      await channel.send('command timed out')
    else:
      msg_ = msg.content
      calcprocess = await channel.send('calculating')
      await asyncio.sleep(0.333)
      await calcprocess.edit(content = 'calculating.')
      await asyncio.sleep(0.333)
      await calcprocess.edit(content = 'calculating..')
      await asyncio.sleep(0.333)
      await calcprocess.edit(content = 'calculating...')
      percent = str(round(random.uniform(0, 100), 2)) + '%'
      await calcprocess.edit(content = f'{msg_} is {percent} a simp!')
  
  @commands.command(aliases = ['rps'], brief = 'play rock paper scissors')
  async def rockpaperscissors(self, ctx):
    await ctx.send(random.choice([':rock:', ':roll_of_paper:', ':scissors:']))

def setup(client):
  client.add_cog(Fun(client))