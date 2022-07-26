import json
import discord
from discord.ext import commands, tasks
from discord import app_commands
from paginator import PaginatorSession


class Project(commands.Cog):
    '''Project commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="projectcount",
                      aliases=[
                          'projectamount', 'countprojects', 'projectnumber',
                          'projectnum'
                      ])
    async def project_count(self, ctx):
        projects = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" in data[str(ctx.message.guild.id)]:
            projects = data[str(ctx.message.guild.id)]["projects"]
        if len(projects) == 1:
            await ctx.send(
                f"There has been {len(projects)} project in this server.")
        else:
            await ctx.send(
                f"There have been {len(projects)} project in this server.")
        await ctx.message.delete()

    @commands.command(
        name="ideacount",
        aliases=['ideaamount', 'countideas', 'ideanumber', 'ideanum'])
    async def idea_count(self, ctx, project_id):
        ideas = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "ideas" in data[str(ctx.message.guild.id)]["projects"][project_id]:
            ideas = data[str(
                ctx.message.guild.id)]["projects"][project_id]["ideas"]
        if len(ideas) == 1:
            await ctx.send(f"There has been {len(ideas)} idea in this server.")
        else:
            await ctx.send(
                f"There have been {len(ideas)} ideas in this server.")
        await ctx.message.delete()

    @commands.command(name="bugreportcount",
                      aliases=[
                          'bugcount', 'bugreportamount', 'bugamount',
                          'countbugreports', 'countbugs', 'bugreportnumber',
                          'bugnumber', 'bugreportnum', 'bugnum'
                      ])
    async def bugreport_count(self, ctx, project_id):
        bugreports = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "bugreports" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            bugreports = data[str(
                ctx.message.guild.id)]["projects"][project_id]["bugreports"]
        if len(bugreports) == 1:
            await ctx.send(
                f"There has been {len(bugreports)} bug report in this server.")
        else:
            await ctx.send(
                f"There have been {len(bugreports)} bug reports in this server."
            )
        await ctx.message.delete()

    @commands.command(name="commissioncount",
                      aliases=[
                          'commissionamount', 'countcommission',
                          'commissionnumber', 'commissionnum'
                      ])
    async def commission_count(self, ctx, project_id=""):
        commissions = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id != "" and project_id not in data[str(
                ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "commissions" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["commissions"] = {}
        commissions = data[str(ctx.message.guild.id)]["commissions"]
        if project_id != "":
            if "commissions" not in data[str(
                    ctx.message.guild.id)]["projects"][project_id]:
                data[str(ctx.message.guild.id
                         )]["projects"][project_id]["commissions"] = {}
            commissions.extend(data[str(
                ctx.message.guild.id)]["projects"][project_id]["commissions"])
        if len(commissions) == 1:
            await ctx.send(
                f"There has been {len(commissions)} commission in this server."
            )
        else:
            await ctx.send(
                f"There have been {len(commissions)} commissions in this server."
            )
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def project(self, ctx, id="", name="", description=""):
        if id.strip() == "":
            await ctx.send("Missing project id!")
            return

        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}

        if name.strip() == "":
            if len(data[str(
                    ctx.message.guild.id)]["projects"]) > 0 and id in data[str(
                        ctx.message.guild.id)]["projects"]:
                embed = discord.Embed(title="Successfully added project.",
                                      description="\u200b",
                                      colour=0xFF0000)
                embed.set_thumbnail(
                    url=
                    f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
                )
                embed.add_field(
                    name="Name:",
                    value=data[str(
                        ctx.message.guild.id)]["projects"][id]["name"],
                    inline=False)
                embed.add_field(name="ID:", value=id, inline=False)
                if data[str(ctx.message.guild.id
                            )]["projects"][id]["description"].strip() != "":
                    embed.add_field(name="Description:",
                                    value=data[str(ctx.message.guild.id)]
                                    ["projects"][id]["description"],
                                    inline=False)
                await ctx.send(embed=embed)
                await ctx.message.delete()
            else:
                await ctx.send("Missing project name!")
            return

        if len(data[str(
                ctx.message.guild.id)]["projects"]) > 0 and id in data[str(
                    ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID already exists!")
            await ctx.message.delete()
            return

        embed = discord.Embed(title="Successfully added project.",
                              description="\u200b",
                              colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name="Name:", value=name, inline=False)
        embed.add_field(name="ID:", value=id, inline=False)
        if description.strip() != "":
            embed.add_field(name="Description:",
                            value=description,
                            inline=False)
        await ctx.send(embed=embed)

        data[str(ctx.message.guild.id)]["projects"][id] = {}
        data[str(ctx.message.guild.id)]["projects"][id]["name"] = name
        data[str(
            ctx.message.guild.id)]["projects"][id]["description"] = description
        data[str(ctx.message.guild.id)]["projects"][id]["channels"] = {}
        data[str(
            ctx.message.guild.id)]["projects"][id]["channels"]["idea"] = {}
        data[str(ctx.message.guild.id
                 )]["projects"][id]["channels"]["bugreport"] = {}
        data[str(ctx.message.guild.id
                 )]["projects"][id]["channels"]["commission"] = {}
        data[str(ctx.message.guild.id)]["projects"][id]["channels"]["log"] = {}
        data[str(ctx.message.guild.id)]["projects"][id]["ideas"] = {}
        data[str(ctx.message.guild.id)]["projects"][id]["bugreports"] = {}
        if "channels" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["channels"] = {}
        if "commission" not in data[str(ctx.message.guild.id)]["channels"]:
            data[str(ctx.message.guild.id)]["channels"]["commission"] = {}
        if "log" not in data[str(ctx.message.guild.id)]["channels"]:
            data[str(ctx.message.guild.id)]["channels"]["log"] = {}

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="setprojectname")
    @commands.has_permissions(manage_guild=True)
    async def set_project_name(self, ctx, id="", name=""):
        if id.strip() == "":
            await ctx.send("Missing project id!")
            return
        elif name.strip() == "":
            await ctx.send("Missing new name!")
            return

        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if len(data[str(ctx.message.guild.id)]
               ["projects"]) <= 0 and id not in data[str(
                   ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        embed = discord.Embed(title="Successfully updated project name.",
                              description="\u200b",
                              colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name="Name:", value=name, inline=False)
        embed.add_field(name="ID:", value=id, inline=False)
        if data[str(ctx.message.guild.id
                    )]["projects"][id]["description"].strip() != "":
            embed.add_field(
                name="Description:",
                value=data[str(
                    ctx.message.guild.id)]["projects"][id]["description"],
                inline=False)
        await ctx.send(embed=embed)

        data[str(ctx.message.guild.id)]["projects"][id]["name"] = name

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="setprojectdescription")
    @commands.has_permissions(manage_guild=True)
    async def set_project_description(self, ctx, id="", description=""):
        if id.strip() == "":
            await ctx.send("Missing project id!")
            return

        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if len(data[str(ctx.message.guild.id)]
               ["projects"]) <= 0 and id not in data[str(
                   ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        embed = discord.Embed(title="Successfully updated project name.",
                              description="\u200b",
                              colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name="Name:",
                        value=data[str(
                            ctx.message.guild.id)]["projects"][id]["name"],
                        inline=False)
        embed.add_field(name="ID:", value=id, inline=False)
        if description.strip() != "":
            embed.add_field(name="Description:",
                            value=description,
                            inline=False)
        await ctx.send(embed=embed)

        data[str(
            ctx.message.guild.id)]["projects"][id]["description"] = description

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="projectinfo")
    async def project_info(self, ctx, id=""):
        if id.strip() == "":
            await ctx.send("Missing project id!")
            return

        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if len(data[str(ctx.message.guild.id)]
               ["projects"]) <= 0 and id not in data[str(
                   ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return

        embed = discord.Embed(title=data[str(
            ctx.message.guild.id)]["projects"][id]["name"],
                              description="\u200b",
                              colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name="ID:", value=id, inline=False)
        if description.strip() != "":
            embed.add_field(
                name="Description:",
                value=data[str(
                    ctx.message.guild.id)]["projects"][id]["description"],
                inline=False)
        await ctx.send(embed=embed)

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command()
    async def idea(self, ctx, title="", description="", project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif title.strip() == "":
            await ctx.send("Missing idea name!")
            return
        elif description.strip() == "":
            await ctx.send("Missing idea description!")
            return

        idea_channels = []
        ideas = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            if "idea" in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                idea_channels = data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["idea"]
        if "ideas" in data[str(ctx.message.guild.id)]["projects"][project_id]:
            ideas = data[str(
                ctx.message.guild.id)]["projects"][project_id]["ideas"]

        if len(idea_channels) > 0 and ctx.channel.id not in idea_channels:
            await ctx.message.delete()
            return
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"] = {}
        data[str(
            ctx.message.guild.id)]["projects"][project_id]["ideas"] = ideas

        embed = discord.Embed(
            title=title,
            description=
            f':stopwatch: Vote for idea request **#{len(ideas) + 1}** below!',
            colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name=title, value=description, inline=False)
        message = await ctx.send(embed=embed)

        data[str(ctx.message.guild.id)]["projects"][project_id]["ideas"][
            message.id] = {}
        data[str(ctx.message.guild.id)]["projects"][project_id]["ideas"][
            message.id]["status"] = "open"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Add reactions
        await message.add_reaction("👍")
        await message.add_reaction("👎")

        # Delete user's message
        await ctx.message.delete()

    @commands.command()
    async def bugreport(self, ctx, title="", description="", project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif title.strip() == "":
            await ctx.send("Missing bug report name!")
            return
        elif description.strip() == "":
            await ctx.send("Missing bug report description!")
            return

        # Send message
        bugreport_channels = []
        bugreports = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            if "bugreport" in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                bugreport_channels = data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["bugreport"]
        if "bugreports" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            bugreports = data[str(
                ctx.message.guild.id)]["projects"][project_id]["bugreports"]

        if len(bugreport_channels
               ) > 0 and ctx.channel.id not in bugreport_channels:
            await ctx.message.delete()
            return
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"] = {}
        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["bugreports"] = bugreports

        embed = discord.Embed(
            title=title,
            description=
            f':stopwatch: Vote for bug report priority **#{len(bugreports) + 1}** below!',
            colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name=title, value=description, inline=False)
        message = await ctx.send(embed=embed)

        data[str(ctx.message.guild.id)]["projects"][project_id]["bugreports"][
            message.id] = {}
        data[str(ctx.message.guild.id)]["projects"][project_id]["bugreports"][
            message.id]["status"] = "open"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Add reactions
        await message.add_reaction("👍")
        await message.add_reaction("👎")

        # Delete user's message
        await ctx.message.delete()

    @commands.command()
    async def commission(self,
                         ctx,
                         title="",
                         description="",
                         project_id="",
                         member: discord.Member = None):
        if title.strip() == "":
            await ctx.send("Missing bug report name!")
            return
        elif description.strip() == "":
            await ctx.send("Missing bug report description!")
            return

        # Send message
        bugreport_channels = []
        bugreports = {}
        data = {}
        with open('databases/ideas.json', 'r') as file:
            data = json.load(file)
        if "projects" not in data[str(ctx.message.guild.id)]:
            data[str(ctx.message.guild.id)]["projects"] = {}
        if project_id not in data[str(ctx.message.guild.id)]["projects"]:
            await ctx.send("A project with that ID doesn't exist!")
            await ctx.message.delete()
            return
        if "channels" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            if "bugreport" in data[str(
                    ctx.message.guild.id)]["projects"][project_id]["channels"]:
                bugreport_channels = data[str(
                    ctx.message.guild.id
                )]["projects"][project_id]["channels"]["bugreport"]
        if "bugreports" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            bugreports = data[str(
                ctx.message.guild.id)]["projects"][project_id]["bugreports"]

        if len(bugreport_channels
               ) > 0 and ctx.channel.id not in bugreport_channels:
            await ctx.message.delete()
            return
        if str(ctx.message.guild.id) not in data:
            data[str(ctx.message.guild.id)] = {}
        if "channels" not in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            data[str(ctx.message.guild.id
                     )]["projects"][project_id]["channels"] = {}
        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["bugreports"] = bugreports

        embed = discord.Embed(
            title=title,
            description=
            f':stopwatch: Vote for bug report priority **#{len(bugreports) + 1}** below!',
            colour=0xFF0000)
        embed.set_thumbnail(
            url=
            f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png'
        )
        embed.add_field(name=title, value=description, inline=False)
        message = await ctx.send(embed=embed)

        data[str(ctx.message.guild.id)]["projects"][project_id]["bugreports"][
            message.id] = {}
        data[str(ctx.message.guild.id)]["projects"][project_id]["bugreports"][
            message.id]["status"] = "open"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Add reactions
        await message.add_reaction("👍")
        await message.add_reaction("👎")

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="acceptidea",
                      aliases=['accept', 'approveidea', 'approve'])
    @commands.has_permissions(manage_guild=True)
    async def accept_idea(self, ctx, project_id: str, id: int = None):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif id is None:
            await ctx.send("Missing idea id or its message's id!")
            return

        ideas = {}
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
        if "ideas" in data[str(ctx.message.guild.id)]["projects"][project_id]:
            ideas = data[str(
                ctx.message.guild.id)]["projects"][project_id]["ideas"]

        data[str(
            ctx.message.guild.id)]["projects"][project_id]["ideas"] = ideas

        try:
            if id > len(ideas):
                message_id = str(id)
                idea_number = list(ideas.keys()).index(str(id)) + 1
            else:
                message_id = str(list(ideas.keys())[id - 1])
                idea_number = id

            message = await ctx.fetch_message(message_id)
            embed = message.embeds[0]
            if embed.description.endswith(" **(ACCEPTED)**"):
                embed.description = embed.description[:-15]
            elif embed.description.endswith(" **(DENIED)**"):
                embed.description = embed.description[:-13]
            embed.description = embed.description + " **(ACCEPTED)**"
            await message.edit(embed=embed)

            await ctx.send(f"Successfully accepted **Idea #{idea_number}**.")
        except ValueError:
            await ctx.send(
                "Failed to accept that idea because it wasn't found.")
            return

        data[str(
            ctx.message.guild.id
        )]["projects"][project_id]["ideas"][message_id]["status"] = "accepted"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="acceptbugreport",
                      aliases=['acceptbr', 'approvebugreport', 'approverp'])
    @commands.has_permissions(manage_guild=True)
    async def accept_bugreport(self, ctx, project_id: str, id: int = None):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif id is None:
            await ctx.send("Missing bug report id or its message's id!")
            return

        bugreports = {}
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
        if "bugreports" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            bugreports = data[str(
                ctx.message.guild.id)]["projects"][project_id]["bugreports"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["bugreports"] = bugreports

        try:
            if id > len(bugreports):
                message_id = str(id)
                bugreport_number = list(bugreports.keys()).index(str(id)) + 1
            else:
                message_id = str(list(bugreports.keys())[id - 1])
                bugreport_number = id

            message = await ctx.fetch_message(message_id)
            embed = message.embeds[0]
            if embed.description.endswith(" **(ACCEPTED)**"):
                embed.description = embed.description[:-15]
            elif embed.description.endswith(" **(DENIED)**"):
                embed.description = embed.description[:-13]
            embed.description = embed.description + " **(ACCEPTED)**"
            await message.edit(embed=embed)

            await ctx.send(
                f"Successfully accepted **Bug Report #{bugreport_number}**.")
        except ValueError:
            await ctx.send(
                "Failed to accept that bug report because it wasn't found.")
            return

        data[str(ctx.message.guild.id)]["projects"][project_id]["bugreports"][
            message_id]["status"] = "accepted"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="denyidea",
                      aliases=['deny', 'declineidea', 'decline'])
    @commands.has_permissions(manage_guild=True)
    async def deny_idea(self, ctx, project_id: str, id: int = None):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif id is None:
            await ctx.send("Missing idea id or its message's id!")
            return

        ideas = {}
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
        if "ideas" in data[str(ctx.message.guild.id)]["projects"][project_id]:
            ideas = data[str(
                ctx.message.guild.id)]["projects"][project_id]["ideas"]

        data[str(
            ctx.message.guild.id)]["projects"][project_id]["ideas"] = ideas

        try:
            if id > len(ideas):
                message_id = str(id)
                idea_number = list(ideas.keys()).index(str(id)) + 1
            else:
                message_id = str(list(ideas.keys())[id - 1])
                idea_number = id

            message = await ctx.fetch_message(message_id)
            embed = message.embeds[0]
            if embed.description.endswith(" **(ACCEPTED)**"):
                embed.description = embed.description[:-15]
            elif embed.description.endswith(" **(DENIED)**"):
                embed.description = embed.description[:-13]
            embed.description = embed.description + " **(DENIED)**"
            await message.edit(embed=embed)

            await ctx.send(f"Successfully denied **Idea #{idea_number}**.")
        except ValueError:
            await ctx.send("Failed to deny that idea because it wasn't found.")
            return

        data[str(
            ctx.message.guild.id
        )]["projects"][project_id]["ideas"][message_id]["status"] = "denied"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="denybugreport",
                      aliases=['denybr', 'declinebugreport', 'declinebr'])
    @commands.has_permissions(manage_guild=True)
    async def deny_bugreport(self, ctx, project_id: str, id: int = None):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return
        elif id is None:
            await ctx.send("Missing bug report id or its message's id!")
            return

        bugreports = {}
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
        if "bugreports" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            bugreports = data[str(
                ctx.message.guild.id)]["projects"][project_id]["bugreports"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["bugreports"] = bugreports

        try:
            if id > len(bugreports):
                message_id = str(id)
                bugreport_number = list(bugreports.keys()).index(str(id)) + 1
            else:
                message_id = str(list(bugreports.keys())[id - 1])
                bugreport_number = id

            message = await ctx.fetch_message(message_id)
            embed = message.embeds[0]
            if embed.description.endswith(" **(ACCEPTED)**"):
                embed.description = embed.description[:-15]
            elif embed.description.endswith(" **(DENIED)**"):
                embed.description = embed.description[:-13]
            embed.description = embed.description + " **(DENIED)**"
            await message.edit(embed=embed)

            await ctx.send(
                f"Successfully denied **Bug Report #{bugreport_number}**.")
        except ValueError:
            await ctx.send(
                "Failed to deny that bug report because it wasn't found.")
            return

        data[str(ctx.message.guild.id)]["projects"][project_id]["bugreports"][
            message_id]["status"] = "denied"

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="clearideas")
    @commands.has_permissions(manage_guild=True)
    async def clear_ideas(self, ctx, project_id=""):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return

        ideas = {}
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
        if "ideas" in data[str(ctx.message.guild.id)]["projects"][project_id]:
            ideas = data[str(
                ctx.message.guild.id)]["projects"][project_id]["ideas"]

        data[str(
            ctx.message.guild.id)]["projects"][project_id]["ideas"] = ideas

        for message_id in list(ideas.keys()):
            message = await ctx.fetch_message(message_id)
            embed = message.embeds[0]
            if embed.description.endswith(" **(ACCEPTED)**"):
                embed.description = embed.description[:-15]
            elif embed.description.endswith(" **(DENIED)**"):
                embed.description = embed.description[:-13]
            embed.description = embed.description + " **(DELETED)**"
            await message.edit(embed=embed)

        if len(ideas) == 1:
            await ctx.send(f"Successfully cleared **{len(ideas)} Idea**.")
        else:
            await ctx.send(f"Successfully cleared **{len(ideas)} Ideas**.")

        data[str(ctx.message.guild.id)]["projects"][project_id]["ideas"] = {}

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.command(name="clearbugreports")
    @commands.has_permissions(manage_guild=True)
    async def clear_bugreports(self, ctx, project_id: str):
        if project_id.strip() == "":
            await ctx.send("Missing project ID!")
            return

        bugreports = {}
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
        if "bugreports" in data[str(
                ctx.message.guild.id)]["projects"][project_id]:
            bugreports = data[str(
                ctx.message.guild.id)]["projects"][project_id]["bugreports"]

        data[str(ctx.message.guild.id
                 )]["projects"][project_id]["bugreports"] = bugreports

        for message_id in list(bugreports.keys()):
            message = await ctx.fetch_message(message_id)
            embed = message.embeds[0]
            if embed.description.endswith(" **(ACCEPTED)**"):
                embed.description = embed.description[:-15]
            elif embed.description.endswith(" **(DENIED)**"):
                embed.description = embed.description[:-13]
            embed.description = embed.description + " **(DELETED)**"
            await message.edit(embed=embed)

        if len(bugreports) == 1:
            await ctx.send(
                f"Successfully cleared **{len(bugreports)} Bug Report**.")
        else:
            await ctx.send(
                f"Successfully cleared **{len(bugreports)} Bug Reports**.")

        data[str(
            ctx.message.guild.id)]["projects"][project_id]["bugreports"] = {}

        with open('databases/ideas.json', 'w') as file:
            json.dump(data, file, indent=4)

        # Delete user's message
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await self.bot.get_channel(payload.channel_id
                                             ).fetch_message(payload.message_id
                                                             )

        d = {}
        if str(message.guild.id) not in d:
            d[str(message.guild.id)] = {}
        if "projects" not in d[str(message.guild.id)]:
            d[str(message.guild.id)]["projects"] = {}
        for project_id in d[str(message.guild.id)]["projects"]:
            ideas = {}
            bugreports = {}
            data = {}
            with open('databases/ideas.json', 'r') as file:
                data = json.load(file)
            if "ideas" in data[str(message.guild.id)]["projects"][project_id]:
                ideas = data[str(
                    message.guild.id)]["projects"][project_id]["ideas"]
            if "bugreports" in data[str(
                    message.guild.id)]["projects"][project_id]:
                bugreports = data[str(
                    message.guild.id)]["projects"][project_id]["bugreports"]

            if (str(message.id) not in ideas
                    or "status" not in ideas[str(message.id)]
                    or ideas[str(message.id)]["status"] != "open") and (
                        str(message.id) not in bugreports
                        or "status" not in bugreports[str(message.id)]
                        or bugreports[str(message.id)]["status"] != "open"):
                return

            if str(payload.emoji) != "👍" and str(payload.emoji) != "👎":
                await message.remove_reaction(payload.emoji, payload.member)
                return

            if len(message.reactions) < 2:
                return

            thumbs_up_amount = message.reactions[0].count - 1
            thumbs_down_amount = message.reactions[1].count - 1
            total_amount = thumbs_up_amount + thumbs_down_amount

            if payload.member.id != self.bot.user.id:
                reaction = discord.utils.get(message.reactions,
                                             emoji=payload.emoji.name)

                for react in message.reactions:
                    if react != reaction and payload.member in ([
                            user async for user in react.users()
                    ]):
                        await message.remove_reaction(react.emoji,
                                                      payload.member)

                        if str(react.emoji) == "👍":
                            thumbs_up_amount -= 1
                        elif str(react.emoji) == "👎":
                            thumbs_down_amount -= 1
                        total_amount -= 1
            try:
                filled_thumbs_up = int(7 / (total_amount / thumbs_up_amount))
            except ZeroDivisionError:
                filled_thumbs_up = 0
            try:
                filled_thumbs_down = int(7 /
                                         (total_amount / thumbs_down_amount))
            except ZeroDivisionError:
                filled_thumbs_down = 0

            embed = message.embeds[0]
            update_embed = discord.Embed(title=embed.title,
                                         description=embed.description,
                                         colour=embed.colour)
            update_embed.set_thumbnail(
                url=
                f'https://cdn.discordapp.com/icons/{message.guild.id}/{message.guild.icon}.png'
            )
            update_embed.add_field(name=embed.fields[0].name,
                                   value=embed.fields[0].value,
                                   inline=embed.fields[0].inline)

            update_embed.add_field(
                name='\u200b',
                value=
                f"👍 {(':red_square:' * filled_thumbs_up) + (':white_large_square:' * (7 - filled_thumbs_up))} {thumbs_up_amount}"
            )
            update_embed.add_field(
                name='\u200b',
                value=
                f"👎 {(':red_square:' * filled_thumbs_down) + (':white_large_square:' * (7 - filled_thumbs_down))} {thumbs_down_amount}"
            )

            await message.edit(embed=update_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message = await self.bot.get_channel(payload.channel_id
                                             ).fetch_message(payload.message_id
                                                             )

        d = {}
        if str(message.guild.id) not in d:
            d[str(message.guild.id)] = {}
        if "projects" not in d[str(message.guild.id)]:
            d[str(message.guild.id)]["projects"] = {}
        for project_id in d[str(message.guild.id)]["projects"]:
            ideas = {}
            bugreports = {}
            data = {}
            with open('databases/ideas.json', 'r') as file:
                data = json.load(file)
            if "ideas" in data[str(message.guild.id)]["projects"][project_id]:
                ideas = data[str(
                    message.guild.id)]["projects"][project_id]["ideas"]
            if "bugreports" in data[str(
                    message.guild.id)]["projects"][project_id]:
                bugreports = data[str(
                    message.guild.id)]["projects"][project_id]["bugreports"]

            if (str(message.id) not in ideas
                    or "status" not in ideas[str(message.id)]
                    or ideas[str(message.id)]["status"] != "open") and (
                        str(message.id) not in bugreports
                        or "status" not in bugreports[str(message.id)]
                        or bugreports[str(message.id)]["status"] != "open"):
                return

            if len(message.reactions) < 2:
                return

            thumbs_up_amount = message.reactions[0].count - 1
            thumbs_down_amount = message.reactions[1].count - 1
            total_amount = thumbs_up_amount + thumbs_down_amount

            try:
                filled_thumbs_up = int(7 / (total_amount / thumbs_up_amount))
            except ZeroDivisionError:
                filled_thumbs_up = 0
            try:
                filled_thumbs_down = int(7 /
                                         (total_amount / thumbs_down_amount))
            except ZeroDivisionError:
                filled_thumbs_down = 0

            embed = message.embeds[0]
            update_embed = discord.Embed(title=embed.title,
                                         description=embed.description,
                                         colour=embed.colour)
            update_embed.set_thumbnail(
                url=
                f'https://cdn.discordapp.com/icons/{message.guild.id}/{message.guild.icon}.png'
            )
            update_embed.add_field(name=embed.fields[0].name,
                                   value=embed.fields[0].value,
                                   inline=embed.fields[0].inline)

            update_embed.add_field(
                name='\u200b',
                value=
                f"👍 {(':red_square:' * filled_thumbs_up) + (':white_large_square:' * (7 - filled_thumbs_up))} {thumbs_up_amount}"
            )
            update_embed.add_field(
                name='\u200b',
                value=
                f"👎 {(':red_square:' * filled_thumbs_down) + (':white_large_square:' * (7 - filled_thumbs_down))} {thumbs_down_amount}"
            )

            await message.edit(embed=update_embed)


async def setup(bot):
    await bot.add_cog(Project(bot))
