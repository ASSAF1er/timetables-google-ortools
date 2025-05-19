# Générateur d'emplois du temps — Université de Yaoundé I

Ce projet implémente un système de génération automatique d’emplois du temps hebdomadaires pour les classes du département d'informatique de l’Université de Yaoundé I, en utilisant Google OR-Tools (solveur CP-SAT).

## Contenu du projet

- `timetables.py` : script Python principal contenant l'implémentation du solveur CP-SAT.
- `subjects.json` : liste des cours, enseignants, niveaux et semestres.
- `rooms.json` : liste des salles disponibles pour la planification.
- `rapport.pdf` : rapport LaTeX du projet, avec modélisation mathématique.
- `README.md` : documentation du projet.

## Installation

1. Installer les dépendances nécessaires :

```bash
pip install ortools
```

## Exécution

Assurez-vous que les fichiers `subjects.json` et `rooms.json` sont présents dans le même répertoire que `timetables.py`, puis exécutez :

```bash
python3 timetables.py
```

Le script affiche en console une solution d’emploi du temps possible.

## Fonctionnalités

- Chaque cours est affecté une seule fois par semaine.
- Une classe ne suit jamais deux cours en même temps.
- Deux cours ne peuvent pas se dérouler dans la même salle au même moment.
- Les cours sont planifiés préférentiellement en matinée grâce à une fonction objectif pondérée.

## Modèle mathématique (résumé)

### Ensembles

- `C` : classes
- `S` : matières
- `T` : enseignants
- `R` : salles
- `D` : jours (Lundi à Samedi)
- `P` : périodes (P1 à P5)

### Paramètres

- `w_p` : poids associé à chaque période (plus élevé pour les périodes du matin)
- `S_c ⊆ S` : matières de la classe `c`
- `L_s` : enseignant responsable de la matière `s`

### Variable de décision

x_{s,r,d,p}^c = 1 si la classe c suit la matière s avec l'enseignant L_s
dans la salle r au jour d et à la période p, 0 sinon.

### Contraintes

1. Chaque cours est donné une seule fois par semaine.
2. Une classe ne suit jamais deux cours en même temps.
3. Une salle ne peut accueillir qu’un seul cours à la fois.
4. Une classe ne peut recevoir qu’un cours appartenant à son programme.

### Objectif

Maximiser :
∑_{c,s,r,d,p} w_p ⋅ x_{s,r,d,p}^c

## Rapport LaTeX

Le fichier `rapport.pdf` contient :

- La formulation complète du problème (ensembles, paramètres, variables, contraintes)
- Le lien avec le code Python
- Une section résultat



## Auteur
ASSONFACK YEMENE BERAL 21T2501

Département d’Informatique  
Université de Yaoundé I  
Avril 2025