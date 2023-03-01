#######################################################################
# Example:
# A list of security events with adverse consequences with P(TE) = in %
# and 90% of confidence interval:
# lower bound of the interval - LOWER_LOSS(TE)
# upper bound of the interval - UPPER_LOSS(TE)
#
# Existing or planned security controls compensating P(TE) in %
# 
# Number of simulations: i.e. 1000
#
# Presumed risk tolerance with the following distribution:
#    50 000 EUR - 90%
#   250 000 EUR - 50%
#   500 000 EUR - 20%
#   750 000 EUR -  5%
# 1 000 000 EUR -  1%
# 5 000 000 EUR -  0.1%
########################################################################

# list of security events [probability, lower bound loss, upper bound loss, description]
events = {
    "event1": (0.11, 100000, 400000, "Successful DDoS on the cloud base core app"),
    "event2": (0.08, 500000, 1500000, "Sensitive data exfiltration"),
    "event3": (0.03, 200000, 1000000, "Malicious code injected into production pipeline"),
    "event4": (0.2, 10000, 100000, "Laptop with sensitive data lost/stolen"),
    "event5": (0.12, 15000, 50000, "Malicious code in 3rd party dependencies"),
    "event6": (0.15, 1000, 150000, "Broken backups"),
    "event7": (0.01, 1000000, 12000000, "Malware attack, knocked out internal network"),
    "event8": (0.05, 10000, 500000, "Insider's threat"),
    "event9": (0.01, 100000, 500000, "Terrorist attack"),
    "event10": (0.25, 5000, 50000, "Broken app release")
}

# list of mitigating security controls [annual cost, with impact on event probability reduction]
sec_controls = {
    "event1": (70000, 0.65),
    "event2": (200000, 0.55),
    "event3": (250000, 0.7),
    "event4": (30000, 0.7),
    "event5": (25000, 0.4),
    "event6": (100000, 0.9),
    "event7": (800000, 0.85),
    "event8": (250000, 0.5),
    "event9": (300000, 0.6),
    "event10": (25000, 0.45)
}

# defined risk tolerance
risk_tolerance = [
    (100000, 90), 
    (250000, 80), 
    (500000, 40), 
    (750000, 15), 
    (1000000, 2), 
    (10000000, 0.1)
]

# simulation parameters

STEP = 5000
NO_SIMULATIONS = 1000


### computing functions

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def threat_event_happened(event_p, reduct_p):
    return np.random.rand() < event_p*(1-reduct_p)

def threat_event_loss(lower_bnd, upper_bnd):
    mean = (np.log(lower_bnd) + np.log(upper_bnd))/2
    std_deviation = (np.log(upper_bnd) - np.log(lower_bnd))/3.29
    return round(float(np.random.lognormal(mean, std_deviation)),2)

def loss_distribution(events_dict, no_of_simulations):
    i = 0
    event_keys = []
    events_keys = events_dict.keys()
    sim_list = []
    for i in range(no_of_simulations):
        rnd_list = []
        loss_sum = 0
        for key in events_keys:
            if threat_event_happened(events_dict[key][0],0):
                event_loss = threat_event_loss(events_dict[key][1], events_dict[key][2])
            else:
                event_loss = 0
            rnd_list.append("{:.2f}".format(event_loss))
        for each_loss in range(len(rnd_list)):
            loss_sum += float(rnd_list[each_loss])
        sim_list.append(round(loss_sum, 2))
    return sim_list # return a list of lists for each test for all events.

def loss_distribution_reduced(events_dict, controls_dict, no_of_simulations):
    i = 0
    events_keys = []
    events_keys = events_dict.keys()
    sim_list = []
    for i in range(no_of_simulations):
        rnd_list = []
        loss_sum = 0
        for key in events_keys:
            if threat_event_happened(events_dict[key][0],controls_dict[key][1]):
                event_loss = threat_event_loss(events_dict[key][1], events_dict[key][2])
            else:
                event_loss = 0
            rnd_list.append("{:.2f}".format(event_loss))
        for each_loss in range(len(rnd_list)):
            loss_sum += float(rnd_list[each_loss])
        sim_list.append(round(loss_sum,2))
    return sim_list # return a list of lists for each test for all events.

def loss_average(lst):
    accu = 0
    for loss in lst:
        accu += loss
    loss_ave = round(accu/len(lst), 2)
    return loss_ave

def draw_loss_distribution(lst, fig_name):
    ax = 0
    losses_series = 0
    losses_series = pd.Series(lst)
    ax = losses_series.plot(**{'color': 'blue', 'marker': '.'})
    ax.set_xlabel('No. of tests')
    ax.set_ylabel('Loss magnitude')
    ax.set_title('Loss distribution')
    ax.figure.savefig(fig_name)
    ax.cla()
    plt.close()


def loss_exceedance_curve(lst, STEP):
    loss_ex_lst = []
    losses_count = 0
#    for loss in lst:
#        if loss > 0: losses_count += 1
    for x in range(0,5000000,STEP):
        accu = 0
        for loss in lst:
            if loss > 0 and loss > x: 
                accu += 1
        loss_ex_lst.append([x,round(accu/len(lst),2)*100])
    return loss_ex_lst

def draw_loss_exceedance(lst, lst_for_risk_tolerance, fig_name):
    fig, ax = plt.subplots()
    for item in [lst, lst_for_risk_tolerance]:
        x = []
        y = []
        for n, p in item:
            x.append(n)
            y.append(p)
        ax.plot(x, y, linewidth=2)
    ax.set_xscale('log')
    ax.set_xlabel('Loss magnitude in EUR [log]')
    ax.set_ylabel('P(loss exceeded) in %')
    ax.set_title('Loss exceedance curve')
    fig.savefig(fig_name)
    fig.clear()

# run

losses_no_ctrls = loss_distribution(events, NO_SIMULATIONS)
losses_with_ctrls = loss_distribution_reduced(events, sec_controls, NO_SIMULATIONS)

# draw loss distribution without security controls in place
draw_loss_distribution(losses_no_ctrls, 'Fig-1.png')

# draw loss distribution with security controls in place
draw_loss_distribution(losses_with_ctrls, 'Fig-2.png')

print("Average loss: {:,.2f} EUR with no controls in place".format(loss_average(losses_no_ctrls)))
print("Average loss: {:,.2f} EUR with controls in place".format(loss_average(losses_with_ctrls)))

# draw loss esceedance curve without security controls in place
draw_loss_exceedance(loss_exceedance_curve(losses_no_ctrls, STEP), risk_tolerance, "Fig-3.png")

# draw loss esceedance curve with security controls in place
draw_loss_exceedance(loss_exceedance_curve(losses_with_ctrls, STEP), risk_tolerance, "Fig-4.png")
