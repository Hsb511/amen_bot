from fails_manager import gather_fails
import matplotlib.pyplot as plt

""" Function called to display the second graph to show the proportion of errors by members """
def plt_fail(mgs, fig, my_flocks, fails):
    fail_plot = fig.add_subplot(2, 2, 3)
    
    # We gather the fails in a global variable "fails" 
    gather_fails(mgs, fails)

    # We arange the data to prepare them for the graph
    errors = []
    people = []
    for my_flock in my_flocks:
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

""" Fuction used to format the value of a pie chart """
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format