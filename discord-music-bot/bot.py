import discord

file1 = open("..lib\\secret.txt", 'r')
TOKEN = file1.readline()
file1.close() 

client = discord.ext.commands.Bot(command_prefix="!", help_command=None)

# runs the bot
client.run(TOKEN)