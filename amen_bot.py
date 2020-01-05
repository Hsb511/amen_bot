# Work with Python 3.6
import asyncio
from discord.ext.commands import Bot
import matplotlib.pyplot as plt
import numpy as np
import time, datetime

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
                    if not ((x.timestamp.minute == 22 and x.timestamp.hour == 22) or 'amen+' in x.content.lower() or 'amen +' in x.content.lower()):
                        if x.author not in times:
                            times[x.author] = [x.timestamp]
                        else:
                            times[x.author].append(x.timestamp)

    # We cleare the figure and create a new one
    plt.clf()
    fig = plt.figure()

    # We call the 3 methods that create the graphs
    plt_temporel(mgs, fig)
    plt_fail(mgs, fig)
    plt_streak(times, fig)

    # We store it in a png and we send it
    f = plt.gcf()
    f.savefig("test.png")
    await client.send_file(context.message.channel,'test.png')

""" Function used to plot the first graph : the monthly amount of correct 'amen' said """
def plt_temporel(mgs, fig):
    dates = [datetime.date(2017, k, 23) for k in range (1, 13)] + [datetime.date(2018, k, 23) for k in range (1, 13)] + [datetime.date(2019, k, 23) for k in range (1, 13)] + [datetime.date(2020, k, 23) for k in range (1, 2)]
    flocks = {}
    for message in mgs:
        if not message.author in flocks and str(message.author) != '23-robot#3554':
            flocks[message.author] = [0 for k in range(len(dates))]

    for message in reversed(mgs):
        if str(message.author) != '23-robot#3554' and message.timestamp.minute == 23:
            flocks[message.author][(message.timestamp.year - 2017) * 12 + message.timestamp.month - 1] += 1

    half_dates = []
    for i in range(len(dates)):
        if (i%2 == 0):
            half_dates.append(dates[i])
    temp_plot = fig.add_subplot(3, 1, 1)
    temp_plot.set_xticks(half_dates)
    temp_plot.set_xticklabels([str(half_date.month) + " / " + str(half_date.year)[2:5] for half_date in half_dates], rotation=45, fontsize=8, horizontalalignment="center")
    temp_plot.set_title("Répartition temporelle des 'Amen' dits sur ce channel discord")
    temp_plot.set_xlabel("mois")
    temp_plot.set_yticks(np.arange(1, 22, step=2))
    temp_plot.set_yticklabels(np.arange(1, 22, step=2), fontsize=8,)
    temp_plot.set_ylabel("nombre de 'Amen' par mois")

    for my_flock in my_flocks:
        for flock in flocks:
            if (my_flock in str(flock)):
                temp_plot.plot(dates, flocks[flock], marker='+', linestyle='-', label=str(flock).split("#")[0])
                break
    temp_plot.legend(ncol=2)
    temp_plot.grid(True)
    plt.subplots_adjust(wspace= 1.0)

""" Function called to display the second graph to show the proportion of errors by members """
def plt_fail(mgs, fig):
    fail_plot = fig.add_subplot(2, 2, 3)

    flocks = {}
    for message in mgs:
        if not message.author in flocks and str(message.author) != '23-robot#3554':
            flocks[message.author] = 0

    for message in reversed(mgs):
        if str(message.author) != '23-robot#3554':
            if (message.timestamp.minute == 22 and message.timestamp.hour == 22) or 'amen+' in message.content.lower() or 'amen +' in message.content.lower():
                flocks[message.author] += 1
    
    errors = []
    people = []
    for my_flock in my_flocks:
        for flock in flocks:
            if (my_flock in str(flock)):
                if (flocks[flock] != 0):
                    errors.append(flocks[flock])
                    people.append(str(flock).split("#")[0])
                break

    texts = fail_plot.pie(errors, labels=people, shadow=True, autopct=autopct_format(errors), startangle=90)[1]
    for text in texts:
        text.set_fontsize(8)
    fail_plot.axis('equal')
    fail_plot.set_title("Répartition des 'Amens' ratés : \n les 'Amen+' ou ceux à 23:22")
    plt.subplots_adjust(wspace= 1.0)

""" Fuction used to format the value of a pie chart """
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format

""" Function used to show the best streak e.g. the maximum of consecutive days a correct 'amen' has been said by a member """
def plt_streak(times, fig):
    streak_plot = fig.add_subplot(2, 2, 4)

    flocks = {}

    for flock in times:
        flocks[flock] = [0, times[flock][0], 1]
        for time in times[flock]:
            if ((flocks[flock][1] - time).days == 0 and (flocks[flock][1] - time).seconds > 86300) or ((flocks[flock][1] - time).days == 1 and (flocks[flock][1] - time).seconds < 61):
                flocks[flock][2] += 1
            else:
                if flocks[flock][0] < flocks[flock][2]:
                    flocks[flock][0] = flocks[flock][2]
                flocks[flock][2] = 1
            flocks[flock][1] = time

    streak = []
    people = []
    for my_flock in my_flocks:
        for flock in flocks:
            if (my_flock in str(flock)):
                if (flocks[flock] != 0):
                    streak.append(flocks[flock][0])
                    people.append(str(flock).split("#")[0])
                break

    streak_plot.set_title("Meilleure série de 'Amen' \n en jours consécutifs")
    streak_plot.barh(people, streak)
    streak_plot.invert_yaxis()
    streak_plot.set_xlabel('Nombre de jours consécutifs')


# Starts the bot
client.run(TOKEN)
