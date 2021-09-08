from discord.ext import commands
from discord import Intents
import asyncio
from collections import defaultdict

intents=intents=Intents.all()

bot = commands.Bot(command_prefix="+", intents=intents)
bot.remove_command("help")

global invite_uses_before
invite_uses_before = defaultdict(dict)

global invite_uses_after
invite_uses_after = defaultdict(dict)

global counter
counter = {}

@bot.event
async def on_ready(): 
    await restart()
    print("im ready")
    task = asyncio.create_task(await update_every_5s())
    task = asyncio.create_task(await restart_every_10_s())

async def restart():
    for guild in bot.guilds:
        invites = await guild.invites()
        for invite in invites:
            counter[invite.code] = []
            counter[invite.code] = list()
            counter[invite.code].clear()

async def update_invites():
    for guild in bot.guilds:
        invite_uses_before[guild.id] = []
        invite_uses_before[guild.id] = list()
        invites = await guild.invites()
        invite_uses_before[guild.id].clear()
        for invite in invites:
            invite_uses_before[guild.id].append(invite)

@bot.event
async def on_invite_create(invite):
    counter[invite.code] = []
    counter[invite.code] = list()

@bot.event
async def on_guild_join(guild):
    invite_uses_before[guild.id] = []
    invite_uses_before[guild.id] = list()
    invites = await guild.invites()
    for invite in invites:
        invite_uses_before[guild.id].append(invite)

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(member.guild.id)
    invite_uses_after[guild.id] = []
    invite_uses_after[guild.id] = list()
    invite_uses_after[guild.id].clear()
    invites = await guild.invites()

    for invite in invites:
        invite_uses_after[guild.id].append(invite)

    for i, invite in enumerate(invite_uses_after[guild.id]):
        counter[invite.code].append(member.id)
        if int(invite_uses_before[guild.id][i].uses) != int(invite.uses):
            if len(counter[invite.code]) >= 5:
                await invite.delete(reason="used for spam")
                for user in counter[invite.code]:
                    await guild.ban(bot.get_user(user), reason = "Flow protector is ON and is protecting you from token spams", delete_message_days = 7)
                    await guild.unban(bot.get_user(user))
        else:
            pass
    
    invite_uses_before[guild.id].clear()
    for invite in invite_uses_after[guild.id]:
        invite_uses_before[guild.id].append(invite)

async def restart_every_10_s():
    while True:
        await asyncio.sleep(10)
        await restart()

async def update_every_5s():
    while True:
        await asyncio.sleep(5)
        await update_invites()

bot.run("ENTER YOUR TOKEN HERE")
