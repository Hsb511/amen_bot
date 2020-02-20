import datetime

""" Function to gather failed Amen """
def gather_fails(mgs, fails):
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
                        if (not message.author in today_amen):
                            today_amen[message.author] = [str(message.timestamp.year)+str(message.timestamp.month)+str(message.timestamp.day)]
                        else:
                            today_amen[message.author].append(str(message.timestamp.year)+str(message.timestamp.month)+str(message.timestamp.day))
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
    
    return fails