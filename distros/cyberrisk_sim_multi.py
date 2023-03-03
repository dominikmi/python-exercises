###################################################################################
# Based on "How to measure anything in Cybersecurity" by D. Hubbard and R. Seiersen
# 
# Example:
# A list of security events with adverse consequences with P(TE) = in %
# and 90% of confidence interval:
# lower bound of the interval - LOWER_LOSS(TE)
# upper bound of the interval - UPPER_LOSS(TE)
#
# Existing or planned security controls compensating P(TE) in %
# 
# Number of simulations: i.e. 10000
#
# Presumed risk tolerance with the following distribution:
#    100 000 EUR - 90%
#    250 000 EUR - 50%
#    500 000 EUR - 30%
#    750 000 EUR - 15%
#  1 000 000 EUR -  2%
# 10 000 000 EUR -  0.2%
####################################################################################

# list of security events [probability, lower bound loss, upper bound loss, description]
events = {
    "event1": (0.21, 100000, 550000, "Successful DDoS on the cloud base core app"),
    "event2": (0.08, 500000, 1500000, "Sensitive data exfiltration"),
    "event3": (0.15, 200000, 1000000, "Malicious code injected into production pipeline"),
    "event4": (0.38, 10000, 100000, "Laptop with sensitive data lost/stolen"),
    "event5": (0.17, 15000, 50000, "Malicious code in 3rd party dependencies"),
    "event6": (0.15, 1000, 150000, "Broken backups"),
    "event7": (0.04, 1000000, 12000000, "Malware attack, knocked out internal network"),
    "event8": (0.05, 10000, 500000, "Insider's threat"),
    "event9": (0.03, 1000000, 11500000, "Terrorist attack"),
    "event10": (0.25, 5000, 50000, "Broken app release")
}

# list of mitigating security controls [annual cost, with impact on event probability reduction]
sec_controls = {
    "event1": (70000, 0.65),
    "event2": (200000, 0.55),
    "event3": (77000, 0.7),
    "event4": (30000, 0.37),
    "event5": (25000, 0.42),
    "event6": (100000, 0.62),
    "event7": (230000, 0.85),
    "event8": (121000, 0.47),
    "event9": (130000, 0.6),
    "event10": (25000, 0.45)
}

# defined risk tolerance
risk_tolerance = [
    (100000, 90), 
    (250000, 50), 
    (500000, 30), 
    (750000, 15), 
    (1000000, 2), 
    (10000000, 0.2)
]

# simulation parameters

STEP = 5000
NO_SIMULATIONS = 10000


### computing functions

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def threat_event_happened(event_p, reduct_p):
    """A threat event occurs if a random number
    falls below given probability"""
    return np.random.rand() < event_p*(1-reduct_p)

def threat_event_loss(lower_bnd, upper_bnd):
    """If threat event occured, let's get its loss it inflicts,
    given lower and upper bounds of 90% CI"""
    mean = (np.log(lower_bnd) + np.log(upper_bnd))/2
    std_deviation = (np.log(upper_bnd) - np.log(lower_bnd))/3.29
    return round(float(np.random.lognormal(mean, std_deviation)),2)

def loss_distribution(events_dict, no_of_simulations):
    """Using Monte Carlo (number of simulations) get
    a distribution of losses for the given list of estimated events"""
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
    """ If we want to see our security investments impact on given list of threat
    events, we need to run Monte Carlo again reducing original threat event by the 
    estimated impact in the given list of security controls"""
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
    """ This one is simple, I guess"""
    accu = 0
    for loss in lst:
        accu += loss
    loss_ave = round(accu/len(lst), 2)
    return loss_ave

def plot_loss_distribution(lst, fig_name):
    """Plot the distribution of losses for both variants -
    with and w/o security controls"""
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
    """ Compute a list of LEC to see how good we are in terms of
    probability and magnitude of losses"""
    loss_ex_lst = []
    for x in range(0,5000000,STEP):
        accu = 0
        for loss in lst:
            if loss > 0 and loss > x: 
                accu += 1
        loss_ex_lst.append([x,round(accu/len(lst),2)*100])
    return loss_ex_lst

def plot_loss_exceedance(lst, lst_for_risk_tolerance, fig_name):
    """ Plot the LEC"""
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

def total_sec_investments(sec_controls):
    """ Give the total sum of all security investments and 
    in this respect compare both LECs """
    controls_keys = sec_controls.keys()
    total_sum = 0
    for each_key in controls_keys:
        total_sum += sec_controls[each_key][0]
    return total_sum

# run

losses_no_ctrls = loss_distribution(events, NO_SIMULATIONS)
losses_with_ctrls = loss_distribution_reduced(events, sec_controls, NO_SIMULATIONS)

# plot loss distribution without security controls in place
plot_loss_distribution(losses_no_ctrls, 'Fig-1.png')

# plot loss distribution with security controls in place
plot_loss_distribution(losses_with_ctrls, 'Fig-2.png')

print("Average loss: {:,.2f} EUR with no controls in place".format(loss_average(losses_no_ctrls)))
print("Average loss: {:,.2f} EUR with controls in place".format(loss_average(losses_with_ctrls)))
print("Total security investments: {:,.2f} EUR: ".format(total_sec_investments(sec_controls)))

# plot loss exceedance curve without security controls in place
plot_loss_exceedance(loss_exceedance_curve(losses_no_ctrls, STEP), risk_tolerance, "Fig-3.png")

# plot loss exceedance curve with security controls in place
plot_loss_exceedance(loss_exceedance_curve(losses_with_ctrls, STEP), risk_tolerance, "Fig-4.png")
