import discord, random, time, os, json
import keep_alive
from discord.ext import commands
client = commands.Bot(command_prefix='>')
dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir, 'setting.json'), 'r', encoding='utf-8') as jfile:
    settings = json.load(jfile)

@client.event
async def on_ready():
    print(client.user)
    game = discord.Game('你媽')
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_message(message):
    # 防止機器人發出的訊息觸發指令
    if message.author == client.user:
        return
    else:
        print(message.content, message.channel)
    # 複誦訊息
    if message.content.startswith('偉大唐主席說：'):
        tmp = message.content.split('：', 2)
        if tmp[1] == '':
            replys = ['= =', '==', '你要我說三小', '講人話好嗎', '不要煩我', '滾']
            await message.channel.send(random.choice(replys))
        else:
            await message.channel.send(tmp[1])
    # @R6警察
    if message.content == '<@&831204351313313812>' and message.channel == client.get_channel(831200868103356476) and message.author.id == 361192451777626113:
            chance = random.randrange(5, 100)
            print(chance)
            if chance <= 20:
                for _ in range(10):
                    await message.channel.send('<@&875375560132530197>')
                    time.sleep(0.5)
                await message.channel.send('操你媽 你現在爽了沒')
            else:
                await message.channel.send('幹你娘 閉嘴 低能兒')
    # 請問這是我婆嗎
    if message.content == '請問這是我婆嗎':
        if message.author.id == 453528901650612244:
            lines = ['是', '沒錯', '當然']
            await message.channel.send(random.choice(lines))
        else:
            lines = ['0', '並沒有', '不是', '想太多', '快醒醒', '滾']
            await message.channel.send(random.choice(lines))
    # 唐主席中文名言集
    if message.author.id == 453528901650612244:
        if message.content == '真的':
            pic = discord.File(os.path.join(dir, 'Pic', 'Really.png'))
            await message.channel.send(file=pic)
        elif message.content == '謝謝':
            pic = discord.File(os.path.join(dir, 'Pic', 'Thanks.png'))
            await message.channel.send(file=pic)

if __name__ == '__main__':
  keep_alive.keep_alive()
  client.run(settings['TOKEN'])