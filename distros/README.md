### Cyberattack simulation

Symulacja zdarzenia cyberbezpieczeństwa, w następstwie którego wystąpiła strata.

#### Parametry wejściowe:

* `P(TE)` - prawdopodobieństwo wystąpienia zdarzenia (po kalibracji, równaniu Bayesa itd.) np. 10% w ciagu roku.
* Zakres strat z poziomem ufności 90%, np. [100k, 1mln] PLN.
* Skutecznośc zabezpieczeń w wymiarze obnizenia P(TE) - np. 50%
* Załozona tolerancja na ryzyko z zadanym rozkładem.
* Liczba symulacji (Monte Carlo) np. 10000
* Rozkład P dla wystąpienia zdarzenia: log-normalny.

W wyniku otrzymujemy:

* Wykres wystąpień strat dla 10000 prób
  [fig.1](https://github.com/dominikmi/python-exercises/blob/main/distros/fig1.png)
* Rozkład gęstości prawdopodobieństwa dla wysokości strat, wraz z załozoną tolerancją na ryzyko (na czerwono)
  [fig.2](https://github.com/dominikmi/python-exercises/blob/main/distros/fig2.png)
* Średnia wysokośc straty (Average Loss) (np. 407,243.14 PLN)
* Z wykresu na [fig.2](https://github.com/dominikmi/python-exercises/blob/main/distros/fig2.png) odczytujemy P(AL) - ok. 35%
* **Wniosek**: Pomimo istniejących zabezpieczeń, ich skutecznośc w wyniku tego danego ataku nie przeciwdziała stratom, których wysokośc przekracza tolerancję na ryzyko.
* **Wniosek 2**: Jeśli wykonamy symulację o tych samych parametrach, zmieniając jedynie zakres strat (do 500 000 PLN zamiast 1000000), to okaze się, ze istniejące zabezpieczenia 
  powodują, ze P strat powyzej ok. 200 000 mieszczą się w zadanej tolerancji na ryzyko. ([fig.3](https://github.com/dominikmi/python-exercises/blob/main/distros/fig3.png))