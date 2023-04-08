from random import randint
import discord
from discord.ext import commands
import os
import musicFunctions
from requests import get
import spotifyFunctions


# get token for bot
file1 = open("discord-music-bot\\secret.txt", 'r')
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
    await ctx.send(f"```yaml\n"
                   "!musichelp\nPrints the help menu for music\n\n"
                   "!plhelp\nPrints the help menu for playlists\n\n"
                   "!invite\nSends a link so you can invite King Chuck to your server\n\n"
                   "!av <target>\nDisplays full-size profile picture of target\n\n"
                   "!changename <target> newname\nChange targets nickname\n\n"
                   "!resetname <target>\nDelete targets nickname\n\n"
                   "!randnum <min> <max>\nPrints a random number in the given range\n\n"
                   "!flip\nFlips a coin and prints the result\n\n"
                   "```")
    

@client.command()
async def musichelp (ctx):
    await ctx.send(f"```yaml\n"
                "!play <songname>\nSearches youtube for the song, joins the voice channel, plays the song (adds to queue if something is already playing)\n\n"
                "!join\nJoins the voice channel\n\n"
                "!pause\nPause the song\n\n"
                "!resume\nResumes the song\n\n"
                "!skip\nSkips the current song\n\n"
                "!stop\nStops and disconnects the bot\n\n"
                "```")
    

@client.command()
async def plhelp (ctx):
    await ctx.send(f"```yaml\n"
                "!plplay <playlist name>\nShuffle plays the desired playlist\n\n"
                "!s <spotify url> <new playlist name>\nCreates a new playlist\n\n"
                "!pllist\nLists all current playlists\n\n"
                "!skip\nSkips the current song\n\n"
                "!pause\nPause the song\n\n"
                "!resume\nResumes the song\n\n"
                "!stop\nStops and disconnects the bot\n\n"
                "```")

    
# works
# allow the bot to be invited to servers
@client.command()
async def invite(ctx):
    await ctx.send("Click this link to invite me to your server!\n"
                   "https://discord.com/api/oauth2/authorize?client_id=812037295040364584&permissions=8&scope=bot")
    
# works
# change nickname of a user
@client.command()
async def changename(ctx, member: discord.Member, name):
    await member.edit(nick=name)
    
@client.command()
async def resetname(ctx, member: discord.Member):
    await member.edit(nick=member.name)

@changename.error
async def permission_error(ctx, error):
    await ctx.send("Sorry, I do not have permissions to do that!")
    

# works
@client.command()
async def randnum(ctx, min, max):
    min = min.replace(",", "")
    min = int(min)
    max = int(max)
    shuffler = randint(min, max)
    await ctx.send("From numbers " + str(min) + " to " + str(max) + " I chose " + str(shuffler))


# works
@client.command()
async def flip(ctx):
    shuffler = randint(0, 1)
    if shuffler == 0:
        await ctx.send("Heads")
    else:
        await ctx.send("Tails")


# works
@client.command()
async def av(ctx, user:discord.Member = None):
    if (user):
        userAvatarUrl = user.avatar.url
        await ctx.send(userAvatarUrl)
    else:
        await ctx.send("Be sure to ping the target user after the command!")


# works
@client.command()
async def tictactoeinfo(ctx):
    await ctx.send(":one: :two: :three:\n"
                   ":four: :five: :six:\n"
                   ":seven: :eight: :nine:")
    

# in progress
@client.command()
async def tictactoe(ctx, p2 : discord.Member):
    players = {ctx.message.author, p2}
    
    await ctx.send("Player 1: " + players[0]+
                   "\nPlayer 2: " + players[1])
    

# works
@client.command()
async def play(ctx, *, songname):
    # ctx.voice_client.source.volume = 0.5
    await ctx.message.delete()
    if (discord.utils.get(client.voice_clients, guild=ctx.guild) == None):
        await musicFunctions.join(ctx)
    await musicFunctions.queueSong(ctx, songname)
    if (ctx.voice_client.is_playing() == False):
        await ctx.send(musicFunctions.playSong(ctx))
    else:
        await ctx.send(f"Queued the following: '{songname}'", delete_after=5)


@client.command()
async def join(ctx):
    await musicFunctions.join(ctx)


@client.command()
async def plplay(ctx, *, playlistName):
    await ctx.message.delete()
    if (discord.utils.get(client.voice_clients, guild=ctx.guild) == None):
        await musicFunctions.join(ctx)
    if (ctx.voice_client.is_playing() == False):
        value = (musicFunctions.plPlay(ctx, playlistName))
        if (value == -1):
            await ctx.send("Could not find your playlist")
        else:
            await ctx.send(f"Now playing your playlist called {playlistName}")
    else:
        await ctx.send("Something is already playing currently.")

# work
@client.command()
async def pause(ctx):
    await ctx.message.delete()
    ctx.voice_client.pause()
    await ctx.send("-----Paused-----", delete_after=5)


# works
@client.command()
async def resume(ctx):
    await ctx.message.delete()
    ctx.voice_client.resume()
    await ctx.send("-----Resumed-----", delete_after=5)


@client.command()
async def skip(ctx):
    await ctx.message.delete()
    ctx.voice_client.stop()
    await ctx.send("-----Skipped-----", delete_after=5)


@client.command()
async def stop(ctx):
    await musicFunctions.disconnect(ctx)
    await ctx.send("-----Stopped-----", delete_after=5)


@client.command()
async def s(ctx, url, *, playlist_name):
    await spotifyFunctions.makePlaylist(ctx, playlist_name, url)


@client.command()
async def pllist(ctx):
    await ctx.send("Here is a list of all playlists:")
    playlistsToSend = ""
    playlists = os.listdir("playlists")
    for p in playlists:
        p=p.replace(".txt", "\n")
        playlistsToSend += p
    await ctx.send(playlistsToSend)

# runs the bot
client.run(TOKEN)