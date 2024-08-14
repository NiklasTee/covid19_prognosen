# COVID-19: Prognosen auf kommunaler Ebene

Dieses studentische Projekt ist im Rahmen des Kurses ‚Projekt Data Science‘ im Sommersemester 2021 am Fachbereich Informatik und Sprachen an der HS Anhalt entstanden.

Ziel war es, ein Modell zur Vorhersage von COVID-19 Erkrankungen auf kommunaler Ebene in Deutschland zu entwickeln. Mit solchen Prognosen ließe sich die Effektivität dezentraler Eindämmungsmaßnahmen erheblich verbessern. Quarantäneanordnungen müssten nicht pauschal auf die gesamte Bundesrepublik angewendet werden, sondern könnten besser an das regionale Pandemiegeschehen angepasst werden.

Zur Modellierung wurden diverse Modelle der statistischen Zeitreihenanalyse und des maschinellen Lernens getestet. Grundlage für die Vorhersage war die Anzahl gemeldeter Neuinfektionen, täglich publiziert durch das Robert Koch-Institut. Ergänzend wurden die demographischen und sozioökonomischen Besonderheiten der 401 Kreise in Deutschland berücksichtigt. Ein Rekurrentes Neuronales Netz (RNN) mit Long short-term memory (LSTM) wurde für die Implementierung ausgewählt.


Die Ergebnisse sind als Webanwendung unter https://www.covid-prognosen.de/ veröffentlicht.




## Struktur des GitLab-Repository:

- **konzept**: Enthält das ausformulierte Projektkonzept, die Folien der Konzeptpräsentation sowie die wöchtentliche Dokumentation der Arbeitsteilung

- **land_clustering**: Enthält Code, Daten, Erläuterungen und Darstellung zum Clustering der Landkreise. 

- **rki_vorhersagen**:  Enthält Code, Daten, Erläuterungen und Darstellung zur Vorhersage der Fallzahlen.

- **webanwendung**:  Enthält Code, Daten, Erläuterungen und Darstellung zur Erstellung der Webanwendung.

## Datensätze

- [RKI COVID-19 Datenhub](https://npgeo-corona-npgeo-de.hub.arcgis.com/search?collection=Dataset)
- [Regionalatlas Destatis](https://regionalatlas.statistikportal.de/)

- [Impfdashboard BfG](https://impfdashboard.de/)
- [Bevölkerung nach Landkreisen Destatis](https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html)
- [Esri Kreisgrenzen](https://opendata-esri-de.opendata.arcgis.com/datasets/esri-de-content::kreisgrenzen-2019-mit-einwohnerzahl/explore?location=51.164254%2C10.454033%2C6.78&showTable=true)


## Anforderungen

- Python 3.8

**Verwendete Python-Libraries**

- geopandas
- json
- keras
- matplotlib
- numpy
- os
- pandas
- pickle
- scikit-learn
- seaborn
- statsmodels
- tensorflow
- umap
- xarray


## Verantwortlich

Niklas Tscheuschner
