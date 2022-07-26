import os
import sys
from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Greedy
from discord import app_commands, Object
from typing import Optional, Literal
import asyncio
import random
import traceback
import inspect
from paginator import PaginatorSession

#import neverSleep

#neverSleep.awake(
#    f"https://{str(os.environ['REPL_SLUG']).lower()}.{str(os.environ['REPL_OWNER']).lower()}.repl.co",
#    True)

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('~'),
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents)

bot.author_id = 920305118535094304
bot.remove_command('help')


@bot.hybrid_command()
async def invite(ctx: commands.Context):
    '''Gives you an invite link for the bot'''

    await ctx.send(
        'https://discord.com/api/oauth2/authorize?client_id=966342595557089400&permissions=8&scope=bot%20applications.commands',
    )


async def send_cmd_help(ctx):
    cmd = ctx.command
    em = discord.Embed(title=f'Usage: {ctx.prefix + cmd.signature}')
    em.color = discord.Color.green()
    em.description = cmd.help
    return em


def format_command_help(prefix, cmd):
    '''Format help for a command'''
    color = discord.Color.green()
    em = discord.Embed(color=color, description=cmd.help)

    if hasattr(cmd, 'invoke_without_command') and cmd.invoke_without_command:
        em.title = f'`Usage: {prefix}{cmd.signature}`'
    else:
        em.title = f'`{prefix}{cmd.signature}`'

    return em


def format_cog_help(prefix, cog):
    '''Format help for a cog'''
    signatures = []
    color = discord.Color.green()
    em = discord.Embed(color=color, description=f'*{inspect.getdoc(cog)}*')
    em.title = type(cog).__name__.replace('_', ' ')
    cc = []
    for cmd in bot.commands:
        if not cmd.hidden:
            if cmd.cog is cog:
                cc.append(cmd)
                signatures.append(len(cmd.name) + len(prefix))
    max_length = max(signatures)
    abc = sorted(cc, key=lambda x: x.name)
    cmds = ''
    for c in abc:
        cmds += f'`{prefix + c.name:<{max_length}} '
        cmds += f'{c.short_doc:<{max_length}}`\n'
    em.add_field(name='Commands', value=cmds)

    return em


def format_bot_help(prefix):
    signatures = []
    fmt = ''
    commands = []
    for cmd in bot.commands:
        if not cmd.hidden:
            if type(cmd.cog).__name__ == 'NoneType':
                commands.append(cmd)
                signatures.append(len(cmd.name) + len(prefix))
    max_length = max(signatures)
    abc = sorted(commands, key=lambda x: x.name)
    for c in abc:
        fmt += f'`{prefix + c.name:<{max_length}} '
        fmt += f'{c.short_doc:<{max_length}}`\n'
    em = discord.Embed(title='Bot', color=discord.Color.green())
    em.description = '*Commands for the main bot.*'
    em.add_field(name='Commands', value=fmt)

    return em


@bot.command()
async def help(ctx: commands.Context, *, command: str = None):
    '''Shows this message'''

    if command is not None:
        cog = bot.get_cog(command.replace(' ', '_').title())
        cmd = bot.get_command(command)
        if cog is not None:
            em = format_cog_help(ctx.prefix, cog)
        elif cmd is not None:
            em = format_command_help(ctx.prefix, cmd)
        else:
            await ctx.send('No commands found.')
        return await ctx.send(embed=em)

    pages = []
    for cog in bot.cogs.values():
        em = format_cog_help(ctx.prefix, cog)
        pages.append(em)
    em = format_bot_help(ctx.prefix)
    pages.append(em)

    p_session = PaginatorSession(
        ctx,
        bot=bot,
        footer=f'Type {ctx.prefix}help command for more info on a command.',
        pages=pages)
    await p_session.run()


@bot.command()
@commands.is_owner()
async def sync(self,
               ctx: commands.Context,
               guilds: Greedy[Object],
               spec: Optional[Literal["~"]] = None) -> None:
    if not guilds:
        if spec == "~":
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        else:
            fmt = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(fmt)} commands {'globally' if spec is not None else 'to the current guild.'}"
        )
        return

    assert guilds is not None
    fmt = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            fmt += 1

    await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")


@bot.event
async def setup_hook():
    #await bot.tree.sync()
    if __name__ == '__main__':  # Ensures this is the file being
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[: -3]}'
                                         )  #Loads every extension.


@bot.event
async def on_ready():  # When the bot is ready
    status_change.start()
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.event
async def on_command_error(ctx, error):
    send_help = (commands.MissingRequiredArgument, commands.BadArgument,
                 commands.TooManyArguments, commands.UserInputError)

    if isinstance(error, commands.CommandNotFound):  # fails silently
        pass

    elif isinstance(error, send_help):
        _help = await send_cmd_help(ctx)
        await ctx.send(embed=_help)

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f'This command is on cooldown. Please wait {error.retry_after:.2f}s'
        )

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions to use this command.')

    else:
        print(''.join(
            traceback.format_exception(type(error), error,
                                       error.__traceback__)))


seconds_between_changes = 240
presence_index = 1


@tasks.loop(seconds=seconds_between_changes)
async def status_change():
    global presence_index

    if random.randint(1, seconds_between_changes) == 1:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="https://m.youtube.com/watch?v=oHg5SJYRHA0"))
        return

    index = presence_index + 1
    if presence_index == 1:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing, name="Cloud"))
    elif presence_index == 2:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="The Celestial Reawakening Soundtrack"))
    elif presence_index == 3:
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing, name="Spirit"))
    else:
        rand = random.randint(1, 4)
        if rand == 1:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching, name="for ~help"))
        elif rand == 2:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening, name="~help"))
        elif rand == 3:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.custom, name="Waiting for ~help"))
        else:
            await bot.change_presence(activity=discord.Activity(
                type=discord.ActivityType.competing, name="'~idea's"))
        index = 1
    presence_index = index


if "nowebserver" not in sys.argv:
    keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
# try:
#     bot.run(token)  # Starts the bot
# except discord.errors.HTTPException:
#     print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
#     os.system("python restarter.py")
#     os.system('kill 1')
