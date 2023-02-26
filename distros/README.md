### Cyberattack simulation

Symulacja zdarzenia cyberbezpieczeństwa, w następstwie którego wystąpiła strata.

#### Parametry wejściowe:

* `P(TE)` - prawdopodobieństwo wystąpienia zdarzenia (po kalibracji, równaniu Bayesa itd.) np. 10% w ciagu roku.
* Zakres strat z poziomem ufności 90%, np. [100k, 1mln] PLN.
* Skutecznośc zabezpieczeń w wymiarze obnizenia P(TE) - np. 50%
* Załozona tolerancja na ryzyko z zadanym rozkładem.
* Liczba symulacji (Monte Carlo) np. 10000

W wyniku otrzymujemy:

* Wykres wystąpień strat dla 10000 prób
  [fig.1](https://github.com/dominikmi/python-exercises/blob/main/distros/fig1.png)
* Rozkład gęstości prawdopodobieństwa dla wysokości strat, wraz z załozoną tolerancją na ryzyko (na czerwono)
  [fig.2](https://github.com/dominikmi/python-exercises/blob/main/distros/fig2.png)