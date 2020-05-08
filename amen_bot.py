# -*- coding: utf-8 -*-
#! /usr/bin/env python3
# Work with Python 3.6
import json
import asyncio
from discord.ext.commands import Bot
import discord
import matplotlib.pyplot as plt
import time, datetime, calendar
import numpy as np
import pytz


# Load the bot's configuration
with open("resources/configuration/config.json") as f:
    CONFIGURATION = json.load(f)

# Getting the discord's bot token that you can find here : https://discordapp.com/developers/applications/me
with open("resources/configuration/bot.txt", "r") as f:
    TOKEN = f.readline()[:-1]
    CHANNEL_ID = f.readline()

# Creating the bot client
client = Bot(command_prefix=CONFIGURATION['cmd_prefix'])

mgs = []    # Empty list to put all the messages in the log
times = {}  # Stores each datetime by members where a correct 'Amen' has been said
fails = {}  # Stores the datime by members of the failed 'Amen' (said too soon or too late)

def get_channel_from_context(context):
    sent_channel = context.message.channel
    all_channels = sent_channel.server.channels
    for channel in all_channels:
        if channel.id == CHANNEL_ID:
            return channel
    return sent_channel

async def fill_times(context):
    """ Fill the ``times`` variable with data retrieved from the channel's messages history."""
    # We get the last max_msg messages from the channel where the command has been called
    async for x in client.logs_from(get_channel_from_context(context), CONFIGURATION['max_msg']):
        if (x.content != None):
            # We filter and store the messages containing 'amen' and not sent by a bot
            if "amen" in x.content.lower():
                if str(x.author) not in CONFIGURATION['excluded_users']:
                    mgs.append(x)
                    if not ((x.timestamp.minute == 22 and x.timestamp.hour == 22) or 'amen+' in x.content.lower() or 'amen +' in x.content.lower() or '!amen' in x.content):
                        u_times = times.setdefault(x.author, [])
                        u_times.append(x.timestamp)


def plt_temporel(mgs, fig):
    """ Function used to plot the first graph : the monthly amount of correct 'amen' said """
    print("*** drawing temporal graph ***")
    dates = [datetime.date(2017, k, 23) for k in range (1, 13)] + [datetime.date(2018, k, 23) for k in range (1, 13)] + [datetime.date(2019, k, 23) for k in range (1, 13)] + [datetime.date(2020, k, 23) for k in range (1, 4)]
    flocks = {}
    for message in mgs:
        if not message.author in flocks and str(message.author) not in CONFIGURATION['excluded_users']:
            flocks[message.author] = [0 for k in range(len(dates))]

    for message in reversed(mgs):
        if str(message.author) not in CONFIGURATION['excluded_users'] and message.timestamp.minute == 23:
            try:
                flocks[message.author][(message.timestamp.year - 2017) * 12 + message.timestamp.month - 1] += 1
            except:
                print("une erreur est survenue")

    half_dates = []
    for i in range(len(dates)):
        if (i%2 == 0):
            half_dates.append(dates[i])
    temp_plot = fig.add_subplot(3, 1, 1)
    temp_plot.set_xticks(half_dates)
    temp_plot.set_xticklabels([str(half_date.month) + " / " + str(half_date.year)[2:5] for half_date in half_dates], rotation=45, fontsize=8, horizontalalignment="center")
    temp_plot.set_title("Répartition temporelle des 'Amen' dits sur ce channel discord")
    temp_plot.set_xlabel("mois")
    temp_plot.set_yticks(np.arange(1, 30, step=4))
    temp_plot.set_yticklabels(np.arange(1, 30, step=4), fontsize=8,)
    temp_plot.set_ylabel("nombre de 'Amen' par mois")

    for my_flock in CONFIGURATION['flocks']:
        for flock in flocks:
            if (my_flock in str(flock)):
                temp_plot.plot(dates, flocks[flock], marker='+', linestyle='-', label=str(flock).split("#")[0] + ": "+str(sum(flocks[flock])))
                break
    temp_plot.legend(ncol=2, prop={'size': 6})
    temp_plot.grid(True)
    plt.subplots_adjust(wspace= 1.0)
    print("*** temporal graph drawn ***")

def plt_fail(mgs, fig):
    """ Function called to display the second graph to show the proportion of errors by members """
    print("*** drawing fails graph ***")
    fail_plot = fig.add_subplot(2, 2, 3)
    
    # We gather the fails in a global variable "fails" 
    gather_fails(mgs)

    # We arange the data to prepare them for the graph
    errors = []
    people = []
    for my_flock in CONFIGURATION['flocks']:
        for flock in fails:
            if (my_flock in str(flock)):
                failsAmount = len(fails[flock])
                if (failsAmount != 0):
                    errors.append(failsAmount)
                    people.append(str(flock).split("#")[0])
                break

    # We construct the pie chart and add it to the main figure
    texts = fail_plot.pie(errors, labels=people, shadow=True, autopct=autopct_format(errors), startangle=90)[1]
    for text in texts:
        text.set_fontsize(8)
    fail_plot.axis('equal') 
    fail_plot.set_title("Répartition des 'Amens' ratés : \n les 'Amen+' ou ceux à 23:22")
    plt.subplots_adjust(wspace= 1.0)
    print("*** fails graph drawn ***")

def gather_fails(mgs):
    """ Function to gather failed Amen """
    print("*** gathering fails ***")
    if fails == {}:
        today_amen = {} # dict of newest correct amen by member

        # We gather the authors
        for message in mgs:
            if not message.author in fails and str(message.author) != '23-robot#3554':
                fails[message.author] = []


        # we iterate through all the messages
        for message in reversed(mgs):
            if str(message.author) != '23-robot#3554':
                if "amen" in message.content.lower():
                    if (message.timestamp.hour == 22 or message.timestamp.hour == 23) and message.timestamp.minute == 23:
                        u_today_amen = today_amen.setdefault(message.author, [])
                        u_today_amen.append(str(message.timestamp.year)+str(message.timestamp.month)+str(message.timestamp.day))
                    if message.timestamp.hour == 22 or message.timestamp.hour == 23:
                        if message.timestamp.minute == 22 or message.timestamp.minute == 24 or message.timestamp.minute == 25:
                            fails[message.author].append(message.timestamp)

        # We check that if a correct amen has been said, an amen said shortly after that is not a fail
        for member in fails:
            previous_fail = datetime.date(2323, 11, 23)
            for fail in fails[member]:
                # we check if a correct amen has not been said today or if another fail has been said today, if so we remove the fail
                if (str(fail.year)+str(fail.month)+str(fail.day) in today_amen[member] and fail.minute != 22) or (previous_fail.year == fail.year and previous_fail.month == fail.month and previous_fail.day == fail.day):
                    fails[member].remove(fail)

                previous_fail = fail

def autopct_format(values):
    """ Fuction used to format the value of a pie chart """
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format

def plt_streak(times, fig):
    """ Function used to show the best streak e.g. the maximum of consecutive days a correct 'amen' has been said by a member """
    print("*** Drawing streak graph ***")
    streak_plot = fig.add_subplot(2, 2, 4)

    flocks = {}
    for flock in times:
        flocks[flock] = [0, times[flock][0], 1]
        for time in times[flock]:
            time_difference = flocks[flock][1] - time
            if (time_difference.days == 0 and time_difference.seconds > 86300) or (time_difference.days == 1 and time_difference.seconds < 61):
                flocks[flock][2] += 1
            else:
                if flocks[flock][0] < flocks[flock][2]:
                    flocks[flock][0] = flocks[flock][2]
                flocks[flock][2] = 1
            flocks[flock][1] = time

    streak = []
    people = []
    for my_flock in CONFIGURATION['flocks']:
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
    for i, v in enumerate(streak):
        streak_plot.text(v + 3, i + .25, str(v), fontweight='bold')
    print("*** streak graph drawn ***")

@client.command(pass_context=True)
async def amensAmount(context, *player):
    """ The second command to show the amount of amens for one player """
    if (player == ()):
        player = str(context.message.author)
    else:
        player = player[0]

    if (times == {}):
        await fill_times(context)

    # Variable used to check if noone has been found
    found = False

    # We iterate through all the time data
    for flock in times:
        if player.lower() in str(flock).lower():
            amensAmount = 1
            # We check all the data : if 2 amens have been said the same day, only one is counted
            for i in range(len(times[flock]) - 1):
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


@client.command(pass_context=True)
async def failsAmount(context, *player):
    """ The third command to show the amount of fails for one player """
    if not player:
        player = str(context.message.author)
    else:
        player = player[0]

    # We gather the data relative to the "amen" msgs and their time
    if (times == {} or mgs == []):
        await fill_times(context)

    gather_fails(mgs)

    # Variable used to check if noone has been found
    found = False

    for flock in fails:
        if player.lower() in str(flock).lower():
            found = True
            await client.say(str(flock).split("#")[0] + " s'est fail le : ")
            for fail in fails[flock]:
                await client.say("\t" + fail.strftime("%d/%m/%Y") + " à " + fail.strftime("%Hh%M"))
    
    # If none has been found we notify it
    if not found :
        await client.say(player + " n'a pas été trouvé parmis les membres de ce channel !")

#TODO create a command that displays only the temporal graph by chosing the starting and ending month by default all the period is shown

@client.command(pass_context=True)
async def amenStats(context):
    """ The first command to show the different stats """
    print("*** the command !amenStats has been requested ***")
    await fill_times(context)
    
    # We clear the figure and create a new one
    plt.clf()
    fig = plt.figure()

    # We call the 3 methods that create the graphs
    plt_temporel(mgs, fig)
    plt_fail(mgs, fig)
    plt_streak(times, fig)

    # We store it in a png and we send it
    f = plt.gcf()
    f.savefig(CONFIGURATION['picture_name'])
    await client.send_file(context.message.channel, CONFIGURATION['picture_name'])


# Starts the bot
client.run(TOKEN)