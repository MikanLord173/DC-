import discord, random, re, time, os, json
from discord.ext import commands
from core import Cog_Core
from bot import update_settings, dir

with open(os.path.join(dir, 'setting.json'), 'r', encoding='utf-8') as jfile:
    settings = json.load(jfile)

class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
	    # 防止機器人發出的訊息觸發指令
        if message.author == self.bot.user:
            return
        else:
            print(message.content, message.channel)
        # 複誦訊息
        if re.match(r'偉大唐主席說[：:\s]?.*', message.content):
            if len(message.content) > 6:
                tmp = message.content.split(message.content[6], 1)
            else:
                tmp = '偉大唐主席說'
            if len(tmp) == 1 or tmp[1] == '' or tmp == '偉大唐主席說':
                replys = ['= =', '==', '你要我說三小', '講人話好嗎', '不要煩我', '滾']
                await message.channel.send(random.choice(replys))
            else:
                await message.channel.send(tmp[1])
                if not isinstance(message.channel, discord.channel.DMChannel):
                    await message.delete()
        # @R6警察
        if re.search('<@&831204351313313812>', message.content) and message.channel == self.bot.get_channel(831200868103356476): 
            if message.author.id == 361192451777626113 or message.author.id == 854013876411564039:
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
        if message.content == '謝謝':
            pic = discord.File(os.path.join(dir, 'Pic', 'Thanks.png'))
            await message.channel.send(file=pic)
        if re.search('滾', message.content) and message.author.id == 453528901650612244:
            pic = discord.File(os.path.join(dir, 'Pic', 'FuckOff.png'))
            await message.channel.send(file=pic)
        sleepRegex = r'.*我.*要睡[了啦]?\b|.*晚安|(我要)?睡[了啦]?\b'
        if re.match(sleepRegex, message.content):
            pic = discord.File(os.path.join(dir, 'Pic', 'GoodNight.png'))
            await message.channel.send(file=pic)
        # 針對鴆希說婆
        if message.author.id == 361192451777626113 and re.search(
            '婆', message.content):
            lines = ['0', '並沒有', '不是']
            await message.channel.send(random.choice(lines))
        # 好笑嗎
        if message.content == '好笑嗎' and message.reference != None:
            dumb_jokes = settings['dumb_jokes']
            target = await message.channel.fetch_message(message.reference.message_id)
            if target.author == self.bot.user:
                lines = ['別想給我來這招', '不好笑']
                await message.channel.send(random.choice(lines))
            else:
                dumb_jokes.append([target.content, target.author.id])
                await message.channel.send('好笑嗎')
                update_settings(settings)
            print(dumb_jokes)
        # 你覺得這樣很好笑嗎
        if message.content == '你覺得這樣很好笑嗎' and message.reference != None:
            target = await message.channel.fetch_message(
                message.reference.message_id)
            dumb_jokes = settings['dumb_jokes']
            if dumb_jokes[-1][1] == target.author.id:
                dumb_jokes[-1][0] += f'\r{target.content}'
                await message.channel.send('你要不要想一下你剛才到底講了什麼')
                update_settings(settings)
        if message.content == '鴆希又在幹話了' and message.reference != None:
            target = await message.channel.fetch_message(message.reference.message_id)
            dumb_jokes = settings['dumb_jokes']
            dumb_jokes.append([target.content, 361192451777626113])
            await message.channel.send('= =')
            update_settings(settings)

def setup(bot):
    bot.add_cog(Message(bot))