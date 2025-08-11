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
- git clone https://github.com/IlyasHassen/StressSentry_Telegram.git
- cd votre-projet

2. **Installer les dépendances :**
- pip install -r requirements.txt

3. **Configurer vos clés API dans `.env` :**
- TELEGRAM_TOKEN=VotreTokenTelegram
- OURA_TOKEN=VotreTokenOura
- COHERE_API_KEY=VotreCleCohere

4. **Lancer le bot :**
- python app.py


---

## Usage

**Commandes Telegram disponibles :**
- `/start` : Affiche la liste des commandes avec descriptions.  
- `/journal` : Voir tous vos ressentis enregistrés.  
- `/agenda` : Ajouter un événement à votre agenda.  
- `/exam` : Ajouter un examen à votre planning.  
- `/ressenti` : Saisir un ressenti et recevoir des recommandations.  
- `/oura_ring_4j` : Consulter les données sommeil (4 derniers jours).  
- `/recherche <mot>` : Recherche un mot dans vos ressentis.  
- `/organisation` : Affiche votre agenda et vos examens.  
- `/delete` : Supprime toutes vos données personnelles.

---

## Structure du code

- `userdata.py` : Gestion et chiffrement du stockage local.  
- `oura_client.py` : Classe pour interroger l’API Oura Cloud.  
- `cohere_client.py` : Classe pour interagir avec Cohere Chat.  
- `bot_handlers.py` : Logique métier et gestion des commandes Telegram.  
- `app.py` : Point d’entrée, assemble les modules et lance le bot.

---

## Sécurité et confidentialité

- Données stockées localement avec chiffrement Fernet.  
- Clés API sécurisées via fichier `.env`.  
- Suppression des données à la demande via `/delete`.

---

## Perspectives et améliorations

- Visualisations statistiques des données.  
- Extension multi-plateforme (Slack, WhatsApp).  
- Analyse prédictive et alertes automatiques.  
- Intégration avec SI universitaires.

---

## Contribution

Utilisez les issues et pull requests pour vos propositions d’amélioration ou pour rapporter un problème.




