import discord, random, time, os, json, re, requests
import crawler
from discord.ext import commands, tasks
bot = commands.Bot(command_prefix='>', help_command=None)
dir = os.path.dirname(os.path.abspath(__file__))

r = requests.head(url='https://discord.com/api/v1')
try:
    print(f'Rate limit {int(r.headers["Retry-After"])/60} minutes left.')
except:
    print('No rate limit.')

with open(os.path.join(dir, 'setting.json'), 'r', encoding='utf-8') as jfile:
    settings = json.load(jfile)

with open(os.path.join(dir, 'token.json'), 'r', encoding='utf-8') as jtoken:
    Token = json.load(jtoken)

def update_settings(sett):
  with open(os.path.join(dir, 'setting.json'), 'w', encoding='utf-8') as file:
    json.dump(sett, file, indent=4)

@bot.event
async def on_ready():
    print(f'{bot.user}到Discord耍帥')
    game = discord.Game('你媽')
    await bot.change_presence(status=discord.Status.idle, activity=game)
    #YouTubeCrawler.start()

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
	embed = discord.Embed(
	    title='偉大唐主席',
	    description='很好....你很腦殘嗎....敢這樣講學園偶像.......我死也不會放過你。',
	    color=discord.Color.from_rgb(160, 255, 249))
	embed.add_field(
	    name='>gacha [遊戲] [single/multi] [次數]',
	    value=
	    '抽卡模擬\r目前支援遊戲：LLAS、LLSIF、ARKNIGHTS。\rsingle(S)代表單抽；multi(M)代表連抽（通常為十連）。\r次數為正整數，代表進行抽卡的次數，若不填則抽一次，不要填入太大的數字。',
	    inline=False)
	embed.add_field(name='偉大唐主席說：[文字]',
	                value='唐主席會複誦[文字]內的內容，冒號可用半/全形，或用空格代替。',
	                inline=False)
	embed.add_field(name='好笑嗎',
	                value='使用此指令必須要回覆一則訊息，會將該訊息的內容及發送者存入『白痴語錄庫』當中。',
	                inline=False)
	embed.add_field(name='>白痴語錄',
	                value='從『白痴語錄庫』隨機發送一則訊息，並標註原作者。',
	                inline=False)
	embed.add_field(
	    name='其它功能',
	    value='會針對特定訊息做回覆，像是：\r防止鴆希@R6\r當某人說XXX婆會做出回應\r說"真的"或"謝謝"會丟圖片',
	    inline=False)
	await ctx.send(embed=embed)

@bot.command()
async def temp(ctx):
	numbers = crawler.run()
	if numbers != []:
		output = ''
		for a in numbers:
			output += f'{a}號 '
		output += '還沒填體溫'
		await ctx.send(output)
	else:
		await ctx.send('大家很乖')

@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cmds.{extension}')
	await ctx.send(f'已載入{extension}。')

@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cmds.{extension}')
	await ctx.send(f'已卸載{extension}。')

@bot.command()
async def reload(ctx, extension):
	bot.reload_extension(f'cmds.{extension}')
	await ctx.send(f'已重新載入{extension}。')

'''@tasks.loop(minutes=3.0)
async def YouTubeCrawler():
	Crawler = YTCrawler.YTCrawler(Token['YTAPI'])
	uploads_id = Crawler.get_uploads_id('UCTkyJbRhal4voLZxmdRSssQ')
	playlist = Crawler.get_playlist(uploads_id)
	video_info = Crawler.get_video(playlist[0])
	if settings['last_upload'][0] != video_info['time']:
		channel = bot.get_channel(831184709241274372)
		await channel.send(f"{video_info['channel']}發布了新影片！\r{video_info['url']}")
	settings['last_upload'][0] = video_info['time']
	update_settings()'''

for file in os.listdir(os.path.join(dir, 'cmds')):
	if file.endswith('.py'):
		bot.load_extension(f'cmds.{file[:-3]}')

if __name__ == '__main__':
	bot.run(Token['TOKEN'])