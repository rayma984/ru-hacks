import nextcord
import asyncio
import time
from nextcord.ext import commands
from nextcord import Intents, Interaction

intents = Intents.all()
bot = commands.Bot(intents=intents)

async def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        #print(timer, end="\r")
        asyncio.sleep(1)
        t -= 1

@bot.slash_command(
    name="ping",
    description="pong!",
    guild_ids=[425353150250221601]
)
async def ex2(interaction: Interaction):
    embed1 = nextcord.Embed(title="Wordle", description="hello new york", url = "https://www.nytimes.com/games/wordle/index.html")
    embed1.set_image(url = "https://styles.redditmedia.com/t5_2rvxp/styles/communityIcon_9msefvyceyv51.jpg?") 
    # embed1.set_thumbnail(url = "https://b.thumbs.redditmedia.com/zgZBtjEP0iu9OWnybsjd1YqBehlb-c9dfqee1rXitbs.png") 
    embed1.add_field(name="Field1", value="hi", inline=False)
    embed1.add_field(name="Field2", value="hi2", inline=False)
    embed2 = nextcord.Embed(url = "https://www.nytimes.com/games/wordle/index.html")
    embed2.set_image(url = "https://b.thumbs.redditmedia.com/zgZBtjEP0iu9OWnybsjd1YqBehlb-c9dfqee1rXitbs.png")
    embed = [embed1, embed2]
    # await interaction.send("https://b.thumbs.redditmedia.com/zgZBtjEP0iu9OWnybsjd1YqBehlb-c9dfqee1rXitbs.png")
    await interaction.send(embed = embed1)
    await interaction.send(embed = embed2)

    # Could I do vote = await.interaction.send() instead to get the message???
    async for message in interaction.channel.history():
        if not message.embeds:
            continue
        if message.embeds[0].title == embed1.title:
            vote = message
            break
    else:
        # something broke
        return

    await vote.add_reaction("⬆")
    await vote.add_reaction("⬇")
    #await countdown(5)
    #await interaction.send(vote.reactions)
    await asyncio.sleep(5)
    cache_msg = await vote.channel.fetch_message(vote.id)
   # cache_msg = nextcord.utils.get(bot.cached_messages, id=vote.id)

    await interaction.send(cache_msg.reactions)

    for x in cache_msg.reactions: 
        if x.emoji == "⬆":
            upArrow = x.count
        if x.emoji == "⬇":
            downArrow = x.count
    
    await interaction.send(f'{upArrow} and {downArrow}')



    # reactionUpCounter = nextcord.utils.get(vote.reactions, emoji = "⬆")

    # await interaction.send(f'Hello: {reactionUpCounter.count}')

bot.run("ODE4NzI2NjM3Njc5NTQyMzAy.GnOr3S.77Rzd3laFRDurb41cz3piRi25ccXWjElMk-3MA")
