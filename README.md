# discord-anti-raid
[![Last Commit](https://img.shields.io/github/last-commit/flowitoo/discord-anti-raid?color=9b59b6&logo=Elixir&logoColor=9b59b6&style=for-the-badge)](https://github.com/flowitoo/discord-anti-raid)
[![Repo visits](https://badges.pufler.dev/visits/flowitoo/discord-anti-raid?style=for-the-badge&logo=elixir&logoColor=9b59b6&color=9b59b6&label=repo+visits)](https://github.com/flowitoo/discord-anti-raid)

This simple bot will protect your server from token raids, delete all messages (if tokens manage to spam something) and soft ban them (ban them and unban them).

## How it works?

The bot works by tracking the invite code and how many users will enter within 10 seconds, and if more than 5 users enter within 10 seconds using the same invite code the bot will soft ban them (ban them and unban them) and delete all their messages and thus prevent tokens to spam on your server.

## How does the bot know through which invite code who entered?
The bot compares all the invite codes and checks which invite code has more uses after someone has joined the server and in that way you can extract Invite uses, Invite code, Inviter, and everything else related to invite...

```python
...
global invite_uses_before
invite_uses_before = []
invite_uses_before = list()

global invite_uses_after
invite_uses_after = []
invite_uses_after = list()

async def update_invites():
    for guild in bot.guilds:
        invites = await guild.invites()
        invite_uses_before.clear()
        for invite in invites:
            invite_uses_before.append(invite)

@bot.event()
async def on_member_join(member):
    guild = bot.get_guild(member.guild.id)
    invite_uses_after.clear()
    invites = await guild.invites()

    for invite in invites:
        invite_uses_after.append(invite)

    for i, invite in enumerate(invite_uses_after):
        if int(invite_uses_before[i].uses) != int(invite.uses):
            print(f"User {member.name} was invited by {invite.inviter}, invite code is {invite.code}, invite code was used {invite.uses} times")
...
```

As you can see in **update_invites** we append invite codes to the **invite_uses_before**, and then we just wait for the user to join so the code below runs below **on_member_join** event execute. When the user joins, we append the invite codes to **invite_uses_after** and compare the invite uses of each invite code from **invite_uses_before** with the invite uses from **invite_uses_after**, and extract the invite code that has one use more.

## EXTRA
The bot supports multi-guild functionality, which means it can run on multiple servers, with individual options for each server.
