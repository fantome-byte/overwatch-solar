# overwatch-solar
Overwatcch - Solar est un projet académique de programmation orientée objet en Python. Il s'agit d'un prototype de supervision et de maintenance d'une centrale photovoltaïque, capable de modéliser des équipements, de simuler des mesures et de générer des tickets de maintenance.

Le projet est organisé en modules distincts :

- `models/` contient les classes métier qui définissent les équipements (onduleurs, capteurs, chaînes de panneaux, centrale) et leur comportement.
- `manager/` contient le gestionnaire de maintenance qui pilote la simulation, récupère les alertes et crée des tickets.
- `api.py` charge la configuration depuis `data/config.json`, initialise la centrale, exécute la simulation et gère la persistance des tickets.
- `data/` contient la configuration de la centrale et le stockage des tickets.
- `test_backend.py` est un script de démonstration qui montre l'initialisation, l'exécution de la simulation et la gestion des tickets.

Ce projet illustre plusieurs concepts de la POO : héritage, abstraction, encapsulation et modularité. Il est conçu pour être extensible et servir de base à une application plus complète de supervision d'une installation solaire.
