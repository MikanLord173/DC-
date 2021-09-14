import discord, json, os
from discord.ext import tasks, commands
from core import Cog_Core
from bot import update_settings, dir
import YTCrawler

with open(os.path.join(dir, 'setting.json'), 'r', encoding='utf-8') as jfile:
    settings = json.load(jfile)

class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.Crawl.start()

    @tasks.loop(minutes=1.0)
    async def Crawl(self):
        print('Im working')
        Crawler = YTCrawler.YTCrawler('UCTkyJbRhal4voLZxmdRSssQ')
        info = Crawler.Run()
        if info != None and settings['last_upload'][0] != info['title']:
            channel = self.bot.get_channel(831184709241274372)
            await channel.send(f"{info['channel']}發布了新影片！\r{info['url']}")
        settings['last_upload'][0] = info['title']
        update_settings(settings)

    @Crawl.before_loop
    async def before_crawl(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Tasks(bot))
