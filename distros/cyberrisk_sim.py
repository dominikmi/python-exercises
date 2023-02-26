import matplotlib.pyplot as plt
import numpy as np

# Prosta symulacja zdarzenia cyberbezpieczeństwa, o oszacowanym P;
# Jeśli atak by się powiódł, oszacowano wystąpienie straty w przedziale X, Y z poziomem
# ufności 90% (tzn, jest 5% P, ze straty wyjdą poza przedział).
# Zastosowano tutaj rozkład log-normalny, który istotnie pasuje do rozkładu
# incydentów bezpieczeństwa, gdzie te najbardziej prawdopodobne (i najczęstsze)
# przynoszą mniejsze straty, niz te rzadsze.

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
    sim_lst = []
    for i in range(no_of_simulations):
        if (threat_event_comp_by_sec(te_prob,ctrl_reduct)) > 0:
            threat_loss = threat_event_loss(lower_bnd, upper_bnd)
            sim_lst.append("{:.2f}".format(threat_loss))
        else:
            threat_loss = 0
            sim_lst.append(threat_loss)    
    return sim_lst

def loss_average(sim_lst):
    x = 0
    accu = 0
    losses = list(map(float, sim_lst))
    for loss in losses:
        if loss > 0:
            accu += loss
            x += 1
    loss_ave = round(accu/x, 2)
    return loss_ave

def draw_loss_distribution(sim_lst):
    x = 0
    losses = list(map(float, sim_lst))
    fig, ax = plt.subplots()
    for loss in losses:
        ax.plot(x, loss,  **{'color': 'blue', 'marker': '.'})
        x += 1
    ax.set_xlabel('No. of tests')
    ax.set_ylabel('Loss magnitude')
    ax.set_title('Loss distribution')
    fig.savefig('fig1.png')

def loss_exceedance_curve(sim_lst, TE_UB, STEP):
    loss_ex_lst = []
    losses = list(map(float, sim_lst))
    losses_count = 0
    for loss in losses:
        if loss > 0: losses_count += 1
    for x in range(0,TE_UB,STEP):
        accu = 0
        for loss in losses:
            if loss > 0 and loss > x: 
                accu += 1
        loss_ex_lst.append([x,round(accu/losses_count,2)*100])
    return loss_ex_lst

def draw_loss_exceedance(lst, lst_for_risk_tolerance):
    fig, ax = plt.subplots()
    for x, perc in lst:
        ax.plot(x, perc, **{'color': 'green', 'marker': '.'})
    for x, perc in lst_for_risk_tolerance:
        ax.plot(x, perc, **{'color': 'red', 'marker': '.'})
    ax.set_xlabel('Loss magnitude')
    ax.set_ylabel('P(loss exceeded)')
    ax.set_title('Loss exceedance curve')
    fig.savefig('fig2.png')

#######################################################################
# Przykład:
# Wystąpienie zdarzenia - P(TE) = 10%
# dolna granica oczekiwanej straty - LOSS(TE) -> LB = 100 000 PLN
# górna granica oczekiwanej straty - LOSS(TE) -> UB = 1 000 000 PLN
#
# Istniejące środki bezpieczeństwa:
# -> redukcja wystąpienia P(TE) o 70%
#
# Liczba symulacji: 1000
#
# Zakładana tolerancja na strate w następstwie incydentow bezp w ciagu roku:
#   100 000 PLN - 90%
#   250 000 PLN - 50%
#   500 000 PLN - 20%
#   750 000 PLN -  5%
#  1000 000 PLN -  1%
########################################################################

TE = 0.1
TE_LB = 100000
TE_UB = 1000000
STEP = 25000
SEC_CTRL_RED = 0.7
NO_SIMULATIONS = 1000
RISK_TOLERANCE = [[100000,90], [250000,50], [500000,20],[750000,5],[1000000,1]]

# run:

sim_lst = loss_distribution(TE, SEC_CTRL_RED, NO_SIMULATIONS, TE_LB, TE_UB)
draw_loss_distribution(sim_lst)
print("Average loss: {:,.2f} PLN".format(loss_average(sim_lst)))
draw_loss_exceedance(loss_exceedance_curve(sim_lst, TE_UB, STEP), RISK_TOLERANCE)
