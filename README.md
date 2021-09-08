# discord-anti-raid
[![Last Commit](https://img.shields.io/github/last-commit/flowitoo/token-checker?color=9b59b6&logo=Elixir&logoColor=9b59b6&style=for-the-badge)](https://github.com/flowitoo/token-checker)
[![Repo visits](https://badges.pufler.dev/visits/flowitoo/token-checker?style=for-the-badge&logo=elixir&logoColor=9b59b6&color=9b59b6&label=repo+visits)](https://github.com/flowitoo/token-checker)
This simple bot will protect your server from token raids, delete all messages (if tokens manage to spam something) and soft ban them (ban them and unban them).

## How it works?

The bot works by tracking the invite code and how many users will enter within 10 seconds, and if more than 5 users enter within 10 seconds the bot will soft ban them (ban pa unban) and delete all their messages and thus prevent tokens to spam on your server.

## How does the bot know through which invite code who entered?
The bot compares all the invite codes and checks which invite code has more uses after someone has joined the server and in that way you can extract Invite uses, Invite code, Inviter, and everything else related to invite...

```python
...
for i, invite in enumerate(invite_uses_after[guild.id]):
    counter[invite.code].append(member.id)
    if int(invite_uses_before[guild.id][i].uses) != int(invite.uses):
...
```
