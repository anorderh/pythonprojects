import discord
import asyncio
from discord.ext import commands
import requests
import random
import sys
import json

# commands from discord.extended to make Bot(), subclass of Client()
# asyncio for waiting

TOKEN = ""  # USE OWN KEY
TENOR_KEY = ""  # USE OWN KEY
example_link = "https://g.tenor.com/v1/search?q=excited&key=LIVDSRZULELA&limit=50"  # debug, on api page
bot_channel = ""  # assigns what channel bot operates in, not being used

client = commands.Bot(command_prefix='!')
last_gif_url = None
favorited = {}


@client.event
async def on_ready():
    print("{0.user} is online!".format(client))
    print("Bot ID: {0.user.id}\n".format(client))


@client.event
async def on_message(ctx):
    channel = str(ctx.channel)
    author = str(ctx.author).split('#')[0]
    content = str(ctx.content)

    print(f'{channel} | {author}: {content}')
    await client.process_commands(ctx)


async def speak(ctx, msg: str, time=0):
    async with ctx.typing():
        await asyncio.sleep(time)
    await ctx.send(msg)
    await ctx.author.send('beep')  # used for getting discord "ping" sound


async def gif_info(input_url):
    keywords = input_url.replace('https://tenor.com/view/', '').split('-')
    del keywords[-1]

    return [' '.join(keywords[0:3]), input_url]


@client.command()
async def gif(ctx):
    global last_gif_url
    # default values
    queued = 5  # 50 -> MAX
    search = "hooray"
    user_input = list(filter(None, str(ctx.message.content).replace("!gif", "").split(" ")))

    if len(user_input) != 0:
        last_term = user_input[-1]
        if last_term.isdigit() and (50 >= int(last_term) > 0):
            queued = int(user_input.pop())

        search = ' '.join(user_input)

    # requests.get() retrieves Request object, containing decoded info from website server
    request = requests.get(
        f"https://g.tenor.com/v1/search?q={search}&key={TENOR_KEY}&limit={queued}" +
        '&media_filter=minimal')

    # built-in JSON decoder in Requests, converts any JSON data present in Request object into Python dict
    py_dict = request.json()
    gif_list = [entry['itemurl'] for entry in py_dict['results']]  # creating a list of found URLs

    # based on gifs queued, randomly-accesses indexed URL for variety
    random.seed()
    gif_url = gif_list[random.randint(0, queued - 1)]

    await speak(ctx, gif_url)
    last_gif_url = gif_url


@client.command()
async def save_gif(ctx):
    active_user = str(ctx.author).split('#')[0]

    if last_gif_url is None:
        await speak(ctx, f"{active_user}, no gifs have been used yet.")
        return
    elif last_gif_url in list(favorited.values()):
        await speak(ctx, f'{active_user}, this gif has already been saved.')
        return
    else:
        details = await gif_info(last_gif_url)
        favorited[details[0]] = details[1]

    await speak(ctx, f'{active_user}, "{details[0]}" has been successfully saved!')


@client.command()
async def fav_gifs(ctx):
    if len(favorited) == 0:
        await speak(ctx, "No gifs have been saved yet!")
        return

    await speak(ctx, "Retrieving saved gifs...")

    for title in favorited.keys():
        await speak(ctx, f"\t {title}")


@client.command()
async def use_gif(ctx, keyword):
    if len(favorited) == 0:
        await speak(ctx, "No gifs have been saved yet!")
        return
    elif any(keyword in title for title in favorited.keys()):

        # if keyword does exist in str[], then keyword becomes closest term
        keyword = [title for title in favorited.keys() if keyword in title][0]
        await speak(ctx, favorited[keyword])
    else:
        await speak(ctx, f'"{keyword}" could not be found.')


@client.command()
async def gif_commands(ctx):
    await speak(ctx, "\nCOMMANDS:\n\n" +
                '!gif <keyword> \tOR\t gif "<phrase>"\n\t* posts gif\n' +
                '!save_gif \n\t* saves gif\n' +
                '!fav_gifs \n\t* lists saved gifs\n' +
                '!use_gif <keyword> \tOR\t !use_gif "<phrase>" \n\t * uses saved gif')


client.run(TOKEN)
