import discord, random
from discord.ext import commands
from core import Cog_Core

class Gacha(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gacha(self, ctx, game, type, count: int = None, too_many=None):
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
                    if (x + 1) % 5 == 0:
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
                    cards = random.choices(Game[0], weights=Game[1], k=Game[2] - 1)
                    high_rarities = [[], []]
                    for y in range(1, len(Game[0])):
                        high_rarities[0].append(Game[0][y])
                        high_rarities[1].append(Game[1][y])
                    high_rarities[1][0] += Game[1][0]
                    cards.append(
                        random.choices(high_rarities[0],
                                    weights=high_rarities[1],
                                    k=1)[0])
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
    async def gacha_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('指令格式錯誤。\r正確格式：>gacha [遊戲] [single/multi] [次數]')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('次數不是正整數我是要怎麼抽')

def setup(bot):
    bot.add_cog(Gacha(bot))