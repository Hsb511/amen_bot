# amen_bot
This is a discord bot used to show some stats about a certain word ("Amen" or "amen") said at a certain hour (23:23)
The main commands are :
- **!amenStats** : when called, the bot will answer after few seconds by a picture on which you can find 3 graphs :
![the stats](/test.png)
  - top graph shows the monthly amount of 'Amen' said at 23:23 for each member
  - bottom left shows the proportion of 'Amen' said not exactly at 23:23 (23:22 or after 23:23)
  - bottom right : a bar graph that shows the best streak, meaning the best consecutive amount of days where one person said a correct amen
- **!amensAmount [member_nick]** : command that prints the amount of amen said for all member that have [member_nick] in their nick name. If nothing is specified, it will send the stats of the person that executed the command

# Technical points
This bot works with python 3.6 and mainly relies on [discord](https://pypi.org/project/discord.py/) and [matplotlib.pyplot](https://matplotlib.org/3.1.1/)
To run a python bot, you just have to type `python amen_bot.py` in a bash on Linux or the cmd for Windows with python 3.6 and the libraries installed
