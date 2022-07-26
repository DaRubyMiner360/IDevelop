import json
import discord
from discord.ext import commands, tasks
from discord import app_commands
from paginator import PaginatorSession


class Channels(commands.Cog):
    '''Channel commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_subcommand=True)
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title=
                "Usage: ~channel <add|remove|clear|list> <idea|bugreport|commission|logs> <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

    @channel.group(invoke_without_subcommand=True, aliases=['set'])
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title=
                "Usage: ~channel add <idea|bugreport|commission|logs> <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

    @add.command(name='idea')
    async def add_idea_channel(self,
                               ctx,
                               channel: discord.TextChannel = None,
                               project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif channel is None:
            embed = discord.Embed(
                title="Usage: ~channel add idea <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        idea_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "idea" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["idea"] = {}
        idea_channels = data[str(
            ctx.message.guild.id)]["projects"][project_id]["channels"]["idea"]

        if channel.id in idea_channels:
            embed = discord.Embed(
                title=f"{channel.mention} is already an idea channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        idea_channels.append(channel.id)
        data[str(ctx.message.guild.id)]["channels"]["idea"] = idea_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully added {channel.mention} as an idea channel.")

    @add.command(
        name='bugreport',
        aliases=['bug-report', 'bugreports', 'bug-reports', 'bug', 'bugs'])
    async def add_bugreport_channel(self,
                                    ctx,
                                    channel: discord.TextChannel = None,
                                    project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif channel is None:
            embed = discord.Embed(
                title="Usage: ~channel add bugreport <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        bugreport_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "bugreport" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["bugreport"] = {}
        bugreport_channels = data[str(
            ctx.message.guild.id
        )]["projects"][project_id]["channels"]["bugreport"]

        if channel.id in bugreport_channels:
            embed = discord.Embed(
                title=f"{channel.mention} is already a bug report channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        bugreport_channels.append(channel.id)
        data[str(ctx.message.guild.id
                 )]["channels"]["bugreport"] = bugreport_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully added {channel.mention} as a bug report channel.")

    @add.command(name='commission',
                 aliases=['commissions', 'request', 'requests'])
    async def add_commission_channel(self,
                                     ctx,
                                     channel: discord.TextChannel = None,
                                     project_id=""):
        if channel is None:
            embed = discord.Embed(
                title="Usage: ~channel add commission <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        commission_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["commission"] = {}
            commission_channels = data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["commission"]
        else:
            if "channels" not in data[str(ctx.message.guild.id)]:
                data[str(ctx.message.guild.id)]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id)]["channels"]["commission"] = {}
            commission_channels = data[str(
                ctx.message.guild.id)]["channels"]["commission"]

        if channel.id in commission_channels:
            embed = discord.Embed(
                title=f"{channel.mention} is already a commission channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        commission_channels.append(channel.id)
        if project_id != "":
            data[str(ctx.message.guild.id)]["projects"][project_id][
                "channels"]["commission"] = commission_channels
        else:
            data[str(ctx.message.guild.id
                     )]["channels"]["commission"] = commission_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully added {channel.mention} as a commission channel.")

    @add.command(name='logs', aliases=['log', 'logging'])
    async def add_logs_channel(self,
                               ctx,
                               channel: discord.TextChannel = None,
                               project_id=""):
        if channel is None:
            embed = discord.Embed(
                title="Usage: ~channel add logs <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        log_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"]["log"] = {}
            log_channels = data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["log"]
        else:
            if "channels" not in data[str(ctx.message.guild.id)]:
                data[str(ctx.message.guild.id)]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id)]["channels"]["log"] = {}
            log_channels = data[str(ctx.message.guild.id)]["channels"]["log"]

        if channel.id in log_channels:
            embed = discord.Embed(
                title=f"{channel.mention} is already a logs channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        log_channels.append(channel.id)
        if project_id != "":
            data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["log"] = log_channels
        else:
            data[str(ctx.message.guild.id)]["channels"]["log"] = log_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully added {channel.mention} as a logs channel.")

    @channel.group(invoke_without_subcommand=True,
                   aliases=['rem', 'delete', 'del'])
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title=
                "Usage: ~channel remove <idea|bugreport|commission|logs> <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

    @remove.command(name='idea')
    async def remove_idea_channel(self,
                                  ctx,
                                  channel: discord.TextChannel = None,
                                  project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif channel is None:
            embed = discord.Embed(
                title="Usage: ~channel remove idea <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        idea_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "idea" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["idea"] = {}
        idea_channels = data[str(
            ctx.message.guild.id)]["projects"][project_id]["channels"]["idea"]

        if channel.id not in idea_channels:
            embed = discord.Embed(
                title=f"{channel.mention} isn't an idea channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        idea_channels.remove(channel.id)
        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["channels"]["idea"] = idea_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully removed {channel.mention} from being an idea channel."
        )

    @remove.command(
        name='bugreport',
        aliases=['bug-report', 'bugreports', 'bug-reports', 'bug', 'bugs'])
    async def remove_bugreport_channel(self,
                                       ctx,
                                       channel: discord.TextChannel = None,
                                       project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif channel is None:
            embed = discord.Embed(
                title="Usage: ~channel remove bugreport <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        bugreport_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "bugreport" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["bugreport"] = {}
        bugreport_channels = data[str(
            ctx.message.guild.id
        )]["projects"][project_id]["channels"]["bugreport"]

        if channel.id not in bugreport_channels:
            embed = discord.Embed(
                title=f"{channel.mention} isn't a bug report channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        bugreport_channels.remove(channel.id)
        data[str(ctx.message.guild.id)]["projects"][project_id]["channels"][
            "bugreport"] = bugreport_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully removed {channel.mention} from being a bug report channel."
        )

    @remove.command(name='commission',
                    aliases=['commissions', 'request', 'requests'])
    async def remove_commission_channel(self,
                                        ctx,
                                        channel: discord.TextChannel = None,
                                        project_id=""):
        if channel is None:
            embed = discord.Embed(
                title="Usage: ~channel remove logs <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        commission_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["commission"] = {}
            commission_channels = data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["commission"]
        else:
            if "channels" not in data[str(ctx.message.guild.id)]:
                data[str(ctx.message.guild.id)]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id)]["channels"]["commission"] = {}
            commission_channels = data[str(
                ctx.message.guild.id)]["channels"]["commission"]

        if channel.id not in commission_channels:
            embed = discord.Embed(
                title=f"{channel.mention} isn't a commission channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        commission_channels.remove(channel.id)
        data[str(ctx.message.guild.id)]["projects"][project_id]["channels"][
            "commission"] = commission_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully removed {channel.mention} from being a commission channel."
        )

    @remove.command(name='logs', aliases=['log', 'logging'])
    async def remove_logs_channel(self,
                                  ctx,
                                  channel: discord.TextChannel = None,
                                  project_id=""):
        if channel is None:
            embed = discord.Embed(
                title="Usage: ~channel remove logs <channel> [project]",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

        log_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"]["log"] = {}
            log_channels = data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["log"]
        else:
            if "channels" not in data[str(ctx.message.guild.id)]:
                data[str(ctx.message.guild.id)]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id)]["channels"]["log"] = {}
            log_channels = data[str(ctx.message.guild.id)]["channels"]["log"]

        if channel.id not in log_channels:
            embed = discord.Embed(
                title=f"{channel.mention} isn't a logs channel!",
                color=0x64c466)
            await ctx.send(embed=embed)
            return
        log_channels.remove(channel.id)
        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["channels"]["log"] = log_channels

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(
            f"Successfully removed {channel.mention} from being a logs channel."
        )

    @channel.group(invoke_without_subcommand=True)
    async def clear(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Usage: ~channel clear <idea|bugreport|commission|logs>",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

    @clear.command(name='idea')
    async def clear_idea_channel(self, ctx, project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return

        idea_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "idea" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["idea"] = {}
        idea_channels = data[str(
            ctx.message.guild.id)]["projects"][project_id]["channels"]["idea"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["channels"]["idea"] = []

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        if len(idea_channels) == 1:
            await ctx.send(
                f"Successfully removed {len(idea_channels)} idea channel.")
        else:
            await ctx.send(
                f"Successfully removed {len(idea_channels)} idea channels.")

    @clear.command(name='bugreport')
    async def clear_bugreport_channel(self, ctx, project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return

        bugreport_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "bugreport" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["bugreport"] = {}
        bugreport_channels = data[str(
            ctx.message.guild.id
        )]["projects"][project_id]["channels"]["bugreport"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["channels"]["bugreport"] = []

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        if len(bugreport_channels) == 1:
            await ctx.send(
                f"Successfully removed {len(bugreport_channels)} bug report channel."
            )
        else:
            await ctx.send(
                f"Successfully removed {len(bugreport_channels)} bug report channels."
            )

    @clear.command(name='commission',
                   aliases=['commissions', 'request', 'requests'])
    async def clear_commission_channel(self, ctx, project_id=""):
        commission_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["commission"] = {}
            commission_channels = data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["commission"]
        else:
            if "channels" not in data[str(ctx.message.guild.id)]:
                data[str(ctx.message.guild.id)]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id)]["channels"]["commission"] = {}
            commission_channels = data[str(
                ctx.message.guild.id)]["channels"]["commission"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["channels"]["commission"] = []

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        if len(commission_channels) == 1:
            await ctx.send(
                f"Successfully removed {len(commission_channels)} commission channel."
            )
        else:
            await ctx.send(
                f"Successfully removed {len(commission_channels)} commission channels."
            )

    @clear.command(name='logs', aliases=['log', 'logging'])
    async def clear_logs_channel(self, ctx, project_id=""):
        log_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"]["log"] = {}
            log_channels = data[str(
                ctx.message.guild.id
            )]["projects"][project_id]["channels"]["log"]
        else:
            if "channels" not in data[str(ctx.message.guild.id)]:
                data[str(ctx.message.guild.id)]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id)]["channels"]["log"] = {}
            log_channels = data[str(ctx.message.guild.id)]["channels"]["log"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["channels"]["log"] = []

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        if len(log_channels) == 1:
            await ctx.send(
                f"Successfully removed {len(log_channels)} log channel.")
        else:
            await ctx.send(
                f"Successfully removed {len(log_channels)} log channels.")

    @channel.group(invoke_without_subcommand=True,
                   aliases=['display', 'show', '?'])
    async def list(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Usage: ~channel list <idea|bugreport|commission|logs>",
                color=0x64c466)
            await ctx.send(embed=embed)
            return

    @list.command(name='idea')
    async def list_idea_channel(self, ctx, project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return

        idea_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "idea" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["idea"] = {}
        idea_channels = data[str(
            ctx.message.guild.id)]["projects"][project_id]["channels"]["idea"]

        if len(idea_channels) > 0:
            pages = []
            max_per_page = 7
            full_page_count = int(len(idea_channels) / max_per_page)
            remaining_item_count = len(idea_channels) % max_per_page
            index = 0
            for i in range(full_page_count + 1):
                if i == full_page_count and remaining_item_count == 0:
                    break
                em = discord.Embed(title="Idea Channels",
                                   description=f"Page {i + 1}",
                                   colour=0xFF0000)
                if remaining_item_count > 0:
                    item_count = remaining_item_count
                else:
                    item_count = max_per_page
                for o in range(item_count):
                    em.add_field(name="\u200b",
                                 value=self.bot.get_channel(
                                     int(idea_channels[index])).mention)
                    index += 1
                pages.append(em)

            p_session = PaginatorSession(ctx, bot=self.bot, pages=pages)
            await p_session.run()
        else:
            em = discord.Embed(title="Idea Channels",
                               description="Page 1",
                               colour=0xFF0000)
            em.add_field(name="No Idea Channels", value="\u200b")
            await ctx.channel.send(embed=em)

    @list.command(name='bugreport')
    async def list_bugreport_channel(self, ctx, project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return

        bugreport_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "bugreport" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"]["bugreport"] = {}
        bugreport_channels = data[str(
            ctx.message.guild.id
        )]["projects"][project_id]["channels"]["bugreport"]

        if len(bugreport_channels) > 0:
            pages = []
            max_per_page = 7
            full_page_count = int(len(bugreport_channels) / max_per_page)
            remaining_item_count = len(bugreport_channels) % max_per_page
            index = 0
            for i in range(full_page_count + 1):
                if i == full_page_count and remaining_item_count == 0:
                    break
                em = discord.Embed(title="Bug Report Channels",
                                   description=f"Page {i + 1}",
                                   colour=0xFF0000)
                if remaining_item_count > 0:
                    item_count = remaining_item_count
                else:
                    item_count = max_per_page
                for o in range(item_count):
                    em.add_field(name="\u200b",
                                 value=self.bot.get_channel(
                                     int(bugreport_channels[index])).mention)
                    index += 1
                pages.append(em)

            p_session = PaginatorSession(ctx, bot=self.bot, pages=pages)
            await p_session.run()
        else:
            em = discord.Embed(title="Bug Report Channels",
                               description="Page 1",
                               colour=0xFF0000)
            em.add_field(name="No Bug Report Channels", value="\u200b")
            await ctx.channel.send(embed=em)

    @list.command(name='commission',
                  aliases=['commissions', 'request', 'requests'])
    async def list_commission_channel(self, ctx, project_id=""):
        commission_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "commission" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id)]["channels"]["commission"] = {}
        commission_channels = data[str(
            ctx.message.guild.id)]["channels"]["commission"]
        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "commission" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["commission"] = {}
            commission_channels.extend(data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]
                                       ["commission"])

        if len(commission_channels) > 0:
            pages = []
            max_per_page = 7
            full_page_count = int(len(commission_channels) / max_per_page)
            remaining_item_count = len(commission_channels) % max_per_page
            index = 0
            for i in range(full_page_count + 1):
                if i == full_page_count and remaining_item_count == 0:
                    break
                em = discord.Embed(title="Commission Channels",
                                   description=f"Page {i + 1}",
                                   colour=0xFF0000)
                if remaining_item_count > 0:
                    item_count = remaining_item_count
                else:
                    item_count = max_per_page
                for o in range(item_count):
                    em.add_field(name="\u200b",
                                 value=self.bot.get_channel(
                                     int(commission_channels[index])).mention)
                    index += 1
                pages.append(em)

            p_session = PaginatorSession(ctx, bot=self.bot, pages=pages)
            await p_session.run()
        else:
            em = discord.Embed(title="Commission Channels",
                               description="Page 1",
                               colour=0xFF0000)
            em.add_field(name="No Commission Channels", value="\u200b")
            await ctx.channel.send(embed=em)

    @list.command(name='logs', aliases=['log', 'logging'])
    async def list_logs_channel(self, ctx, project_id=""):
        log_channels = []
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "log" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id)]["channels"]["log"] = {}
        log_channels = data[str(ctx.message.guild.id)]["channels"]["log"]
        if project_id != "":
            if "channels" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"] = {}
            if "log" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["channels"]["log"] = {}
            log_channels.extend(data[str(ctx.message.guild.id)]["projects"]
                                [project_id]["channels"]["log"])

        if len(log_channels) > 0:
            pages = []
            max_per_page = 7
            full_page_count = int(len(log_channels) / max_per_page)
            remaining_item_count = len(log_channels) % max_per_page
            index = 0
            for i in range(full_page_count + 1):
                if i == full_page_count and remaining_item_count == 0:
                    break
                em = discord.Embed(title="Log Channels",
                                   description=f"Page {i + 1}",
                                   colour=0xFF0000)
                if remaining_item_count > 0:
                    item_count = remaining_item_count
                else:
                    item_count = max_per_page
                for o in range(item_count):
                    em.add_field(name="\u200b",
                                 value=self.bot.get_channel(
                                     int(log_channels[index])).mention)
                    index += 1
                pages.append(em)

            p_session = PaginatorSession(ctx, bot=self.bot, pages=pages)
            await p_session.run()
        else:
            em = discord.Embed(title="Log Channels",
                               description="Page 1",
                               colour=0xFF0000)
            em.add_field(name="No Log Channels", value="\u200b")
            await ctx.channel.send(embed=em)


async def setup(bot):
    await bot.add_cog(Channels(bot))
    """
    log_channels = []
    data = {}
    with open('databases/ideas.json', 'r') as file:
        data = json.load(file)
    if str(ctx.message.guild.id) not in data:
        data[str(ctx.message.guild.id)] = {}
    if "projects" not in data[str(ctx.message.guild.id)]:
        data[str(ctx.message.guild.id)]["projects"] = {}
    if project_id != "" and project_id not in data[str(ctx.message.guild.id)]["projects"]:
        await ctx.send("A project with that ID doesn't exist!")
        await ctx.message.delete()
        return
    if "channels" not in data[str(ctx.message.guild.id)]:
        data[str(ctx.message.guild.id)]["channels"] = {}
    if "log" not in data[str(ctx.message.guild.id)]["projects"][project_id]["channels"]:
        data[str(ctx.message.guild.id)]["channels"]["log"] = {}
    log_channels = data[str(ctx.message.guild.id)]["channels"]["log"]
    if project_id != "":
        if "channels" not in data[str(ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id)]["projects"][project_id]["channels"] = {}
        if "log" not in data[str(ctx.message.guild.id)]["projects"][project_id]["channels"]:
            data[str(ctx.message.guild.id)]["projects"][project_id]["channels"]["log"] = {}
        log_channels.extend(data[str(ctx.message.guild.id)]["projects"][project_id]["channels"]["log"])
    """
