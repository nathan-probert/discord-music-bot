import asyncio
from random import randint
import discord
from discord.ext import commands
import os
import musicFunctions
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
                "!pllist <playlist number>\n\nPrints all songs of the playlist\n\n"
                "!pladd <playlist number> <song name>\nAdds a song to the playlist\n\n"
                "!pldelete <playlist number> <song name>\Deletes a song from the playlist\n\n"
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
    

@client.command()
async def spam(ctx, user : discord.Member, numPings=100):
    i = 0

    # so i dont get spammed
    if ((user.name == "Proby.8") or (user.name == "MiKe WaZonsKi")):
        await ctx.send("Nice try")
        return

    while i < int(numPings):
        await ctx.send(user.mention)
        i+=1


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
    if (len(playlistName) == 1):
        print("here")
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
async def pllist(ctx, playlistNum=-1):
    if (playlistNum == -1):
        i=1
        await ctx.send("Here is a list of all playlists:")
        playlistsToSend = ""
        playlists = os.listdir("playlists")
        for p in playlists:
            p=p.replace(".txt", "\n")
            playlistsToSend += str(i) + ": " + p
            i+=1
        await ctx.send(f"{playlistsToSend}")
    else:
        i = 1
        playlists = os.listdir("playlists")
        for p in playlists:
            if (i == playlistNum):
                playlist = p
            i+=1
        filename = (f"playlists\\{playlist}")

        with open(filename, "r") as f:
            lines = f.readlines()

        songsToSend = ""
        for l in lines:
            songsToSend += l + "\n"
        try:
            await ctx.send("```" + songsToSend + "```")
        except:
            await ctx.send("Your playlist exceeds discord's 2000 char limit. Please look at this file instead")
            await ctx.send(file=discord.File(filename))


@client.command()
async def pldelete(ctx, playlistNum, *, songtitle):
    i = 1
    playlists = os.listdir("playlists")
    for p in playlists:
        if (str(i) == playlistNum):
            playlist = p
        i+=1
    
    delete = False
    filename = (f"playlists\\{playlist}")

    with open(filename, "r") as f:
        lines = f.readlines()

    oglines = lines

    songtitle = songtitle.lower()
    songtitle = songtitle.strip("\n")
    songtitle = songtitle.replace(" ", "")

    with open(filename, "w") as f:
        i=0
        for line in lines:
            line = line.lower()
            line = line.strip("\n")
            line = line.replace(" ", "")

            if line != songtitle:
                f.write(oglines[i])
            else:
                await ctx.send(f"Your song {oglines[i]} has been deleted from {playlist}")
            i+=1
    if (delete == False):
        await ctx.send("We could not find that song. "
                       "Please use !pllist <playlist name> to see your playlist, "
                       "as any spelling mistakes you made when entering the song name "
                       "are not corrected and must be entered here as well.")


@client.command()
async def pladd(ctx, playlistNum, *, songtitle):
    i = 1
    playlists = os.listdir("playlists")
    for p in playlists:
        if (str(i) == playlistNum):
            playlist = p
        i+=1
    
    filename = (f"playlists\\{playlist}")
    with open(filename, "a") as fw:
        fw.write(songtitle)

    await ctx.send(f"Added your song {songtitle} to your playlist {playlist}")


GameOver = True
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
    

# runs the bot
client.run(TOKEN)