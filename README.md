# VivoLift

VivoLift est une app conçue pour croiser les données physiologiques de récupération (issues d'une montre Garmin Vivoactive) avec la planification de séances de musculation. 

L'objectif est d'ajuster l'intensité de l'entraînement en fonction de l'état de fatigue réel du système nerveux.

## Fonctionnalités (Version 1.0)

* Saisie des métriques physiologiques quotidiennes (Score de sommeil, Niveau de stress, Body Battery).
* Sélection du groupe musculaire ciblé pour la séance du jour.
* Calcul d'un score de récupération interne.
* Recommandation d'intensité basée sur l'état de forme (repos, séance modérée, ou intensité maximale).

## Prérequis

* Python 3.x installé sur la machine.
* Windows (PowerShell) utilisé pour les commandes ci-dessous.

## Installation

1. Cloner ou télécharger ce dépôt.
2. Ouvrir un terminal PowerShell dans le dossier du projet.
3. Créer un environnement virtuel pour isoler les dépendances :
   ```powershell
   python -m venv env