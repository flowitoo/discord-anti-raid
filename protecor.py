import discord
import time
from discord import Intents, Activity
import asyncio
from collections import defaultdict
import threading

intents=intents=Intents.all()

bot = discord.Client(intents=intents)

global invite_uses_before
invite_uses_before = defaultdict(dict)

global invite_uses_after
invite_uses_after = defaultdict(dict)

global counter
counter = {}

global countdown_task
countdown_task = {}

global spam
spam = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(name=f"protecting {len(bot.guilds)} server(s) with {len(bot.users)} user(s)", type=5))
    print("im ready")

    loop = asyncio.get_event_loop()
    loop.create_task(update_every_5s())


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
        countdown_task[invite.code] = asyncio.create_task(checkit())
        try:
            if countdown_task[invite.code] in asyncio.all_tasks():
                pass
                
            else:
                countdown_task[invite.code].start()
        except:
            countdown_task[invite.code].start()
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

async def checkit():
    time.sleep(10)
    for guild in bot.guilds:
        invites = await guild.invites()
        for invite in invites:
            counter[invite.code] = []
            counter[invite.code] = list()
            counter[invite.code].clear()

async def update_every_5s():
    while True:
        await asyncio.sleep(5)
        await update_invites()

bot.run("TOKEN")
