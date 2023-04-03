### Cyberattack simulation

Simulating cybersec events resulting in assessed losses.

#### Input parametrization:

* `P(TE)` - probability of an event (assumed: post some calibration) like 10% during 12 months.
* Loss intervals with CI at 90%, np. [100k, 1mln] EUR.
* Security controls efficiency, i.e.: downplaying the P(TE) by 50%
* Presumed risk tolerance with given P distribution.
* Number of simulations (Monte Carlo) i.e. 10000
* Used P distribution for the events: lognorma.

this all results in:

* Plot for 10000 tests
  [fig.1](https://github.com/dominikmi/python-exercises/blob/main/distros/fig1.png)
* PMF distribution for losses with assumed risk tolerance (in red): 
  [fig.2](https://github.com/dominikmi/python-exercises/blob/main/distros/fig2.png)
* Average expected Loss (np. 407,243.14 EUR)
* From the second plot [fig.2](https://github.com/dominikmi/python-exercises/blob/main/distros/fig2.png) we get P(AEL) - ~35%
* **Outcome 1**: Despite existing security controls, their efficiency does not play well against simulated losses, which go beyond assumed risk tolerance.
* **Outcome 2**: If we carry out a simulation limiting upper bound of loss interval by half, then we'd see that existing security controls would get us in the limits of assumed risk tolerance for events with losses of 200 000 EUR+ ([fig.3](https://github.com/dominikmi/python-exercises/blob/main/distros/fig3.png))
