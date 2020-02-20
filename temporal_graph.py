import datetime
import matplotlib.pyplot as plt
import numpy as np

""" Function used to plot the first graph : the monthly amount of correct 'amen' said """
def plt_temporal(mgs, fig, my_flocks):
    dates = [datetime.date(2017, k, 23) for k in range (1, 13)] + [datetime.date(2018, k, 23) for k in range (1, 13)] + [datetime.date(2019, k, 23) for k in range (1, 13)] + [datetime.date(2020, k, 23) for k in range (1, 4)]
    flocks = {}
    for message in mgs:
        if not message.author in flocks and str(message.author) != '23-robot#3554':
            flocks[message.author] = [0 for k in range(len(dates))]

    for message in reversed(mgs):
        if str(message.author) != '23-robot#3554' and message.timestamp.minute == 23:
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
