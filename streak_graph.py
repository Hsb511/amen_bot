import matplotlib.pyplot as plt

""" Function used to show the best streak e.g. the maximum of consecutive days a correct 'amen' has been said by a member """
def plt_streak(times, fig, my_flocks):
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
    for i, v in enumerate(streak):
        streak_plot.text(v + 3, i + .25, str(v), fontweight='bold')