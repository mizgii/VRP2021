# VRP2021
programowanie zespołowe || projekt grupy VRP 

autorki:

Diana Glebowicz

Karolina Robinson

Zofia Mizgalewicz

Raport z projektu:

https://drive.google.com/file/d/1P_qFN5DdC07XrBsPtluoXBVFrc6j_DUT/view



  Przedmiotem niniejszego projektu było znalezienie i zastosowanie narzędzi optymalizacyjnych przy szeroko rozumianym problemie VRP (ang. Vehicle Routing Problem) oraz stworzenie aplikacji webowej do wizualizacji uzyskanych wyników.


  VRP, po polsku znany jako problem marszrutyzacji, jest problemem decyzyjnym, którego celem jest znalezienie optymalnych tras przewozowych dla ściśle określonej liczby pojazdów, mających obsłużyć dany zbiór lokalizacji. Problem VRP jest zwykle uzupełniony o dodatkowe założenia, takie jak przedziały czasowe, ładowność pojazdów, ograniczenie zasobów ludzkich bądź przestrzennych oraz kary za opuszczenie dostawy.  
  
  Problemy z wyznaczaniem tras są z natury trudne do rozwiązania: czas potrzebny na ich rozwiązanie rośnie wykładniczo wraz z rozmiarem problemu. Popularne narzędzia używane do pracy nad zagadnieniem VRP często pozwalają ograniczyć czas działania programu kosztem otrzymania wyników dobrych, a nie optymalnych. Szansą na przyspieszenie działania podobnych algorytmów optymalizacyjnych jest wykorzystanie obliczeń kwantowych, takich jak quantum annealing – heurystyczna metoda znajdowania minimum funkcji celu (ang. objective function), spośród skończonej liczby proponowanych rozwiązań o równych wagach, z użyciem fluktuacji kwantowych.	
  
  W przypadku rozpatrywanych przez zespół problemów jako kryterium optymalizacji przyjęto koszt podróży wyrażony odległościowo – celem działania gotowego programu było, w każdym wypadku, znalezienie najkrótszej trasy dla pojazdów. Skupiono się głównie na problemie Pickup and Delivery, w którym pojazdy odbierają zadaną ilość towaru z jednej lokalizacji i dostarczają go do innej. Jako dodatkowe założenia przyjęto ograniczoną ładowność samochodów (ang. capacity constraints) oraz rozpoczęto pracę nad dodaniem ograniczeń czasowych (ang. time window constraints). Algorytmy testowano na zbiorze przypadkowych punktów, jednak rozpoczęto prace nad przełożeniem ich na wariant rzeczywisty – oparty na danych pochodzących z Open Street Map, zapisywanej skrótowo OSM. Wszystkie kody przedstawione w niniejszym repozytorium napisano w języku Python.

Licencje:

© autorzy OpenStreetMap, wszystkie materiały udostępnione na bazie licencji Open Database License: https://www.openstreetmap.org/copyright

OR-Tools 7.2. Laurent Perron and Vincent Furnon, oprogramowanie udostępnione na bazie licencji Apache Licence 2.0: https://developers.google.com/optimization/

© Copyright 2010 Pallets, wszystkie narzędzia i dokumentacja udostępnione na bazie licencji BSD-3-Clause Source License: 
https://flask.palletsprojects.com/en/2.0.x/license/


