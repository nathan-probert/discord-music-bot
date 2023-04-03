from random import randint
import discord
from discord.ext import commands

# get token for bot
file1 = open("discord-music-bot\\lib\\secret.txt", 'r')
TOKEN = file1.readline()
file1.close() 

# set up bot
client = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())

#on start up
@client.event
async def on_ready():  # runs when the bot goes online
    print('Logged in as')
    print(client.user.name)
    print('------')

    await client.change_presence(status=discord.Status.do_not_disturb)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="top tier music"))

# help menu
@client.command()
async def help(ctx):
    await ctx.send("```yaml\n"
                   "!join\nConnects the bot to your voice channel\n\n"
                   "```")
    
# allow the bot to be invited to servers
@client.command()
async def invite(ctx):
    await ctx.send("Click this link to invite me to your server!\n"
                   "https://discord.com/api/oauth2/authorize?client_id=812037295040364584&permissions=8&scope=bot")
    
# change nickname of a user
@client.command()
async def changename(ctx, member: discord.Member, name):
    await member.edit(nick=name)
@changename.error
async def permission_error(ctx, error):
    text = "Sorry, I do not have permissions to do that!"
    await ctx.send(text)
    

# print permissions
@client.command()
async def permissions(ctx, bot : discord.Member=None):
    if bot.guild_permissions.administrator:
        await ctx.send("This user has administrator permissions")
    else:

        if bot.guild_permissions.manage_guild:
            s1 = "manage_guild=**TRUE**"
        else:
            s1 = "manage_guild=False"

        if bot.guild_permissions.embed_links:
            s2 = "embed_links=**TRUE**"
        else:
            s2 = "embed_links=False"

        if bot.guild_permissions.deafen_members:
            s3 = "deafen_members=**TRUE**"
        else:
            s3 = "deafen_members=False"

        if bot.guild_permissions.create_instant_invite:
            s4 = "create_instant_invite=**TRUE**"
        else:
            s4 = "create_instant_invite=False"

        if bot.guild_permissions.connect:
            s5 = "connect=**TRUE**"
        else:
            s5 = "connect=False"

        if bot.guild_permissions.change_nickname:
            s6 = "change_nickname=**TRUE**"
        else:
            s6 = "change_nickname=False"

        if bot.guild_permissions.ban_members:
            s7 = "ban_members=**TRUE**"
        else:
            s7 = "ban_members=False"

        if bot.guild_permissions.attach_files:
            s8 = "attach_files=**TRUE**"
        else:
            s8 = "attach_files=False"

        if bot.guild_permissions.add_reactions:
            s10 = "add_reactions=**TRUE**"
        else:
            s10 = "add_reactions=False"

        if bot.guild_permissions.read_messages:
            s11 = "read_messages=**TRUE**"
        else:
            s11 = "read_messages=False"

        if bot.guild_permissions.read_message_history:
            s12 = "read_message_history=**TRUE**"
        else:
            s12 = "read_message_history=False"

        if bot.guild_permissions.priority_speaker:
            s13 = "priority_speaker=**TRUE**"
        else:
            s13 = "priority_speaker=False"

        if bot.guild_permissions.mute_members:
            s14= "mute_members=**TRUE**"
        else:
            s14= "mute_members=False"

        if bot.guild_permissions.move_members:
            s15= "move_members=**TRUE**"
        else:
            s15= "move_members=False"

        if bot.guild_permissions.mention_everyone:
            s16= "mention_everyone=**TRUE**"
        else:
            s16= "mention_everyone=False"

        if bot.guild_permissions.manage_webhooks:
            s17= "manage_webhooks=**TRUE**"
        else:
            s17= "manage_webhooks=False"

        if bot.guild_permissions.manage_roles:
            s18= "manage_roles=**TRUE**"
        else:
            s18= "manage_roles=False"

        if bot.guild_permissions.manage_permissions:
            s19= "manage_permissions=**TRUE**"
        else:
            s19= "manage_permissions=False"

        if bot.guild_permissions.manage_nicknames:
            s20= "manage_nicknames=**TRUE**"
        else:
            s20= "manage_nicknames=False"

        if bot.guild_permissions.manage_messages:
            s21= "manage_messages=**TRUE**"
        else:
            s21= "manage_messages=False"

        if bot.guild_permissions.manage_emojis:
            s22= "manage_emojis=**TRUE**"
        else:
            s22= "manage_emojis=False"

        if bot.guild_permissions.manage_channels:
            s23= "manage_channels=**TRUE**"
        else:
            s23= "manage_channels=False"

        if bot.guild_permissions.kick_members:
            s24= "kick_members=**TRUE**"
        else:
            s24= "kick_members=False"

        if bot.guild_permissions.external_emojis:
            s25= "external_emojis=**TRUE**"
        else:
            s25= "external_emojis=False"

        if bot.guild_permissions.view_guild_insights:
            s26= "view_guild_insights=**TRUE**"
        else:
            s26= "view_guild_insights=False"

        if bot.guild_permissions.view_channel:
            s27= "view_channel=**TRUE**"
        else:
            s27= "view_channel=False"

        if bot.guild_permissions.view_audit_log:
            s28= "view_audit_log=**TRUE**"
        else:
            s28= "view_audit_log=False"

        if bot.guild_permissions.use_voice_activation:
            s29= "use_voice_activation=**TRUE**"
        else:
            s29= "use_voice_activation=False"

        if bot.guild_permissions.use_external_emojis:
            s31= "use_external_emojis=**TRUE**"
        else:
            s31= "use_external_emojis=False"

        if bot.guild_permissions.stream:
            s32= "stream=**TRUE**"
        else:
            s32= "stream=False"

        if bot.guild_permissions.speak:
            s33= "speak=**TRUE**"
        else:
            s33= "speak=False"

        if bot.guild_permissions.send_tts_messages:
            s34= "send_tts_messages=**TRUE**"
        else:
            s34= "send_tts_messages=False"

        if bot.guild_permissions.send_messages:
            s35= "send_messages=**TRUE**"
        else:
            s35= "send_messages=False"

        if bot.guild_permissions.request_to_speak:
            s36= "request_to_speak=**TRUE**"
        else:
            s36= "request_to_speak=False"
        string = s1 + "\n" + s2+ "\n" + s3+ "\n" + s4+ "\n" + s5+ "\n" + s6+ "\n" + s7+ "\n" + s8+  "\n" +s10+  "\n" +s11+  "\n" +s12+  "\n" +s13+  "\n" +s14+  "\n" +s15+  "\n" +s16+  "\n" +s17+  "\n" +s18+  "\n" +s19+  "\n" +s20+  "\n" +s21+  "\n" +s22+  "\n" +s23+  "\n" +s24+ "\n" + s25+ "\n" + s26+ "\n" + s27+  "\n" +s28+  "\n" +s29+ "\n" +s31+  "\n" +s32+  "\n" +s33+  "\n" +s33+  "\n" +s34+  "\n" +s35+ "\n" + s36
        await ctx.send(string)


@client.command()
async def randnum(ctx, min, max):
    min = min.replace(",", "")
    min = int(min)
    max = int(max)
    shuffler = randint(min, max)
    await ctx.send("From " + str(min) + " to " + str(max) + " I chose " + str(shuffler))


@client.command()
async def flip(ctx):
    shuffler = randint(0, 1)
    if shuffler == 0:
        await ctx.send("Heads")
    else:
        await ctx.send("Tails")


@client.command()
async def av(ctx, *,  avamember : discord.Member=None):
    print("ok")
    username = str(avamember)
    username = str(username[:-5])
    userAvatarUrl = avamember.avatar_url
    await ctx.send(str(username))
    await ctx.send(userAvatarUrl)

# runs the bot
client.run(TOKEN)