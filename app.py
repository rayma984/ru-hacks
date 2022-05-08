import nextcord
import time
import asyncio
from functions import *
from nextcord.ext import commands
from nextcord import Intents, Interaction

import os
from dotenv import load_dotenv
load_dotenv()
#we can remove the above block if you import functions.py (redundancy)
TOKEN = os.getenv("TOKEN")

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
    
    sub_data = []

    into_list(sub_data, "list of subs.txt")
    # mergeSort(data)
    print_to_file(sub_data,"sorted.txt")

    score = 0

    #await interaction.send("Game Start!")

    #pick a random entry from sub_data
    num_subs = len(sub_data)
    first_sub = get_rand_sub(num_subs, sub_data)

    embed1 = nextcord.Embed(title="Higher Or Lower Reddit Edition")
    embed1.set_image(url = "https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?width=640&crop=smart&auto=webp&s=bfd318557bf2a5b3602367c9c4d9cd84d917ccd5") 
    tempStr =  first_sub.subreddit + ", {}\n".format(first_sub.subscribers)
    embed1.add_field(name="Reddit 1", value=tempStr, inline=False)

    #pick the second sub
    second_sub = get_rand_sub(num_subs, sub_data)
    ensure_difference(num_subs, sub_data, first_sub, second_sub)

    embed2 = nextcord.Embed()
    embed2.set_image(url = "https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?width=640&crop=smart&auto=webp&s=bfd318557bf2a5b3602367c9c4d9cd84d917ccd5")
    tempStr =  second_sub.subreddit + "\n"
    embed2.add_field(name="Reddit 2", value=tempStr, inline=False)

    await interaction.send(embed = embed1)
    await interaction.send(embed = embed2)

    async for message in interaction.channel.history():
        if not message.embeds:
            continue
        if message.embeds[0].title == embed2.title:
            vote = message
            break
    else:
        # something broke
        return

    async for message in interaction.channel.history():
        if not message.embeds:
            continue
        if message.embeds[0].title == embed1.title:
            original = message
            break
    else:
        # something broke
        return 

    await vote.add_reaction("⬆")
    await vote.add_reaction("⬇")

    await asyncio.sleep(10)
    cache_msg = await vote.channel.fetch_message(vote.id)

    for x in cache_msg.reactions: 
        if x.emoji == "⬆":
            upArrow = x.count
        if x.emoji == "⬇":
            downArrow = x.count

    if upArrow > downArrow:
        resp = "2"
    elif downArrow > upArrow:
        resp = "1"
    else: 
        resp = "1"

    result = handle_response(resp, first_sub, second_sub)

    if(not result): #the guess was wrong
        embed1 = nextcord.Embed(title="Higher Or Lower Reddit Edition")
        tempStr = "Incorrect! {} has {} subscribers".format(second_sub.subreddit, second_sub.subscribers)
        embed1.add_field(name="Field1", value=tempStr, inline=False)
        tempStr = "Game Over, your score: {}".format(score)
        embed1.add_field(name="Field2", value=tempStr, inline=False)
        await cache_msg.edit(embed = embed1)
    
    else:           #the guess was right! continue the game
        while(result):
            score +=1

            result = False

            #generate new subreddit
            first_sub = second_sub
            embed1 = nextcord.Embed(title="Higher Or Lower Reddit Edition")
            embed1.set_image(url = "https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?width=640&crop=smart&auto=webp&s=bfd318557bf2a5b3602367c9c4d9cd84d917ccd5") 
            tempStr =  first_sub.subreddit + ", {}\n".format(first_sub.subscribers)
            embed1.add_field(name="Reddit 1", value=tempStr, inline=False)
            await original.edit(embed = embed1)


            second_sub = get_rand_sub(num_subs, sub_data)
            ensure_difference(num_subs, sub_data, first_sub, second_sub)
            tempStr = "Correct! Your score: {}\n".format(score)
            embed1 = nextcord.Embed(title=tempStr)
            embed1.set_image(url = "https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?width=640&crop=smart&auto=webp&s=bfd318557bf2a5b3602367c9c4d9cd84d917ccd5")
            tempStr =  second_sub.subreddit + "\n"
            embed1.add_field(name="Reddit 2", value=tempStr, inline=False)
            await cache_msg.edit(embed = embed1)

            cache_msg = await vote.channel.fetch_message(vote.id)
            for x in cache_msg.reactions: 
                for user in await x.users().flatten():
                    if user != bot.user: #check if the user is the bot, might be slightly different for you
                        await x.remove(user)
            await vote.add_reaction("⬆")
            await vote.add_reaction("⬇")

            await asyncio.sleep(10)
            cache_msg = await vote.channel.fetch_message(vote.id)

            for x in cache_msg.reactions: 
                if x.emoji == "⬆":
                    upArrow = x.count
                if x.emoji == "⬇":
                    downArrow = x.count

            if upArrow > downArrow:
                resp = "2"
            elif downArrow > upArrow:
                resp = "1"
            else: 
                resp = "1"

            result = handle_response(resp, first_sub, second_sub)
        
        #player has died
        embed1 = nextcord.Embed(title="Higher Or Lower Reddit Edition")
        tempStr = "Incorrect! {} has {} subscribers".format(second_sub.subreddit, second_sub.subscribers)
        embed1.add_field(name="Field1", value=tempStr, inline=False)
        tempStr = "Game Over, your score: {}".format(score)
        embed1.add_field(name="Field2", value=tempStr, inline=False)
        await cache_msg.edit(embed = embed1)
        #END OF GAME#

bot.run(TOKEN)
