# amen_bot
This is a discord bot used to show some stats about a certain word ("Amen" or "amen") said at a certain hour (23:23)
The main commands are :
- **!amenStats** : when called, the bot will answer after few seconds by a picture on which we can fin 3 graphs :
![the stats](/test.png)
  - top graph shows the monthly amount of 'Amen' said at 23:23 for each member
  - bottom left shows the proportion of 'Amen' said not exactly at 23:23 (23:22 or after 23:23)
  - bottom right : a bar graph that shows the best streak, meaning the best consecutive amount of days where one person said a correct amen

# techno
This bot works with python 3.6 and mainly relies on [discord](https://pypi.org/project/discord.py/) and [matplotlib.pyplot](https://matplotlib.org/3.1.1/)
