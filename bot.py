import discord, random, time, os, json, re
import keep_alive
from discord.ext import commands
bot = commands.Bot(command_prefix='>')
dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir, 'setting.json'), 'r', encoding='utf-8') as jfile:
    settings = json.load(jfile)

with open(os.path.join(dir, 'token.json'), 'r', encoding='utf-8') as jtoken:
    Token = json.load(jtoken)

def update_settings():
  with open(os.path.join(dir, 'setting.json'), 'w', encoding='utf-8') as file:
    json.dump(settings, file)

@bot.event
async def on_ready():
    print(bot.user)
    game = discord.Game('你媽')
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_message(message):
    # 防止機器人發出的訊息觸發指令
    if message.author == bot.user:
        return
    else:
        print(message.content, message.channel)
    # 複誦訊息
    if re.match(r'偉大唐主席說[：:\s]?.*', message.content):
        str = message.content[6]
        tmp = message.content.split(str, 1)
        if len(tmp) == 1 or tmp[1] == '':
            replys = ['= =', '==', '你要我說三小', '講人話好嗎', '不要煩我', '滾']
            await message.channel.send(random.choice(replys))
        else:
            await message.channel.send(tmp[1])
            if not isinstance(message.channel, discord.channel.DMChannel):
              await message.delete()
    # @R6警察
    if message.content == '<@&831204351313313812>' and message.channel == bot.get_channel(831200868103356476) and message.author.id == 361192451777626113:
            chance = random.randint(1, 100)
            print(chance)
            if chance <= 10:
                for _ in range(10):
                    await message.channel.send('<@&875375560132530197>')
                    time.sleep(0.5)
                await message.channel.send('操你媽 你現在爽了沒')
            else:
                await message.channel.send('幹你娘 閉嘴 低能兒')
    # 請問這是我婆嗎
    if message.content == '請問這是我婆嗎':
        if message.author.id == settings['memberIDs']['深坑麻辣臭豆腐P']:
            lines = ['是', '沒錯', '當然']
            await message.channel.send(random.choice(lines))
        else:
            lines = ['0', '並沒有', '不是', '想太多', '快醒醒', '滾']
            await message.channel.send(random.choice(lines))
    # 唐主席中文名言集
    if message.author.id == settings['memberIDs']['深坑麻辣臭豆腐P']:
        if message.content == '真的':
            pic = discord.File(os.path.join(dir, 'Pic', 'Really.png'))
            await message.channel.send(file=pic)
        elif message.content == '謝謝':
            pic = discord.File(os.path.join(dir, 'Pic', 'Thanks.png'))
            await message.channel.send(file=pic)
    await bot.process_commands(message)
    # 針對鴆希說婆
    if message.author.id == 361192451777626113 and re.search('婆', message.content):
      lines = ['0', '並沒有', '不是']
      await message.channel.send(random.choice(lines))

@bot.command()
async def gacha(ctx):
  cards = random.choices(['R', 'SR', 'UR'], weights=[85, 10, 5], k=9)
  cards.append(random.choices(['SR', 'UR'], weights=[95, 5], k=1)[0])
  result = [0, 0, 0]
  for card in cards:
    if card == 'R':
      result[0] += 1
    elif card == 'SR':
      result[1] += 1
    elif card == 'UR':
      result[2] += 1
  output = str(cards) + f'\r合計：\rR: {result[0]}張\rSR: {result[1]}張\rUR: {result[2]}張'
  if result == [9, 1, 0]:
    output += '\r保底，笑死'
  elif result[2] == 0:
    output += '\r哭啊 沒有UR'
  elif result[2] >= 3:
    output += '\r牛逼啊老鐵'
  await ctx.send(output)

@bot.command()
async def 好笑嗎(ctx):
  dumb_jokes = settings['dumb_jokes']
  message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
  dumb_jokes.append([message.content, message.author.id])
  await ctx.send('好笑嗎')
  update_settings()
  print(dumb_jokes)

@bot.command()
async def 白痴語錄(ctx):
  dumb_jokes = settings['dumb_jokes']
  if len(dumb_jokes) != 0:
    chosen = random.choice(dumb_jokes)
    output = f'{chosen[0]}\rby <@{chosen[1]}>'
    await ctx.send(output)
  else:
    await ctx.send('沒東西可以發')
  print(dumb_jokes)

if __name__ == '__main__':
  keep_alive.keep_alive()
  bot.run(Token['TOKEN'])