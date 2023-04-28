import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import yt_dlp
import os
import urllib.request
import re
from random import randint
import asyncio
import requests
import datetime
import base64
import spotipy


# When switching computers, make sure to change file locations (i think 4 times)
# C:/Users/proby/pythonProject/King Chuck (laptop)
# D:/PythonProjectKingChuck/pythonProject (pc)
location = 'C:/Users/natha/Documents/Code/Python/discord/Discord-Music-Bot'

bsTOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmEx' \
          'LTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWF' \
          'waSIsImp0aSI6ImQzN2QxZTdiLTM4MzUtNDUxZS1hZWU0LTVkZjYxOTgwZjYyMSIsImlhdCI6MTY' \
          'xNzIxNDcxMCwic3ViIjoiZGV2ZWxvcGVyL2NhNmFhYzRhLTE4NmUtZDc3Mi01OTQ4LWYzYjNlNTF' \
          'kNjJkMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3B' \
          'lci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTczLjMyLjIxOS4yMyJ' \
          'dLCJ0eXBlIjoiY2xpZW50In1dfQ.EE1fIZEahb3ossfcQuecpgqqtCshHzAaSixhBjQzhL_-l2fT' \
          'dYV0Mfhu1SyGHDNLmb1K5N-TgLftQ4GVo_vHZw'

TOKEN = 'ODEyMDM3Mjk1MDQwMzY0NTg0.YC66qg.ch8N93LdjtB38L-dnsYgKkvck0Q'

client = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())
players = {}
fakectx = None
correctguesses = 0
time = 0
CLIENT_ID = '27584e99a5e544a39d9438fb567dbe86'
CLIENT_SECRET = 'e52ded355c7a458692794ff88971c271'
GameOver = True


@client.event
async def on_server_join(ctx):
    print("Joined " + str(ctx.guild) + " for the first time.")
    path = os.path.join(location, str(ctx.guild))
    print(str(path))
    mode = 0o666
    os.makedirs(path, mode)


@client.event
async def on_ready():  # runs when the bot goes online
    print('Logged in as')
    print(client.user.name)
    print('------')

    global message
    message = 'placeholder'
    await client.change_presence(status=discord.Status.do_not_disturb)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="top tier music"))


@client.command()
async def help(ctx):
    await ctx.send("```yaml\n"
                   "!join\nConnects the bot to your voice channel\n\n"
                   "!leave\nDisconnects the bot from your voice channel\n\n"
                   "!play <song name>\nPlays the sound of the linked youtube video\n\n"
                   "!pause\nPauses the music\n\n"
                   "!resume\nResumes the music\n\n"
                   "!skip\nSkips the song\n\n"
                   "!plhelp\nOpens the playlist help menu\n\n"
                   "!tictactoe <@player>"
                   "```")


@client.command()
async def plhelp(ctx):
    await ctx.send("```yaml\n"
                   "!join\nConnects the bot to your voice channel\n\n"
                   "!leave\nDisconnects the bot from your voice channel\n\n"
                   "!pause\nPauses the music\n\n"
                   "!resume\nResumes the music\n\n"
                   "!skip\nSkips the song\n\n"
                   "!plcreate <playlist name(must be one word long)>\nCreates your playlist\n\n"
                   "!plplay <playlist name>\nShuffles and plays your playlist\n\n"
                   "!pladd <playlist name> <song title>\nAdds your song to the playlist\n\n"
                   "!pldelete <playlist name> <song title>\nDeletes your song from the playlist"
                   " (Must be typed exactly as you added it)\n\n"
                   "!pllist <playlist name>\nSends a .txt file containing your playlist"
                   "```")


@client.command()
async def tts(ctx, *, message):
    await join(ctx)
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        newvoice = discord.utils.get(client.voice_clients, channel=ctx.channel)
        playagain = False
        if voice.is_playing():
            print('paused')
            voice.pause()
            playagain = True
        tts = gTTS(text=message, lang="en")
        tts.save('speaker.mp3')
        newvoice.play(source='speaker.mp3')
        # slower but clearer
        os.remove("speaker.mp3")
        if playagain:
            voice.resume()
            print('resumed')
    except discord.ext.commands.errors.CommandInvokeError:
        print("They are not in a voice channel.")
    except AttributeError:
        print('attribute error')
        pass #handled elsewhere


@client.command()
async def clearqueue(ctx):
    try:
        server = ctx.guild
        file1 = open(location + "/" + str(server) + "/" + str(server) + ".txt", "w")
        file1.close()
    except Exception as e:
        print("There was a problem opening the file.")
        print(str(e))


@client.command()
async def queue(ctx):
    try:
        server = ctx.guild
        file1 = (location + "/" + str(server) + "/" + str(server) + ".txt")
        with open(file1, "r") as file:
            queue = file.read().splitlines()
            print(file)
        queue = str(queue)
        queue = queue.replace('[', '')
        queue = queue.replace(']', '')
        queue = queue.replace("'", '')
        await ctx.send(queue)  # print out the content
    except Exception as e:
        print("There was a problem reading the file.")
        print(str(e))
        error = ("400 Bad Request (error code: 50006): Cannot send an empty message")
        if (str(e) == error):
            await ctx.send("The queue is empty")


async def t2s(ctx, speaker):
    try:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        playagain = False
        if voice.is_playing():
            voice.pause()
            playagain = True
        tts = gTTS(text=speaker, lang="en")
        tts.save('speaker.mp3')
        playsound("speaker.mp3")
        # slower but clearer
        os.remove("speaker.mp3")
        if playagain:
            voice.resume()
    except discord.ext.commands.errors.CommandInvokeError:
        print("They are not in a voice channel.")


@client.command()
async def invite(ctx):
    await ctx.send("Click this link to invite me to your server!\n"
                   "https://discord.com/api/oauth2/authorize?client_id=812037295040364584&permissions=8&scope=bot")


@client.command()
async def join(ctx):
    try:
        global fakectx
        fakectx = ctx
        channel = ctx.author.voice.channel
        await channel.connect()
        server = ctx.guild
        print("Joined a voice chat in the server: " + str(server))
    except AttributeError:
        await ctx.send("You are not in a voice channel.")
    except discord.errors.ClientException:
        pass
    await ctx.guild.change_voice_state(channel = channel, self_mute=False, self_deaf=True)

    try:
        server = ctx.guild
        file1 = open(location + "/" + str(server) + "/" + str(server) + ".txt", "a")  # create a server called servername.txt
        file1.close()
    except Exception as e:
        print("There was a problem creating the file.")
        print(str(e))


@client.event
async def on_voice_state_update(member, before, after):
    try:
        if before.channel and not after.channel:
            channel = client.get_channel(before.channel.id)
            curMembers = []
            for member in channel.members:
                curMembers.append(member)
            try:
                if curMembers[1] != None:
                    print("There is still at least one other person/bot in the channel")
            except IndexError:
                await leave(fakectx)
    except Exception:
        pass #gets error but works idk


@client.command()
async def leave(ctx):  # leaves the program
    server = ctx.guild
    file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", "w")  # deletes the info off of the file
    file1.close()
    try:
        await stop(ctx, 0)
        await ctx.voice_client.disconnect()
    except Exception:
        pass


async def songplayer(ctx):  # will play the first file
    print("songplayer playin")
    server = ctx.guild
    file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", 'r')  # reads the entire file into content[]
    content = file1.readlines()
    file1.close()
    print("content:" + str(content))  # print out the content

    deletecheck = content[0]
    songtitle = content[0].replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + songtitle)  # searchs for the yt vid
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # dont remember tbh
    songurl = ("https://www.youtube.com/watch?v=" + video_ids[0])  # get the whole url saved as songurl
    print(songurl)  # print the full link for the first result

    song_there = os.path.isfile(location + '/' + str(server) + '/' + str(server) + ".mp3")
    try:
        if song_there:
            os.remove(location + '/' + str(server) + '/' + str(server) + ".mp3")
        try:
            await join(ctx)
        except discord.ext.commands.errors.ClientException:
            print("Bot is already in channel")
        except AttributeError:
            await ctx.send('Please make sure you are in a voice channel before running this command.')
        finally:
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessorts': [{
                    'key': 'FFmpegExtractAudio',
                    'prefessedcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    songurl, download=True)

            for file in os.listdir(location):
                if file.endswith(".webm"):
                    os.rename(file, location + "/" + str(server) + '/' + str(server) + ".mp3")
                if file.endswith(".m4a"):
                    os.rename(file, location + '/' + str(server) + '/' + str(server) + ".mp3")

            seconds = (meta['duration'])
            minutes, seconds = divmod(seconds, 60)
            if seconds > 9:
                messagedelete = await ctx.send("Now playing: " + (meta['title']) +
                                               "\nDuration: " + str(minutes) +
                                               ":" + str(seconds))
            else:
                messagedelete = await ctx.send("Now playing: " + (meta['title']) +
                                               "\nDuration: " + str(minutes) +
                                               ":0" + str(seconds))

            try:
                voice.play(discord.FFmpegPCMAudio(source=location + "/" + str(server) + '/' + str(server) + ".mp3"),
                           after=lambda e: queuetest(ctx))  # first song is now playing
            except discord.errors.ClientException:
                await ctx.send("Please stop the playlist to play a song.")
            file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", 'r')  # song stuff without first line
            content = file1.readlines()[1:]
            file1.close()

            file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", 'r')
            b_string = file1.readline()  # b string should be the first line

            if deletecheck == b_string:
                print("Songs match so it will be deleted from the file.")
                with open(location + '/' + str(server) + '/' + str(server) + ".txt", "w") as outfile:
                    outfile.write("".join(content))
                file1.close()
            else:
                print("The song name did not match the first line, so it won't delete the first line.")

    except PermissionError:  # this means that the first song is still playing
        print("First song is still playing.")
        await ctx.send("Your song has been added to the queue.")
        pass


@client.command()
async def play(ctx, *, songtitle):
    server = ctx.guild
    voice = discord.utils.get(client.voice_clients, guild=server)
    global keepplaying
    keepplaying = True
    file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", "a")
    file1.write(songtitle + "\n")
    file1.close()
    try:
        if voice.is_paused():
            await stop(ctx, 0)
    except AttributeError:
        pass
    await songplayer(ctx)


@client.command()
async def whatgame(ctx, first):
    await ctx.send("no")


def queuetest(ctx):
    print("songplayer playin")
    server = ctx.guild
    file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", 'r')  # reads the entire file into content[]
    content = file1.readlines()
    file1.close()
    print("content:" + str(content))  # print out the content
    try:
        deletecheck = content[0]
        songtitle = content[0].replace(" ", "+")
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + songtitle)  # searchs for the yt vid
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # dont remember tbh
        songurl = ("https://www.youtube.com/watch?v=" + video_ids[0])  # get the whole url saved as songurl
        print(songurl)  # print the full link for the first result

        song_there = os.path.isfile(location + '/' + str(server) + '/' + str(server) + ".mp3")
        try:
            if song_there:
                os.remove(location + '/' + str(server) + '/' + str(server) + ".mp3")
        finally:
            pass

        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessorts': [{
                'key': 'FFmpegExtractAudio',
                'prefessedcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                songurl, download=True)

        for file in os.listdir(location):
            if file.endswith(".webm"):
                os.rename(file, location + '/' + str(server) + '/' + str(server) + ".mp3")
            if file.endswith(".m4a"):
                os.rename(file, location + '/' + str(server) + '/' + str(server) + ".mp3")

        seconds = (meta['duration'])
        minutes, seconds = divmod(seconds, 60)
        try:
            voice.play(discord.FFmpegPCMAudio(source=location + '/' + str(server) + '/' + str(server) + ".mp3"),
                       after=lambda e: queuetest(ctx))  # first song is now playing
        except IndexError:
            pass
        file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", 'r')  # song stuff without first line
        content = file1.readlines()[1:]
        file1.close()

        file1 = open(location + '/' + str(server) + '/' + str(server) + ".txt", 'r')
        b_string = file1.readline()  # b string should be the first line

        if deletecheck == b_string:
            print("Songs match so it will be deleted from the file.")
            with open(location + '/' + str(server) + '/' + str(server) + ".txt", "w") as outfile:
                outfile.write("".join(content))
            file1.close()
        else:
            print("The song name did not match the first line, so it won't delete the first line.")
    except IndexError:
        print("That was the last song in the playlist.")


@client.command()
async def pause(ctx):
    await ctx.message.delete()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.pause()
            global paused
            paused = await ctx.send("--------\n"
                                    "Paused")
        else:
            await ctx.send("--------------------------------\n"
                           "No audio is currently playing", delete_after=5)
    except AttributeError:
        await ctx.send("Nothing is playing")


@client.command()
async def resume(ctx):
    await ctx.message.delete()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    print('resumed')
    try:
        if voice.is_paused():
            await paused.delete()
            await ctx.send("----------\n"
                           "Resumed", delete_after=5)
            voice.resume()
        else:
            await ctx.send("---------------------------\n"
                           "The audio is not paused", delete_after=5)
    except AttributeError:
        await ctx.send("Nothing is playing")


@client.command(pass_context=True)
async def skip(ctx, quiet=1):
    if quiet == 1:
        await ctx.message.delete()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    if quiet == 1:
        await ctx.send("The song has been skipped.", delete_after=5)
        

@client.command()
async def plcreate(ctx, playlist):

    file1 = 'a'
    try:
        file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) +"_playlist.txt")
        await ctx.send("This playlist name has already been taken. Please choose a new name.")
    except IOError:  # ran if file is not found
        path = os.path.join(location, str(playlist) + '_playlist')
        print(str(path))
        mode = 0o666
        os.makedirs(path, mode)
        await ctx.send('Your playlist called ' + str(playlist) + " has been created.")
        await ctx.send('To add songs to this playlist, use !pladd <playlist name> <song title>. '
                       'You can also use the !help playlist command for more help!')
        file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) +"_playlist.txt", "a")
    finally:
        file1.close()


@client.command()
async def pladd(ctx, playlist, *, songtitle):
    try:
        print("Adding to playlist: " + str(playlist) + "_playlist.txt")
        file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", "a")  # writes the file in at the bottom
        file1.write(songtitle + "\n")
        file1.close()
        await ctx.send("Your song has been added.")
    except IOError:
        print("IOError")
        await ctx.send("We could not find the playlist: " +str(playlist))
        pass


@client.command()
async def pldelete(ctx, playlist, *, songtitle):
    delete = False

    with open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", "r") as f:
        lines = f.readlines()

    with open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", "w") as f:
        for line in lines:
            line = line.lower()
            if line.strip("\n") != songtitle:
                f.write(line)
            else:
                delete = True

    if delete:
        await ctx.send("Your song has been deleted.")
    else:
        await ctx.send("We could not find that song. "
                       "Please use !pllist <playlist name> to see your playlist, "
                       "as any spelling mistakes you made when entering the song name "
                       "are not corrected and must be entered here as well.")


@client.command()
async def pllist(ctx, playlist):
    await ctx.send("This file contains your playlist songs. Edits here will not be carried over to our copy.")
    await ctx.send(file=discord.File(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt"))

@client.command()
async def deletepls(ctx, id):
    if (ctx.me.has_permissions(manage_messages=True)) : #does not work fix
        await ctx.message.delete()
        try:
            await ctx.channel.delete_messages([discord.Object(id=id)])
        except Exception as e:
            await ctx.send("No perms lmao")

    else:
        await ctx.send("give me perms")


@client.command()
async def changename(ctx, member: discord.Member, name):
    await member.edit(nick=name)


@changename.error
async def permission_error(ctx, error):
    text = "Sorry, I do not have permissions to do that!"
    await ctx.send(text)


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

        s9 = ''

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

        if bot.guild_permissions.use_slash_commands:
            s30= "use_slash_commands=**TRUE**"
        else:
            s30= "use_slash_commands=False"

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
        string = s1 + "\n" + s2+ "\n" + s3+ "\n" + s4+ "\n" + s5+ "\n" + s6+ "\n" + s7+ "\n" + s8+  "\n" +s10+  "\n" +s11+  "\n" +s12+  "\n" +s13+  "\n" +s14+  "\n" +s15+  "\n" +s16+  "\n" +s17+  "\n" +s18+  "\n" +s19+  "\n" +s20+  "\n" +s21+  "\n" +s22+  "\n" +s23+  "\n" +s24+ "\n" + s25+ "\n" + s26+ "\n" + s27+  "\n" +s28+  "\n" +s29+  "\n" +s30+  "\n" +s31+  "\n" +s32+  "\n" +s33+  "\n" +s33+  "\n" +s34+  "\n" +s35+ "\n" + s36
        await ctx.send(string)


@client.command()
async def plplay(ctx, playlist):
    global keepplaying
    keepplaying = True
    print("Playlist name: " + playlist)
    await ctx.send("Searching for your playlist called " + str(playlist) + "...", delete_after=2)
    file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", 'r')  # reads the entire file into content[]
    content = file1.readlines()
    file1.close()

    count = len(open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt").readlines())
    print("There are " + str(count) + " songs in this playlist.")
    shuffler = randint(0, count - 1)
    print(shuffler)

    songtitle = content[shuffler].replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + songtitle)  # searchs for the yt vid
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # dont remember tbh
    songurl = ("https://www.youtube.com/watch?v=" + video_ids[0])  # get the whole url saved as songurl
    print(songurl)  # print the full link for the first result

    song_there = os.path.isfile(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
    try:
        if song_there:
            os.remove(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
        try:
            await join(ctx)
        except discord.ext.commands.errors.ClientException:
            print("Bot is already in channel")
        except AttributeError:
            await ctx.send('Please make sure you are in a voice channel before running this command.')
        finally:
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessorts': [{
                    'key': 'FFmpegExtractAudio',
                    'prefessedcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    songurl, download=True)

            for file in os.listdir(location):
                if file.endswith(".webm"):
                    os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                    print("renamed")
                if file.endswith(".m4a"):
                    os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                    print("renamed")


            seconds = (meta['duration'])
            minutes, seconds = divmod(seconds, 60)
            rerun = 0
            try:
                voice.play(discord.FFmpegPCMAudio(source=location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3"), after=lambda
                    e: plqueuetest(ctx, playlist, shuffler, rerun, msgID, repeatkiller=[]))
                await ctx.send("Your playlist called " + str(playlist) + " is now playing.")
                if seconds > 9:
                    global message
                    msgID = await ctx.send("Now playing: " + (meta['title']) +
                                           "\nDuration: " + str(minutes) +
                                           ":" + str(seconds))
                else:
                    msgID = await ctx.send("Now playing: " + (meta['title']) +
                                           "\nDuration: " + str(minutes) +
                                           ":0" + str(seconds))
            except Exception:
                await ctx.send("Something is still playing. Please use !skip to skip it before playing a playlist.")
    except PermissionError:  # this means that the first song is still playing
        print("Can't play playlist because the first song is still playing.")
        await ctx.send("Please stop the first song with !skip before playing a playlist.")
    except IndexError:
        print("That was the last song in the playlist.")
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send("Please stop the first song with !skip before playing a playlist.")


@client.command()
async def name(ctx):
    playlistguess = 'playlistguess'
    file1 = open(location + '/' + str(playlistguess) + '_playlist/' + str(playlistguess) + "_plguess.txt", 'r')
    songtitle = file1.readline()
    await ctx.send("The song was: "
                   +songtitle+"\n---------------------------------------------"
                              "-----------------------------------------------------------------------")
    await skip(ctx, 0)


@client.command()
async def g(ctx, *, guess):
    await ctx.message.delete()
    latetime = datetime.datetime.now()
    guess = guess.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + guess)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    guessurl = ("https://www.youtube.com/watch?v=" + video_ids[0])

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessorts': [{
            'key': 'FFmpegExtractAudio',
            'prefessedcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            guessurl, download=False)

    finalguess = (meta['title'])

    playlistguess = 'playlistguess'
    file1 = open(location + '/' + str(playlistguess) + '_playlist/' + str(playlistguess) + "_plguess.txt", 'r')
    songtitle = file1.readline()
    file1.close()
    print('guess: '+finalguess)
    print('song: '+songtitle)
    print(str(time))
    print(str(latetime))
    timer = latetime - time
    goodtimer = str(timer)
    goodtimer = goodtimer[3:-4]
    if finalguess == songtitle:
        await ctx.send("You guessed it in " + str(goodtimer) +" seconds! The anwser was " + finalguess)
        global correctguesses
        correctguesses = correctguesses + 1
        if correctguesses == 1:
            await ctx.send("You have guessed the song correctly "
                           ""+str(correctguesses) + " time!\n----------------------------------------------------")
        else:
            await ctx.send("You have guessed the song correctly "
                           ""+str(correctguesses) + " times!\n----------------------------------------------------")
        await skip(ctx, 0)
    else:
        await ctx.send("Wrong")


def plqueueguess(ctx, playlist, shuffler, rerun, repeatkiller=[]):
    print("The queue test is running")
    if keepplaying:
        print("songplayer playin")
        file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", 'r')  # reads the entire file into content[]
        content = file1.readlines()
        file1.close()

        count = len(open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt").readlines())
        if rerun == 0:
            repeatkiller = [count + 1, count + 2]
        else:
            pass
        repeatkiller.append(shuffler)
        print(str(repeatkiller))

        shuffling = True
        bigcount = 0
        while shuffling:
            if bigcount > 500:
                wefailed = True
                break
            bigcount = bigcount + 1
            shuffler = randint(0, count - 1)
            if shuffler not in repeatkiller:
                wefailed = False
                shuffling = False

        i = 0
        if wefailed:
            while i < count:
                shuffler = i
                i = i + 1
                if shuffler not in repeatkiller:
                    print("We finally have a match!")
                    wefailed = False

        if wefailed:
            coro = ctx.send("That was the last song in your playlist.")
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            fut.result()
        else:
            print(str(shuffler))

            try:
                songtitle = content[shuffler].replace(" ", "+")
                html = urllib.request.urlopen(
                    "https://www.youtube.com/results?search_query=" + songtitle)  # searchs for the yt vid
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # dont remember tbh
                songurl = ("https://www.youtube.com/watch?v=" + video_ids[0])  # get the whole url saved as songurl
                print(songurl)  # print the full link for the first result

                song_there = os.path.isfile(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
                try:
                    if song_there:
                        os.remove(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
                finally:
                    pass

                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessorts': [{
                        'key': 'FFmpegExtractAudio',
                        'prefessedcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(
                        songurl, download=True)

                playlistguess = 'playlistguess'
                file1 = open(location + '/' + str(playlistguess) + '_playlist/' + str(playlistguess) + "_plguess.txt", 'w')
                file1.write(meta['title'])
                file1.close()

                totalduration = (meta['duration'])
                seconds = (meta['duration'])
                minutes, seconds = divmod(seconds, 60)
                for file in os.listdir(location):
                    if file.endswith(".webm"):
                        os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                        print("renamed")
                    if file.endswith(".m4a"):
                        os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                        print("renamed")

                rerun = 1
                try:
                    voice.play(discord.FFmpegPCMAudio(source=location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3"),
                               after=lambda e: plqueueguess(ctx, playlist, shuffler, rerun, repeatkiller))
                    global time
                    time = datetime.datetime.now()
                except IndexError:
                    print("Index Error")
                    pass

            except IndexError:
                print("That was the last song in the playlist.")


@client.command()
async def plguess(ctx, playlist):
    global keepplaying
    keepplaying = True
    print("Playlist name: " + playlist)
    await ctx.send("Searching for your playlist called " + str(playlist) + "...", delete_after=2)
    file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", 'r')  # reads the entire file into content[]
    content = file1.readlines()
    file1.close()

    playlistguess = 'playlistguess'
    try:
        path = os.path.join(location, "playlistguess_playlist")
        print(str(path))
        mode = 0o666
        os.makedirs(path, mode)
    except Exception as e:
        pass

    file1 = open(location + '/' + str(playlistguess) + '_playlist/' + str(playlistguess) + "_plguess.txt", 'a')
    file1.close()

    count = len(open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt").readlines())
    print("There are " + str(count) + " songs in this playlist.")
    shuffler = randint(0, count - 1)
    print(shuffler)

    songtitle = content[shuffler].replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + songtitle)  # searchs for the yt vid
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # dont remember tbh
    songurl = ("https://www.youtube.com/watch?v=" + video_ids[0])  # get the whole url saved as songurl
    print(songurl)  # print the full link for the first result

    song_there = os.path.isfile(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
    try:
        if song_there:
            os.remove(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
        try:
            await join(ctx)
        except discord.ext.commands.errors.ClientException:
            print("Bot is already in channel")
        except AttributeError:
            await ctx.send('Please make sure you are in a voice channel before running this command.')
        finally:
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessorts': [{
                    'key': 'FFmpegExtractAudio',
                    'prefessedcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    songurl, download=True)

            file1 = open(location + '/' + str(playlistguess) + '_playlist/' + str(playlistguess) + "_plguess.txt", 'w')
            file1.write(meta['title'])
            file1.close()

            for file in os.listdir(location):
                if file.endswith(".webm"):
                    os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                    print("renamed")
                if file.endswith(".m4a"):
                    os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                    print("renamed")


            seconds = (meta['duration'])
            minutes, seconds = divmod(seconds, 60)
            rerun = 0
            try:
                await ctx.send("Good luck! We are beginning now. Please note that the time it takes for us to verify your answer will **not** be counted"
                               "in the time that we send you after a correct guess. If you don't know the answer, using !name will tell you the name"
                               " of the song and will skip forwards to the next one!")
                voice.play(discord.FFmpegPCMAudio(source=location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3"), after=lambda
                    e: plqueueguess(ctx, playlist, shuffler, rerun, repeatkiller=[]))
                global time
                time = datetime.datetime.now()
            except Exception:
                await ctx.send("Something is still playing. Please use !skip to skip it before playing a playlist.")
    except PermissionError:  # this means that the first song is still playing
        print("Can't play playlist because the first song is still playing.")
        await ctx.send("Please stop the first song with !skip before playing a playlist.")
    except IndexError:
        print("That was the last song in the playlist.")
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send("Please stop the first song with !skip before playing a playlist.")


def plqueuetest(ctx, playlist, shuffler, rerun, msgID, repeatkiller=[]):
    print("The queue test is running")
    if keepplaying:
        file1 = open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt", 'r')  # reads the entire file into content[]
        content = file1.readlines()
        file1.close()

        count = len(open(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.txt").readlines())
        if rerun == 0:
            repeatkiller = [count + 1, count + 2]
        else:
            pass
        repeatkiller.append(shuffler)
        print(str(repeatkiller))

        shuffling = True
        bigcount = 0
        while shuffling:
            if bigcount > 500:
                wefailed = True
                break
            bigcount = bigcount + 1
            shuffler = randint(0, count - 1)
            if shuffler not in repeatkiller:
                wefailed = False
                shuffling = False

        i = 0
        if wefailed:
            while i < count:
                shuffler = i
                i = i + 1
                if shuffler not in repeatkiller:
                    print("We finally have a match!")
                    wefailed = False

        if wefailed:
            coro = ctx.send("That was the last song in your playlist.")
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            fut.result()
        else:
            print(str(shuffler))

            try:
                songtitle = content[shuffler].replace(" ", "+")
                html = urllib.request.urlopen(
                    "https://www.youtube.com/results?search_query=" + songtitle)  # searchs for the yt vid
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # dont remember tbh
                songurl = ("https://www.youtube.com/watch?v=" + video_ids[0])  # get the whole url saved as songurl
                print(songurl)  # print the full link for the first result

                song_there = os.path.isfile(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
                try:
                    if song_there:
                        os.remove(location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3")
                finally:
                    pass

                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessorts': [{
                        'key': 'FFmpegExtractAudio',
                        'prefessedcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(
                        songurl, download=True)

                totalduration = (meta['duration'])
                seconds = (meta['duration'])
                minutes, seconds = divmod(seconds, 60)
                for file in os.listdir(location):
                    if file.endswith(".webm"):
                        os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                        print("renamed")
                    if file.endswith(".m4a"):
                        os.rename(file, location + "/" + str(playlist) + "_playlist/" + str(playlist) + "_playlist.mp3")
                        print("renamed")

                rerun = 1
                try:
                    if seconds > 9:
                        msgtosend = "Now playing: " + (meta['title']) + "\nDuration: " + str(minutes) + ":" + str(
                            seconds)
                        coromsg = editor(msgtosend, msgID)
                        fut = asyncio.run_coroutine_threadsafe(coromsg, client.loop)
                    else:
                        msgtosend = ("Now playing: " + (meta['title']) +
                                     "\nDuration: " + str(minutes) +
                                     ":0" + str(seconds))
                        coromsg = editor(msgtosend, msgID)
                        fut = asyncio.run_coroutine_threadsafe(coromsg, client.loop)

                    fut.result()

                    voice.play(discord.FFmpegPCMAudio(source=location + '/' + str(playlist) + '_playlist/' + str(playlist) + "_playlist.mp3"),
                               after=lambda e: plqueuetest(ctx, playlist, shuffler, rerun, msgID, repeatkiller))
                    print(str(time))
                except IndexError:
                    print("Index Error")
                    pass

            except IndexError:
                print("That was the last song in the playlist.")


async def editor(message, msgID):
    print("Editing...")
    await msgID.edit(content=message)


async def songdescription(ctx, minutes, seconds, title):
    if seconds > 9:
        await ctx.send("Now playing: " + (title) +
                       "\nDuration: " + str(minutes) +
                       ":" + str(seconds))
    else:
        await ctx.send("Now playing: " + (title) +
                       "\nDuration: " + str(minutes) +
                       ":0" + str(seconds))


@client.command()
async def dumjoke(ctx):
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
    querystring = {"format": "text", "blacklistFlags": "nsfw,racist", "idRange": "0-150", "type": "single,twopart"}
    headers = {
        'x-rapidapi-key': "529d6e620emsh91324f2995b081ep177f79jsn131d745cd6c4",
        'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    json_response = response.json()
    parts = json_response["type"]
    if parts == 'twopart':
        first = json_response["setup"]
        print(first)
        await ctx.send(first)
        await asyncio.sleep(2)
        second = json_response["delivery"]
        print(second)
        await ctx.send(second)

    else:
        joketing = json_response["joke"]
        print(joketing)
        await ctx.send(joketing)


@client.command()
async def dm(ctx):
    await ctx.author.send("This sends a dm to the user.")


@client.command()
async def randnum(ctx, min, max):
    min = min.replace(",", "")
    min = int(min)
    max = int(max)
    shuffler = randint(min, max)
    await ctx.send("From " + str(min) + " to " + str(max) + " I chose " + str(shuffler))


@client.command()
async def wiki(ctx, *, search):
    try:
        response = wikipedia.summary(search, sentences=2)
    except:
        print("error")
        response = 'error'
    await ctx.send(response)
    print(response)
    await t2s(ctx, response)


@client.command()
async def stop(ctx, quiet = 1):
    global keepplaying
    keepplaying = False
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    if quiet == 1:
        await ctx.send('Stopped playing.')


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


@client.command()
async def update(ctx):
    server = ctx.guild
    file1 = open(str(server) + "_update.txt", 'a')
    file1.close()
    file1 = open(str(server) + "_update.txt", 'r')  # reads the entire file into content[]
    content = file1.readline()
    file1.close()
    if content != '0':
        await ctx.send("The bot has been updated.")
        print("The bot has been updated")
        file1 = open(str(server) + "_update.txt", 'w')
        file1.write("0")
        file1.close()
    else:
        await ctx.send("The bot has already been updated.")


@client.command()
async def s(ctx, playlist_name, *, message):
    username = "supernate8"
    access_token = get_token()
    spotify = spotipy.Spotify(auth=access_token)
    write_playlist(username, message, spotify, playlist_name)
    reference_file = "{}_playlist.txt".format(playlist_name)
    try:
        if not os.path.exists(playlist_name):
            os.makedirs(playlist_name + "_playlist")
    except NotADirectoryError:
        await ctx.send("The of your playlist is invalid. Please don't use special characters.")
    os.rename(reference_file, playlist_name + "_playlist/" + reference_file)


def get_token():
    token_url = "https://accounts.spotify.com/api/token"
    method = "POST"
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    token_data = {
        "grant_type": "client_credentials"
    }

    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r = requests.post(token_url, data=token_data, headers= token_headers)
    response_data = r.json()
    access_token = response_data['access_token']
    return access_token


def write_playlist(username: str, playlist_id: str, spotify, playlist):
    results = spotify.user_playlist(username, playlist_id, fields='tracks,next,name')
    playlist_name = results['name']
    text_file = u'{0}.txt'.format(playlist + "_playlist", ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}.'.format(results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks, spotify)


def write_tracks(text_file: str, tracks: dict, spotify):
    # Writes the information of all tracks in the playlist to a text file.

    with open(text_file, 'w+', encoding='utf-8') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                    print('here')
                else:
                    track = item
                    print('there')
                try:
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    csv_line = track_name + " " + track_artist + "\n"
                    try:
                        file_out.write(csv_line)
                    except UnicodeEncodeError:  # Most likely caused by non-English song names
                        print("Track named {} failed due to an encoding error. This is \
                            most likely due to this song having a non-English name.".format(track_name))
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                        track['name'], track['artists'][0]['name']))
                except TypeError:
                    print("type error")
            # 1 page = 50 results, check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


@client.command()
async def brawlstars(ctx, tag):
    bsclient = brawlstats.Client(bsTOKEN, is_async=True)
    tag = tag.replace('#', '')
    player = await bsclient.get_profile(tag)
    await ctx.send("You have "+str(player.trophies)+" trophies.")
    await ctx.send("You have "+str(player.team_victories)+" three vs three wins.")
    print(player.trophies)  # access attributes using dot.notation
    print(player.team_victories)  # use snake_case instead of camelCase
    print("Those are the player trophies and 3v3 victories")

    club = await player.get_club()
    if club is not None:  # check if the player is in a club
        print(club.tag)
        members = await club.get_members()  # members sorted by trophies

        # gets best 5 players or returns all members if the club has less than 5 members
        best_players = members[:5]
        for player in best_players:
            print(player.name, player.trophies)  # prints name and trophies
    print("Those are the top 5 club members")

    # get top 5 players in the world
    ranking = await bsclient.get_rankings(ranking='players', limit=5)
    for player in ranking:
        print(player.name, player.rank)
    print("Top five players in the world")

    # get top 5 mortis players in the US
    ranking = await bsclient.get_rankings(
        ranking='brawlers',
        region='us',
        limit=5,
        brawler='mortis'
    )
    for player in ranking:
        print(player.name, player.rank)
    print("Top five Mortis players"
          "")
    # Gets a player's recent battles
    battles = await bsclient.get_battle_logs(tag)
    i = 0
    while i < 5:
        print(battles[i].battle.mode)
        await ctx.send(battles[i].battle.mode)
        if (battles[i].battle.trophyChange) > 1:
            await ctx.send("You won this game")
        else:
            await ctx.send("You lost this game.")
        i=i+1
    print("Battle log")
    await bsclient.close()


@client.command()
async def tictactoeinfo(ctx):
    await ctx.send(":one: :two: :three:\n"
                   ":four: :five: :six:\n"
                   ":seven: :eight: :nine:")


@client.command()
async def spam(ctx, user : discord.Member):
    x = True
    while x:
        await ctx.send(user.mention)


@client.command()
async def tictactoe(ctx, p2 : discord.Member, troll=3):
    global botmark
    global notbotmark
    global GameOver
    global turn
    global board
    global player1
    global player2
    global count
    global winningConditions
    if p2 == client.user:
        winningConditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        if troll == 3:
            num = randint(1,2)
        elif troll == 1:
            num = 1
        elif troll == 2:
            num = 2
        p1 = ctx.message.author
        player1 = p1
        player2 = client.user
        if num == 1:
            turn = player1
            botmark = ':o2:'
            notbotmark = ':regional_indicator_x:'
        else:
            turn = player2
            botmark = ':regional_indicator_x:'
            notbotmark = ':o2:'
        count = 0
        global GameOver
        if GameOver:
            GameOver = False
            board = {0: ":white_large_square:", 1: ":white_large_square:", 2: ":white_large_square:",
                     3: ":white_large_square:", 4: ":white_large_square:", 5: ":white_large_square:",
                     6: ":white_large_square:", 7: ":white_large_square:", 8: ":white_large_square:"}
            if num == 2:
                await facebot(ctx, ctx.message.author)
            else:
                await go2nd(ctx)
        else:
            await ctx.send("Please finish the current game first.")
    else:
        p1 = ctx.message.author
        if GameOver:
            GameOver = False

            count = 0
            await ctx.send("Starting your Tic Tac Toe game.\nPlayer 1: " + str(p1)
                           +"\nPlayer 2: " + str(p2))

            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            await print_board(ctx, board)
            if troll == 3:
                num = randint(1,2)
            elif troll == 1:
                num = 1
            elif troll == 2:
                num = 2

            player1 = p1

            player2 = p2
            if num == 1:
                turn = p1
                await ctx.send("It is " + str(p1.mention) + "'s turn. Use !t <position from 1- 9>")
            elif num == 2:
                await ctx.send("It is " + str(p2.mention) + "'s turn. Use !t <position from 1- 9>")
                turn = p2
            winningConditions = [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 4, 8],
                [2, 4, 6]
            ]
        else:
            await ctx.send("Please finish the current game or use !t stop to end it.")


@client.command()
async def t(ctx, move, bot=False):
    if move != 'stop':
        move = int(move)
        global GameOver
        if not GameOver:
            global count
            global turn

            mark = ""
            if turn == ctx.author or bot:
                if player2 != client.user:
                    if turn == player1:
                        mark = ":regional_indicator_x:"
                    elif turn == player2:
                        mark = ":o2:"
                else:
                    if turn == player1:
                        mark = notbotmark
                    elif turn == player2:
                        mark = botmark
                if move < 1 or move > 9:
                    await ctx.send("Please enter a number from 1 - 9")
                elif board[move - 1] == ":white_large_square:":
                    count = count + 1
                    board[move-1] = mark
                    await print_board(ctx, board)
                    await checkwinner(ctx, board, mark)
                    if turn == player2:
                        turn = player1
                    elif turn == player1:
                        turn = player2
                    if not GameOver:
                        await ctx.send("It is " + str(turn.mention) + "'s turn. Use !t <position from 1- 9>")
                elif board[move-1] == ":white_large_square:" and bot:
                    count = count + 1
                    board[move-1] = mark
                    await print_board(ctx, board)
                    await checkwinner(ctx, board, mark)
                    if turn == player2:
                        turn = player1
                    elif turn == player1:
                        turn = player2
                    if not GameOver:
                        await ctx.send("It is " + str(turn.mention) + "'s turn. Use !t <position from 1- 9>")
                else:
                    await ctx.send("Someone already played on this square.")
            else:
                await ctx.send("It is not your turn.")
        else:
            pass
    else:
        await ctx.send("The game has been stopped.")
        GameOver = True
    if GameOver == False:
        if turn == client.user:
            await asyncio.sleep(1.5)
            await botgo(ctx)


async def fake_print_board(ctx, board):
    line1 = board[0], board[1], board[2]
    line2 = board[3], board[4], board[5]
    line3 = board[6], board[7], board[8]
    await ctx.send(line1)
    await ctx.send(line2)
    await ctx.send(line3)


async def print_board(ctx, board):
    line = ""
    for x in range(len(board)):
        if x ==2 or x == 5 or x == 8:
            line += " " + board[x]
            await ctx.send(line)
            line = ""
        else:
            line += " " + board[x]


async def checkwinner(ctx, board, mark):
    global GameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            await ctx.send("Game over")
            await ctx.send(mark + " wins!")
            GameOver = True
    if count >= 9:
        if GameOver == False:
            await ctx.send("It's a tie!")
            GameOver = True


async def facebot(ctx, player):
    await ctx.send("That was a mistake!\nPlayer 1: "+str(player)+"\nPlayer 2: "+str(client.user))
    await print_board(ctx, board)
    global turn
    turn = player2
    await ctx.send("It is "+turn.mention+"'s turn. Use !t <position from 1-9>")
    if turn == client.user:
        pos = 1 #first play
        if spaceIsFree(pos):
            await ctx.send("!t "+str(pos))
            await t(ctx, pos, True)
        return



async def go2nd(ctx):
    global player1
    global player2
    await ctx.send("That was a mistake!\nPlayer 1: "+str(player1)+"\nPlayer 2: "+str(player2))
    await print_board(ctx, board)
    global turn
    turn = player1
    await ctx.send("It is "+turn.mention+"'s turn. Use !t <position from 1-9>")


async def botgo(ctx):
    global botmark
    global notbotmark
    global getrippin
    global wherestuffat
    wherestuffat = 0
    global board
    count = 0
    for key in board.keys():
        if (board[key] == ':white_large_square:'):
            count = count + 1

    if botmark == ':regional_indicator_x:':
        if count == 5:
            getrippin = 0
            x = wherestuffat
            for key in board.keys():
                if (board[key] == notbotmark):
                    if key != wherestuffat:
                        y = key
                    #There new placement is y
            if x == 1:
                check = spaceIsFree(3)
                if check:
                    await ctx.send("!t 4")
                    await t(ctx, 4, True)
                else:
                    await ctx.send("!t 5")
                    await t(ctx, 5, True)
                    wherestuffat = 1
            if x == 2:
                check = spaceIsFree(4)
                if check:
                    await ctx.send("!t 5")
                    await t(ctx, 5, True)
                else:
                    await ctx.send("!t 7")
                    await t(ctx, 7, True)
                    wherestuffat = 2
            if x == 3:
                check = spaceIsFree(1)
                if check:
                    await ctx.send("!t 2")
                    await t(ctx, 2, True)
                else:
                    await ctx.send("!t 5")
                    await t(ctx, 5, True)
                wherestuffat = 3
            if x == 4:
                stop = 0
                check = spaceIsFree(2)
                if not check:
                    await ctx.send("!t 7")
                    await t(ctx, 7, True)
                    stop = 1
                check = spaceIsFree(6)
                if not check:
                    await ctx.send("!t 3")
                    await t(ctx, 3, True)
                    stop = 1
                if stop == 0:
                    getrippin = 1
                wherestuffat = 4
            if x == 5:
                check = spaceIsFree(2)
                if check:
                    await ctx.send("!t 3")
                    await t(ctx, 3, True)
                else:
                    await ctx.send("!t 5")
                    await t(ctx, 5, True)
                wherestuffat = 5
            if x == 6:
                check = spaceIsFree(4)
                if check:
                    await ctx.send("!t 5")
                    await t(ctx, 5, True)
                else:
                    await ctx.send("!t 3")
                    await t(ctx, 3, True)
                wherestuffat = 6
            if x == 7:
                check = spaceIsFree(1)
                if check:
                    await ctx.send("!t 2")
                    await t(ctx, 2, True)
                else:
                    await ctx.send("!t 5")
                    await t(ctx, 5, True)
            if x == 8:
                check = spaceIsFree(3)
                if check:
                    await ctx.send("!t 4")
                    await t(ctx, 4, True)
                else:
                    await ctx.send("!t 3")
                    await t(ctx, 3, True)
                wherestuffat = 8

        elif count > 6:
            getrippin = 0
            for key in board.keys():
                if (board[key] == notbotmark):
                    x = key
            if x == 1:
                await ctx.send("!t 7")
                await t(ctx, 7, True)
                wherestuffat = 1
            if x == 2:
                await ctx.send("!t 9")
                await t(ctx, 9, True)
                wherestuffat = 2
            if x == 3:
                await ctx.send("!t 3")
                await t(ctx, 3, True)
                wherestuffat = 3
            if x == 4:
                await ctx.send("!t 9")
                await t(ctx, 9, True)
                wherestuffat = 4
            if x == 5:
                await ctx.send("!t 7")
                await t(ctx, 7, True)
                wherestuffat = 5
            if x == 6:
                await ctx.send("!t 9")
                await t(ctx, 9, True)
                wherestuffat = 6
            if x == 7:
                await ctx.send("!t 3")
                await t(ctx, 3, True)
                wherestuffat = 7
            if x == 8:
                await ctx.send("!t 7")
                await t(ctx, 7, True)
                wherestuffat = 8

        if count < 6:
            getrippin = 1
        if getrippin == 1:
            dontstop = True
            repeat = 0
            while dontstop:
                #if turn == client.user:
                bestScore = -100
                bestMove = 0
                for key in board.keys():
                    if (board[key] == ':white_large_square:'):
                        board[key] = botmark
                        score = minimax(board, 0, False)
                        board[key] = ':white_large_square:'
                        if (score > bestScore) and spaceIsFree(key):
                            bestScore = score
                            bestMove = key
                    else:
                        pass
                if spaceIsFree(bestMove + repeat):
                    await ctx.send("!t "+str(bestMove + 1 + repeat))
                    await t(ctx, bestMove+1+repeat, True)
                    dontstop = False
                else:
                    repeat = 1 + repeat

    elif botmark == ':o2:':
        getrippin = 0
        if count == 8:
            for key in board.keys():
                if (board[key] == notbotmark):
                    x = key
                    #x is where they played
                    wherestuffat = key
            check = spaceIsFree(4)
            if check:
                await ctx.send("!t 5")
                await t(ctx, 5, True)
            else:
                await ctx.send("!t 1")
                await t(ctx, 1, True)

        if count == 6:
            for key in board.keys():
                if (board[key] == notbotmark):
                    if key != wherestuffat:
                        x = key #new placement

            if x == 8:
                await ctx.send("!t 3")
                await t(ctx, 3, True)
            else:
                getrippin = 1

        if count < 5:
            getrippin = 1
        if getrippin == 1:
            dontstop = True
            repeat = 0
            while dontstop:
                #if turn == client.user:
                bestScore = -100
                bestMove = 0
                for key in board.keys():
                    if (board[key] == ':white_large_square:'):
                        board[key] = botmark
                        score = minimax(board, 0, False)
                        board[key] = ':white_large_square:'
                        if (score > bestScore) and spaceIsFree(key):
                            bestScore = score
                            bestMove = key
                    else:
                        pass

                if spaceIsFree(bestMove + repeat):
                    await ctx.send("!t "+str(bestMove + 1 + repeat))
                    await t(ctx, bestMove+1+repeat, True)
                    dontstop = False
                else:
                    repeat = 1 + repeat






def checkWhichMarkWon(mark):
    if board[0] == board[1] and board[0] == board[2] and board[0] == mark:
        return True
    elif (board[3] == board[4] and board[3] == board[5] and board[3] == mark):
        return True
    elif (board[6] == board[7] and board[6] == board[8] and board[6] == mark):
        return True
    elif (board[0] == board[3] and board[0] == board[6] and board[0] == mark):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    elif (board[0] == board[4] and board[0] == board[8] and board[0] == mark):
        return True
    elif (board[6] == board[4] and board[6] == board[3] and board[7] == mark):
        return True
    else:
        return False


def checkwinnernoendgame(board, mark):
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            return True


def checkdraw():
    count = 0
    for key in board.keys():
        if (board[key] == ':white_large_square:'):
            count = count + 1
    if count == 9:
        return True
    else:
        return False


def minimax(board, depth, isMaximizing):
    #maximizing =
    #minimizing =
    if checkwinnernoendgame(board, botmark):
        return 1

    elif checkwinnernoendgame(board, notbotmark):
        return -1

    elif checkdraw():
        return 0

    else:
        pass

    if isMaximizing == True:
        bestScore = 0

        for key in board.keys():
            if(board[key] == "white_large_square"):
                board[key] = botmark
                score = minimax(board, 0, False)
                board[key] = ":white_large_square:"
                if score > bestScore:
                    bestScore = score

        return bestScore

    elif isMaximizing == False:
        bestScore = 1000
        for key in board.keys():
            if(board[key] == ":white_large_square:"):
                board[key] = notbotmark
                score = minimax(board, 0, True)
                board[key] = ":white_large_square:"
                if score < bestScore:
                    bestScore = score

        return bestScore

    else:
        pass


def spaceIsFree(position):
    if board[position] == ":white_large_square:":
        return True
    else:
        return False


client.run(TOKEN)
