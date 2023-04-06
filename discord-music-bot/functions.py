import discord
import os

async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        server = ctx.guild
        print("Joined a voice chat in the server: " + str(server))
        await ctx.guild.change_voice_state(channel = channel, self_mute=False, self_deaf=False)
    except AttributeError:
        await ctx.send("You are not in a voice channel.")
    except discord.errors.ClientException:
        pass

    try:
        os.makedirs(os.path.join(str(ctx.guild)), 0o666)
        file = open(str(os.path.join(str(ctx.guild))) + "/" + str(ctx.guild) + ".txt", "w+")  # create a file called servername.txt
        file.close()
    except Exception:
        try :
            file1 = open(str(ctx.guild) + '/' + str(ctx.guild) + ".txt", "a")
            file1.close()
        except Exception as e:
            print("There was a problem creating the file.")
            print(str(e))
