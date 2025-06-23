# **É**quipe

- Martin Iwen
- Baud Quentin
- Cuvillon Arthur

# Présentation projet

Ce projet est une application web sociale permettant de créer et de suivre des soirées entre amis. Chaque utilisateur peut organiser une soirée, inviter ses amis, et chacun peut enregistrer les verres qu’il consomme en temps réel. L’application calcule automatiquement le taux d’alcoolémie de chaque participant pendant la soirée. Chaque utilisateur peut voir ses statistiques: nombre total de soirées, nombre total de verres consommés, et un classement des boissons les plus consommées. L’objectif est de permettre un suivi ludique, informatif et communautaire.

# MCD

![MCD.png](static/images/MCD.png)

# Découpage des routes

- / : Accueil, présentation rapide et accès aux soirées en cours ou passées.
- /login : Connexion utilisateur.
- /register : Inscription utilisateur.
- /logout : Déconnexion.
- /party/create : Création d'une nouvelle soirée.
- /party/<id> : Détails de la soirée (participants, verres consommés, taux d'alcoolémie en temps réel).
- /party/<id>/invite : Invitation d'amis à une soirée.
- /party/<id>/add_drink : Ajout d'un verre consommé par un participant.
- /party/<id>/stats : Statistiques de la soirée (verres, taux, classement).
- /profile/<id> : Profil utilisateur (historique des soirées, statistiques personnelles).
- /stats/global : Statistiques globales (nombre de soirées, verres, top 3 des boissons).
- /drinks/top : Classement des boissons les plus consommées.

# Makefile
    
L’utilisation d’un Makefile permet de simplifier et d’automatiser les tâches courantes du projet. Grâce à des commandes courtes, il évite d’avoir à retenir ou répéter des instructions complexes pour installer les dépendances, configurer l’environnement ou lancer l’application. Cela garantit aussi que tous les membres de l’équipe utilisent les mêmes procédures, réduisant les risques d’erreurs de configuration.

## Commandes Makefile
```bash
make  init
```
- Crée un environnement virtuel Python (venv)
- Met à jour pip
- Installe les dépendances listées dans requirements.txt
- Copie le fichier .env.example en .env si besoin

```bash
make start
```
- Crée l’environnement virtuel si nécessaire
- Installe les dépendances si besoin
- Lance le serveur Flask (server.py)

```bash
make clean
```
- Supprime l’environnement virtuel, les fichiers compilés et temporaires pour repartir sur une base propre.
