import matplotlib.pyplot as plt
import numpy as np

# Simple simulation of a cyberthreat event against IT (cyberattack)
# Attack is successfull/failed given prior estimated probability
# If the attack is successful it may cause harm - in $$$
# With 90% confidence we can estimate interval of the loss, and
# Lognormal distribution which largely fits the distribution of security
# incidents where there's far greater number of events with small losess, than
# those which inflict catastrophic losses.

def threat_event_happened(event_probability):
    return np.random.rand() < event_probability

def threat_event_loss(lower_bnd, upper_bnd):
    mean = (np.log(lower_bnd) + np.log(upper_bnd))/2.0
    std_deviation = (np.log(upper_bnd) - np.log(lower_bnd))/3.29
    return float(np.random.lognormal(mean, std_deviation))

def threat_event_comp_by_sec(event_probability, ctrl_reduct):
    reduced = threat_event_happened(
        event_probability)*(1-ctrl_reduct)
    return reduced

def loss_distribution(te_prob, ctrl_reduct, no_of_simulations, lower_bnd, upper_bnd):
    i = 0
    accum = 0
    sim_lst = []
    for i in range(no_of_simulations):
        if (threat_event_comp_by_sec(te_prob,ctrl_reduct)) > 0:
            threat_loss = threat_event_loss(lower_bnd, upper_bnd)
            sim_lst.append("{:.2f}".format(threat_loss))
            accum += threat_loss
        else:
            threat_loss = 0
            sim_lst.append(threat_loss)    
    loss_average = accum/i
    return sim_lst, loss_average

def draw_loss_distribution(sim_lst):
    x = 0
    losses = list(map(float, sim_lst))
    fig, ax = plt.subplots()
    for loss in losses:
        ax.stem(x, loss)
        x += 1
    ax.set_xlabel('No. of tests')
    ax.set_ylabel('Loss magnitude')
    ax.legend()
    plt.savefig('fig1.png')

###################################
# Example:
# P(TE) = 20%
# LOSS(TE) -> LB = 50 000 PLN
# LOSS(TE) -> UB = 150 000 PLN
#
# Security Control in place
# -> reduction P(TE) by 70%
#
# Number of simulations: 1000
###################################

TE = 0.2
TE_LB = 50000
TE_UB = 150000
SEC_CTRL_RED = 0.7
NO_SIMULATIONS = 1000

# run:

sim_lst, loss_ave = loss_distribution(TE, SEC_CTRL_RED, NO_SIMULATIONS, TE_LB, TE_UB)
draw_loss_distribution(sim_lst)
print("Average loss: {:,.2f} PLN".format(loss_ave))
# draw_loss_exceedance_curve(sim_lst)
