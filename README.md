# StressSentry 
# Bot Telegram de réduction du stress académique

Ce projet est un **bot Telegram** conçu pour accompagner les étudiants dans la gestion de leur stress académique.  
Il collecte les ressentis utilisateurs, organise leur agenda, suit leurs données biométriques via l’API Oura, et génère des recommandations personnalisées grâce à l’API Cohere Chat.

---

## Fonctionnalités principales

- Enregistrement des ressentis quotidiens via commandes simples.  
- Suivi du sommeil, readiness, activité sur 4 derniers jours via intégration Oura Cloud.  
- Organisation d’agenda et gestion des examens.  
- Recommandations personnalisées basées sur les données et les ressentis.  
- Recherche évoluée dans les ressentis.  
- Protection et chiffrement local des données utilisateurs.  
- Commande de suppression totale des données personnelles.

---

## Architecture du projet

- **Bot Telegram** : Interface utilisateur accessible sur mobile et desktop.  
- **API Oura Cloud v2** : Récupération des données biométriques.  
- **API Cohere Chat v2** : Génération des recommandations personnalisées.  
- **Stockage local sécurisé** : Données chiffrées avec Fernet.  
- **Modules Python** organisés en classes pour gestion des données, API, logique bot.

---

## Installation

### Prérequis

- Python 3.8+  
- Clés API valides pour :
  - Telegram Bot (`TELEGRAM_TOKEN`)
  - Oura Cloud (`OURA_TOKEN`)
  - Cohere Chat (`COHERE_API_KEY`)

### Instructions 
1. **Cloner le repository :**
git clone https://github.com/IlyasHassen/StressSentry_Telegram.git
cd votre-projet


2. **Installer les dépendances :**
