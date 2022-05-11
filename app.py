from webbrowser import get
import nextcord
import time
import asyncio
from functions import *
from nextcord.ext import commands
from nextcord import Intents, Interaction, SlashOption

intents = Intents.all()
bot = commands.Bot(intents=intents)

@bot.slash_command(
    name="play",
    description="Higher or Lower - Reddit edition!",
    guild_ids=[425353150250221601]
)
async def ex2(interaction: Interaction):
    await interaction.send("Click the up arrow if you think the second subreddit has more members than the first, and the down arrow if you think it has fewer members")
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
    embed1.set_image(url = first_sub.pic) 
    tempStr =  first_sub.subreddit + ", {}\n".format(first_sub.subscribers)
    embed1.add_field(name="Reddit 1", value=tempStr, inline=False)

    #pick the second sub
    second_sub = get_rand_sub(num_subs, sub_data)
    ensure_difference(num_subs, sub_data, first_sub, second_sub)

    embed2 = nextcord.Embed()
    embed2.set_image(url = second_sub.pic)
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

    t = 10
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        embed2 = nextcord.Embed()
        embed2.set_image(url = second_sub.pic)
        tempStr =  second_sub.subreddit + "\n"
        embed2.add_field(name="Reddit 2", value=tempStr, inline=False)
        embed2.add_field(name="Timer", value=timer, inline=False)
        await vote.edit(embed = embed2)
        await asyncio.sleep(1)
        t -= 1
    
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
        print("L + ratio + game ended")
        embed1.add_field(name="Answer", value=tempStr, inline=False)
        tempStr = "Game Over, your score: {}".format(score)
        embed1.add_field(name="Result", value=tempStr, inline=False)
        await cache_msg.edit(embed = embed1)
    
    else:           #the guess was right! continue the game
        while(result):
            score +=1

            result = False

            #generate new subreddit
            first_sub = second_sub
            embed1 = nextcord.Embed(title="Higher Or Lower Reddit Edition")
            embed1.set_image(url =  first_sub.pic) 
            tempStr =  first_sub.subreddit + ", {}\n".format(first_sub.subscribers)
            embed1.add_field(name="Reddit 1", value=tempStr, inline=False)
            await original.edit(embed = embed1)


            second_sub = get_rand_sub(num_subs, sub_data)
            ensure_difference(num_subs, sub_data, first_sub, second_sub)
            tempStr = "Correct! Your score: {}\n".format(score)
            embed1 = nextcord.Embed(title=tempStr)
            embed1.set_image(url = second_sub.pic)
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

            t = 10
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                embed2 = nextcord.Embed()
                embed2.set_image(url = second_sub.pic)
                tempStr =  second_sub.subreddit + "\n"
                embed2.add_field(name="Reddit 2", value=tempStr, inline=False)
                embed2.add_field(name="Timer", value=timer, inline=False)
                await vote.edit(embed = embed2)
                await asyncio.sleep(1)
                t -= 1

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
        embed1.add_field(name="Answer", value=tempStr, inline=False)
        tempStr = "Game Over, your score: {}".format(score)
        embed1.add_field(name="Result", value=tempStr, inline=False)
        await cache_msg.edit(embed = embed1)
        #END OF GAME#

@bot.slash_command(
    name="update",
    description="Update Data",
    guild_ids=[425353150250221601]
    )
async def ex3(interaction: Interaction):
    await interaction.send(f'updating...')
    call()
    await interaction.send(f'Done updating')


@bot.slash_command(
    name="load_up",
    description="Fetch reddit posts",
    guild_ids=[425353150250221601]
    )
async def ex4(interaction: Interaction, 
    subreddit: str = SlashOption(
        name="subreddit",
        description="Choose a subreddit",
        required=True # this doesnt work. returns a SlashOption, not a str
    ),
    category: str = SlashOption(
        name="category",
        description="Choose a category",
        required=True,
        choices=["new", "hot", "rising", "top"],
    ), top: str = SlashOption(
        name="category",
        description="Choose a time for filtering 'top'",
        required=False,
        choices=["new", "hot", "rising", "top"],
    ),):
    get_sub_posts(subreddit,category)
    await interaction.send("filler for the load_up command")


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)