import discord, asyncio
from discord.ext import commands
# commands from discord.extended to make Bot(), subclass of Client()
# asyncio for waiting

TOKEN = "" #token hidden, use own
client = commands.Bot(command_prefix='!')


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


async def speak(ctx, msg: str, time: int):
    async with ctx.typing():
        await asyncio.sleep(time)
    await ctx.send(msg)


@client.command()
async def timing(ctx):
    if ctx.channel.name != "bot-fun-2": # Channel name bot talks in
        return

    await speak(ctx, "1 second", 1)
    await speak(ctx, "2 seconds", 2)
    await speak(ctx, "3 seconds", 2)

client.run(TOKEN)