import discord, random, time, os, json, re
import keep_alive
from discord.ext import commands
bot = commands.Bot(command_prefix='>', help_command=None)
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
    wifeRegex = re.compile(r'.*婆.*[嗎吧]')
    if re.match(wifeRegex, message.content):
        if message.author.id == settings['memberIDs']['深坑麻辣臭豆腐P']:
            lines = ['是', '沒錯', '當然']
            await message.channel.send(random.choice(lines))
        else:
            lines = ['0', '並沒有', '不是', '想太多', '快醒醒', '滾']
            await message.channel.send(random.choice(lines))
    # 唐主席中文名言集
    if message.content == '真的':
        pic = discord.File(os.path.join(dir, 'Pic', 'Really.png'))
        await message.channel.send(file=pic)
    elif message.content == '謝謝':
        pic = discord.File(os.path.join(dir, 'Pic', 'Thanks.png'))
        await message.channel.send(file=pic)
    # 針對鴆希說婆
    if message.author.id == 361192451777626113 and re.search('婆', message.content):
      lines = ['0', '並沒有', '不是']
      await message.channel.send(random.choice(lines))
    # 好笑嗎
    if message.content == '好笑嗎' and message.reference.message_id != None:
      dumb_jokes = settings['dumb_jokes']
      target = await message.channel.fetch_message(message.reference.message_id)
      if target.author == bot.user:
        lines = ['別想給我來這招', '不好笑']
        await message.channel.send(random.choice(lines))
      else:
        dumb_jokes.append([target.content, target.author.id])
        await message.channel.send('好笑嗎')
        update_settings()
      print(dumb_jokes)
    await bot.process_commands(message)

@bot.command()
async def gacha(ctx, game, type, count: int=None, too_many=None):
    if too_many != None:
        await ctx.send('指令格式錯誤。\r正確格式：>gacha [遊戲] [single/multi] [次數]')
        return
    if count == None:
      count = 1
    output = ''
    result = {}
    if count < 1:
      await ctx.send('次數不是正整數我是要怎麼抽')
      return
    games = {
      'LLSIF': [['R', 'SR', 'SSR', 'UR'], [80, 15, 4, 1], 11],
      'LLAS': [['R', 'SR', 'UR'], [85, 10, 5], 10],
      'ARKNIGHTS': [['3★', '4★', '5★', '6★'], [40, 50, 8, 2], 10]
    }
    Game = games.get(game.upper())
    if Game != None:
      if type.lower() == 'single' or type.upper() == 'S' or type == '單' or type == '單抽':
        if count > 100:
            await ctx.send('那麼多我抽不完 = =')
            return
        cards = random.choices(Game[0], weights=Game[1], k=count)
        for rarity in Game[0]:
          for card in cards:
            if card == rarity:
              result[rarity] = result.get(rarity, 0) + 1
        for x in range(len(cards)):
            if cards[x] == Game[0][-1]:
                cards[x] = f'__**{Game[0][-1]}**__'
        for x in range(len(cards)):
          if (x+1) % 5 == 0:
            output += f'[{cards[x]}]、\r'
          else:
            output += f'[{cards[x]}]、'
        if output[-1] == '、':
          output = output[:-1:]
        elif output[-1] == '\r':
          output = output[:-2:]
        output += f'\r合計：'
      elif type.lower() == 'multi' or type.upper() == 'M' or type == '連' or type == '連抽':
        if count > 30:
            await ctx.send('那麼多我抽不完 = =')
            return
        for x in range(count):
          cards = random.choices(Game[0], weights=Game[1], k=Game[2]-1)
          high_rarities = [[], []]
          for y in range(1, len(Game[0])):
            high_rarities[0].append(Game[0][y])
            high_rarities[1].append(Game[1][y])
          high_rarities[1][0] += Game[1][0]
          cards.append(random.choices(high_rarities[0], weights=high_rarities[1], k=1)[0])
          for rarity in Game[0]:
            for card in cards:
              if card == rarity:
                result[rarity] = result.get(rarity, 0) + 1
          for x in range(len(cards)):
            if cards[x] == Game[0][-1]:
                cards[x] = f'__**{Game[0][-1]}**__'
          output += f'{str(cards)}\r'
        output += '合計：'
      else:
        await ctx.send('要單抽還是連抽講清楚啦')
        return
      for rarity in Game[0]:
        if result.get(rarity) != None:
          output += f'\r{rarity}: {result[rarity]}張'
        else:
          output += f'\r{rarity}: 0張'
      await ctx.send(output)
    else:
      await ctx.send('那什麼鳥遊戲 聽都沒聽過')

@gacha.error
async def gacha_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('指令格式錯誤。\r正確格式：>gacha [遊戲] [single/multi] [次數]')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('次數不是正整數我是要怎麼抽')

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

@bot.command()
async def get_help(ctx):
  embed = discord.Embed(title='偉大唐主席', description='很好....你很腦殘嗎....敢這樣講學園偶像.......我死也不會放過你。', color=discord.Color.from_rgb(160, 255, 249))
  embed.add_field(name='>gacha [遊戲] [single/multi] [次數]', value='抽卡模擬\r目前支援遊戲：LLAS、LLSIF。\rsingle(S)代表單抽；multi(M)代表連抽（通常為十連）。\r次數為正整數，代表進行抽卡的次數，若不填則抽一次，不要填入太大的數字。', inline=False)
  embed.add_field(name='偉大唐主席說：[文字]', value='唐主席會複誦[文字]內的內容，冒號可用半/全形，或用空格代替。', inline=False)
  embed.add_field(name='好笑嗎', value='使用此指令必須要回覆一則訊息，會將該訊息的內容及發送者存入『白痴語錄庫』當中。', inline=False)
  embed.add_field(name='>白痴語錄', value='從『白痴語錄庫』隨機發送一則訊息，並標註原作者。', inline=False)
  embed.add_field(name='其它功能', value='會針對特定訊息做回覆，像是：\r防止鴆希@R6\r當某人說XXX婆會做出回應\r說"真的"或"謝謝"會丟圖片', inline=False)
  await ctx.send(embed=embed)


if __name__ == '__main__':
  keep_alive.keep_alive()
  bot.run(Token['TOKEN'])