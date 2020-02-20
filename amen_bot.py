# Work with Python 3.6
import asyncio
from discord.ext.commands import Bot
import matplotlib.pyplot as plt
import time, datetime, calendar
import pytz

from temporal_graph import plt_temporal
from fails_graph import plt_fail
from fails_manager import gather_fails
from streak_graph import plt_streak

# Getting the discord's bot token that you can find here : https://discordapp.com/developers/applications/me
f = open("bot.txt", "r")
TOKEN = f.readline()

# Setting the bot's command prefix
BOT_PREFIX = ("?", "!")

# Creating the bot client
client = Bot(command_prefix=BOT_PREFIX)

my_flocks = ["giorn", "Hsb511", "Marshall", "benzayolo", "p76dub", "Braing"]

mgs = []    # Empty list to put all the messages in the log
times = {}  # Stores each datetime by members where a correct 'Amen' has been said
fails = {}  # Stores the datime by members of the failed 'Amen' (said too soon or too late)

""" The first command to show the different stats """
@client.command(pass_context=True)
async def amenStats(context):
    # We get the last 23000 messages from the channel where the command has been called
    async for x in client.logs_from(context.message.channel, 23000):
        if (x.content != None):
            # We filter and store the messages containing 'amen' and not sent by a bot
            if "amen" in x.content.lower():
                if str(x.author) != '23-robot#3554':
                    mgs.append(x)
                    if not ((x.timestamp.minute == 22 and x.timestamp.hour == 22) or 'amen+' in x.content.lower() or 'amen +' in x.content.lower() or '!amen' in x.content):
                        if x.author not in times:
                            times[x.author] = [x.timestamp]
                        else:
                            times[x.author].append(x.timestamp)

    # We cleare the figure and create a new one
    plt.clf()
    fig = plt.figure()

    # We call the 3 methods that create the graphs
    plt_temporal(mgs, fig, my_flocks)
    plt_fail(mgs, fig, my_flocks, fails)
    plt_streak(times, fig, my_flocks)

    # We store it in a png and we send it
    f = plt.gcf()
    f.savefig("test.png")
    await client.send_file(context.message.channel,'test.png')

""" The second command to show the amount of amens for one player """
@client.command(pass_context=True)
async def amensAmount(context, *player):
    if (player == ()):
        player = str(context.message.author)
    else:
        player = player[0]

    if (times == {}):
        # We get the last 23000 messages from the channel where the command has been called
        async for x in client.logs_from(context.message.channel, 23000):
            if (x.content != None):
                # We filter and store the messages containing 'amen' and not sent by a bot
                if "amen" in x.content.lower():
                    if str(x.author) != '23-robot#3554':
                        mgs.append(x)
                        if not ((x.timestamp.minute == 22 and x.timestamp.hour == 22) or 'amen+' in x.content.lower() or 'amen +' in x.content.lower() or '!amen' in x.content):
                            if x.author not in times:
                                times[x.author] = [x.timestamp]
                            else:
                                times[x.author].append(x.timestamp)

    # Variable used to check if noone has been found
    found = False

    # We iterate through all the time data
    for flock in times:
        if player.lower() in str(flock).lower():
            amensAmount = 1
            # We check all the data : if 2 amens have been said the same day, only one is counted
            for i in range(len(times[flock]) - 1):
                print(times[flock])
                print(len(times[flock]))
                if not (times[flock][i+1].year == times[flock][i].year and times[flock][i+1].month == times[flock][i].month and times[flock][i+1].day == times[flock][i].day):
                    # If it's a "correct" amen
                    if (times[flock][i+1].minute == 23):
                        amensAmount += 1
            # For each member's nick that matches the input name we display their amens amount
            await client.say(str(amensAmount) + " amen(s) dit(s) au total pour " + str(flock).split("#")[0])
            found = True

    # If noone has been found we notify it
    if not found :
        await client.say(player + " n'a pas été trouvé parmis les membres de ce channel !")


""" The third command to show the amount of fails for one player """
@client.command(pass_context=True)
async def failsAmount(context, *player):
    if (player == ()):
        player = str(context.message.author)
    else:
        player = player[0]

    # We gather the data relative to the "amen" msgs and their time
    if (times == {} or mgs == []):
        # We get the last 23000 messages from the channel where the command has been called
        async for x in client.logs_from(context.message.channel, 23000):
            if (x.content != None):
                # We filter and store the messages containing 'amen' and not sent by a bot
                if "amen" in x.content.lower():
                    if str(x.author) != '23-robot#3554':
                        mgs.append(x)
                        if not ((x.timestamp.minute == 22 and x.timestamp.hour == 22) or 'amen+' in x.content.lower() or 'amen +' in x.content.lower() or '!amen' in x.content):
                            if x.author not in times:
                                times[x.author] = [x.timestamp]
                            else:
                                times[x.author].append(x.timestamp)


    global fails 
    fails = gather_fails(mgs, fails)

    # Variable used to check if noone has been found
    found = False

    for flock in fails:
        if player.lower() in str(flock).lower():
            await client.say(str(flock).split("#")[0] + " s'est fail le : ")
            for fail in fails[flock]:
                await client.say("\t" + fail.strftime("%d/%m/%Y") + " à " + fail.strftime("%Hh%M"))
    
    # If noone has been found we notify it
    if not found :
        await client.say(player + " n'a pas été trouvé parmis les membres de ce channel !")


# Starts the bot
client.run(TOKEN)
