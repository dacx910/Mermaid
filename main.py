from config.secrets import TOKEN
import discord
from discord.ext import tasks
from discord import app_commands
from discord.ui import Button, View
from base64 import b64decode, b64encode
import time
import sqlite3
from os import path
import logging
logger = logging.getLogger('discord')

def isBadMessage(message: str) -> str:
    if ("strictly first come first serve" in message.lower() and ("DM" in message.upper() or "text" in message.lower())):
        return "FreeMacbook"
    if ("macbook air 2020" in message.lower()):
        return "FreeMacbook"
    if (("ticket" in message.lower() or "seat" in message.lower() or "tixs" in message.lower()) and ("dm" in message.lower() or "text" in message.lower() or "message" in message.lower())):
        return "TicketSeller"
    return ""

def log(message: str):
    fmessage = f"<{time.asctime()}> {message}\n"
    if (len(message) > 100):
        # print(f"<{time.asctime()}> {message[:97]}...", file=stderr)
        logger.info(f"{message:97}...")
    else:
        # print(fmessage, end="", file=stderr)
        logger.info(message)
    with open(f"{path.abspath(path.dirname(__file__))}/logs/latest.log", "a") as f:
        try:
            f.write(fmessage)
        except Exception as e:
            f.write(f"<{time.asctime()}> Error: {e}, writing message as base64\n")
            f.write(f"<{time.asctime()}> {b64encode(message.encode()).decode('utf-8')}\n")
        f.close()

async def find_mod_channel(guild: discord.Guild) -> discord.TextChannel:
    channels = await guild.fetch_channels()
    for channel in channels:
        if (channel.type == discord.ChannelType.text and "mod" in channel.name):
            return channel
    return channels[0]

async def mod_log(guild: discord.Guild, message: str, invokeActions: bool = False, user: discord.Member = None):
    mod_channel: discord.TextChannel
    
    embedMessage = discord.Embed(title=f"Automated Action: <{time.asctime()}>", color=discord.Color(0x80c1c2))
    
    if (len(message) > 1020):
        embedMessage.add_field(name="Message:", value=f"{message[:1019]}```", inline=False)
        embedMessage.add_field(name="**TRUNCATED FOR LENGTH**", value='​', inline=False)
    else:
        embedMessage.add_field(name="Message:", value=message)

    con = sqlite3.connect('main.db')
    cur = con.cursor()
    result = cur.execute("SELECT value FROM settings WHERE guild_id=? AND key='mod_channel_id'", [guild.id]).fetchone()
    if result == None:
        mod_channel = await find_mod_channel(guild)
        cur.execute("INSERT INTO settings (guild, guild_id, key, value) VALUES(?,?,?,?)", (guild.name, guild.id, "mod_channel_id", mod_channel.id))
        con.commit()
    else:
        mod_channel = client.get_channel(result[0])

    if invokeActions:
            view = BanConfirmationView(user)
            await mod_channel.send(embed=embedMessage, view=view)
    else:
        await mod_channel.send(embed=embedMessage)
    con.close()
    return mod_channel

def not_have_table(cursor: sqlite3.Connection.cursor, tableName: str) -> bool:
    return cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tableName]).fetchone() == None

def db_check():
    db_con = sqlite3.connect("main.db")
    db_cur = db_con.cursor()

    if not_have_table(db_cur, "invites"):
        db_cur.execute("CREATE TABLE invites(guild, guild_id, code, num_uses)") # Create it
    if not_have_table(db_cur, "settings"):
        db_cur.execute("CREATE TABLE settings(guild, guild_id, key, value)")

    db_con.close()

async def general_user_audit(user: discord.User) -> discord.Embed:
    flags = user.public_flags
    flagList = ""
    if flags.staff: flagList += "Discord Employee, "
    if flags.partner: flagList += "Discord Partner, "
    if flags.hypesquad: flagList += "HypeSquad member, "
    if flags.bug_hunter: flagList += "Discord Bug Hunter, "
    if flags.hypesquad_balance: flagList += "HypeSquad Balance member, "
    if flags.hypesquad_bravery: flagList += "HypeSquad Bravery member, "
    if flags.hypesquad_brilliance: flagList += "HypeSquad Brilliance member, "
    if flags.early_supporter: flagList += "Early Supporter, "
    if flags.team_user: flagList += "Team User, "
    if flags.system: flagList += "Discord Official System User, "
    if flags.bug_hunter_level_2: flagList += "Bug Hunter Level 2, "
    if flags.verified_bot: flagList += "Verified Bot, "
    if flags.verified_bot_developer: flagList += "Verified Bot Developer, "
    if flags.discord_certified_moderator: flagList += "Discord Certified Moderator, "
    if flags.bot_http_interactions: flagList += "HTTP Bot, "
    if flags.spammer: flagList += "**Known spammer**, "
    if flags.active_developer: flagList += "Active Developer, "
    if flagList == "": flagList = "None"
    if flagList.endswith(", "): flagList = flagList[:-2]

    embed = discord.Embed(title=f"User Audit for {user.name}", color=discord.Color(0x80c1c2))
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="ID:", value=user.id, inline=False)
    embed.add_field(name="Creation Date & Time:", value=user.created_at, inline=False)
    embed.add_field(name="Is Bot:", value=user.bot, inline=False)
    embed.add_field(name="Public Flags:", value=flagList, inline=False)

    return embed

async def ban_command(messagable: discord.abc.Messageable, user: discord.Member):
    view = BanConfirmationView(user)
    embed = discord.Embed(title="Select an action for {user.mention}")
    await messagable.send(embed=embed, view=view)

class BanConfirmationView(View):
    def __init__(self, user_to_ban: discord.Member):
        super().__init__(timeout=None)
        self.user_to_ban = user_to_ban

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.danger)
    async def confirm_ban(self, interaction: discord.Interaction, button: Button):
        if (interaction.user.guild_permissions.ban_members):
            try:
                await self.user_to_ban.ban()
                await interaction.response.send_message(f"{self.user_to_ban.name} has been banned. Actioner: {interaction.user.mention}")
            except discord.Forbidden:
                await interaction.response.send_message("Bot does not have permission to ban this user")
            except Exception as e:
                await interaction.response.send_message(f"An error occurred: {e}")
            await interaction.message.edit(view=None)
        else:
            await interaction.response.send_message("You do not have permission to ban users", ephemeral=True)
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.red)
    async def kick(self, interaction: discord.Interaction, button: Button):
        if (interaction.user.guild_permissions.kick_members):
            await self.user_to_ban.kick()
            await interaction.response.send_message(f"{self.user_to_ban.name} has been kicked. Actioner: {interaction.user.mention}")
            await interaction.message.edit(view=None)
        else:
            await interaction.response.send_message("You do not have permission to kick users", ephemeral=True)
    @discord.ui.button(label="Run Audit on User", style=discord.ButtonStyle.blurple)
    async def audit(self, interaction: discord.Interaction, button: Button):
        embed = await general_user_audit(self.user_to_ban)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @discord.ui.button(label="False Positive", style=discord.ButtonStyle.green)
    async def restore(self, interaction: discord.Interaction, button: Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(f"Marked as a false positive by {interaction.user.mention}")

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        async for guild in self.fetch_guilds():
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        self.update_invites.start()

    async def on_ready(self):
        log(f"STARTED as {self.user}")
        await self.change_presence(activity=discord.CustomActivity("Developed by @dacx910"))
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        async for guild in self.fetch_guilds():
            guild_name = guild.name
            guild_id = guild.id
            for invite in await guild.invites():
                code = invite.id
                usage = invite.uses
                if (cur.execute("SELECT guild_id FROM invites WHERE code=?", [code]).fetchone() == None):
                    cur.execute("INSERT INTO invites (guild, guild_id, code, num_uses) VALUES(?, ?, ?, ?)", (guild_name, guild_id, code, usage))
                else:
                    cur.execute("UPDATE invites SET num_uses=? WHERE guild=? AND guild_id=? AND code=?", (usage, guild_name, guild_id, code))
        con.commit()
        con.close()
                
    async def on_member_join(self, member: discord.Member):
        guild_name = member.guild.name
        guild_id = member.guild.id
        
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        for invite in await member.guild.invites():
            code = invite.id
            uses = invite.uses
            if (cur.execute("SELECT guild_id FROM invites WHERE code=?", [code]).fetchone() == None):
                cur.execute("INSERT INTO invites (guild, guild_id, code, num_uses) VALUES(?,?,?,?)", (guild_name, guild_id, code, uses))
                if (uses >= 1):
                    await mod_log(member.guild, f"User <@{member.id}> joined using code {code} created by <@{invite.inviter.id}>", True, member)
            else:
                stored_uses = cur.execute("SELECT num_uses FROM invites WHERE guild=? AND guild_id=? AND code=?", (guild_name, guild_id, code)).fetchone()[0]
                if (stored_uses == uses):
                    continue
                else:
                    await mod_log(member.guild, f"User <@{member.id}> joined using code {code} created by <@{invite.inviter.id}>", True, member)
                    cur.execute("UPDATE invites SET num_uses=? WHERE guild=? AND guild_id=? AND code=?", (uses, guild_name, guild_id, code))
        con.commit()
        con.close()

    async def on_message(self, message: discord.Message):
        if (message.author != self.user):
            check = isBadMessage(message.content)
            if check != "":
                await message.delete()
                await mod_log(message.guild, f"Blocked message by <@{message.author.id}> because it violated rule: `{check}`\n```{message.content}```", True, message.author)
            else:
                log(f"MESSAGE: In {message.guild}({message.guild.id}) from {message.author}({message.author.id}): {message.content}")

    @tasks.loop(seconds=60)
    async def update_invites(self):
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        async for guild in self.fetch_guilds():
            guild_name = guild.name
            guild_id = guild.id
            for invite in await guild.invites():
                code = invite.id
                usage = invite.uses
                if (cur.execute("SELECT guild_id FROM invites WHERE code=?", [code]).fetchone() == None):
                    cur.execute("INSERT INTO invites (guild, guild_id, code, num_uses) VALUES(?, ?, ?, ?)", (guild_name, guild_id, code, usage))
                else:
                    cur.execute("UPDATE invites SET num_uses=? WHERE guild=? AND guild_id=? AND code=?", (usage, guild_name, guild_id, code))
        codes = cur.execute("SELECT code FROM invites").fetchall()
        for code in codes:
            try:
                await self.fetch_invite(f"https://discord.gg/{code[0]}")
            except:
                cur.execute("DELETE FROM invites WHERE code=?", code)
        con.commit()
        con.close()
    @update_invites.before_loop
    async def wait_update(self):
        await self.wait_until_ready()

def list_to_string(vList: list) -> str:
    buf = ""
    for item in vList:
        buf += (item + ", ")
    buf = buf[:-2]
    if buf == "":
        buf = "None"
    return buf

if __name__ == "__main__":
    db_check()

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = MyClient(intents=intents)

    @client.tree.command(description="Runs a report on all availble info for a particular user")
    @app_commands.describe(user="User you'd like to audit", public="Should the results be posted to the channel? Select 'No' if only you want to see the results")
    @app_commands.choices(public=[app_commands.Choice(name="Yes", value=1), app_commands.Choice(name="No", value=0)])
    @app_commands.default_permissions(view_audit_log=True)
    @app_commands.checks.has_permissions(view_audit_log=True)
    async def audit_user(interaction: discord.Interaction, user: discord.User, public: int=0):
        embed = await general_user_audit(user)
        if public:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @client.tree.command(description="Scans the server for suspicious users")
    @app_commands.describe(includebots="Add a section for bots in the report", public="Should the results be posted to the channel? Select 'No' if only you want to see the results")
    @app_commands.choices(includebots=[app_commands.Choice(name="Yes", value=1), app_commands.Choice(name="No", value=0)], public=[app_commands.Choice(name="Yes", value=1), app_commands.Choice(name="No", value=0)])
    @app_commands.default_permissions(view_audit_log=True)
    @app_commands.checks.has_permissions(view_audit_log=True)
    async def audit_server(interaction: discord.Interaction, includebots: int=0, public: int=0):
        spammers = []
        bots = []

        guild = interaction.guild
        async for member in guild.fetch_members():
            flags = member.public_flags
            if flags.spammer: spammers.append(f"<@{member.id}>")
            if includebots and (flags.verified_bot or flags.bot_http_interactions or member.bot): bots.append(f"<@{member.id}>")
        embed = discord.Embed(title=f"Server Audit for {interaction.guild.name}", color=discord.Color(0x80c1c2))
        try:
            guild_icon_url = interaction.guild.icon.url
        except:
            guild_icon_url = None
        embed.set_thumbnail(url=guild_icon_url)

        embed.add_field(name="Spammers:", value=list_to_string(spammers)[:1023], inline=False)
        if includebots:
            embed.add_field(name="Bots:", value=list_to_string(bots)[:1023], inline=False)
        if public:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @client.tree.command(description="Modify the channel you'd like this bot to send its notifications in")
    @app_commands.describe(channel="The channel you'd like the bot to send its notifications in")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def set_mod_log_channel(interaction: discord.Interaction, channel: discord.TextChannel):
        con = sqlite3.connect('main.db')
        cur = con.cursor()
        if cur.execute("SELECT * FROM settings WHERE guild_id=? AND key='mod_channel_id'", [interaction.guild.id]).fetchone() == None:
            cur.execute("INSERT INTO settings (guild, guild_id, key, value) VALUES(?,?,'mod_channel_id',?)", (interaction.guild.name, interaction.guild.id, channel.id))
        else:
            cur.execute("UPDATE settings SET value=? WHERE guild_id=? AND key='mod_channel_id'", (channel.id, interaction.guild.id))
        con.commit()
        con.close()
        await interaction.response.send_message(f"Log channel updated to <#{channel.id}>")
    

    client.run(TOKEN)