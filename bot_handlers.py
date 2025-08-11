# Import des outils nécessaires
from datetime import datetime  # Pour dater les ressentis enregistrés
from telegram.ext import ContextTypes, ConversationHandler
# ContextTypes : type de contexte pour les méthodes async des handlers Telegram
# ConversationHandler : gère les commandes multi-étapes avec des états

# Définition des identifiants d'états pour les conversations
AGENDA, EXAM, RESSENTI = range(3)
# Cela crée : AGENDA = 0, EXAM = 1, RESSENTI = 2
# Chaque état correspond à l’attente d’une réponse utilisateur différente

class BotHandlers:
    """
    Cette classe regroupe toutes les méthodes déclenchées par les commandes Telegram.
    Elle reçoit les gestionnaires de données et d'API en paramètres, 
    pour les utiliser dans les commandes.
    """

    def __init__(self, dm, oura, cohere_client):
        """
        Constructeur.
        - dm : instance de UserDataManager (gestion des données locale chiffrées)
        - oura : instance de OuraClient (requêtes à l'API Oura)
        - cohere_client : instance de CohereClient (génération de texte AI)
        """
        self.dm = dm
        self.oura = oura
        self.cohere = cohere_client

    # ---------------------- COMMANDE /start ----------------------
    async def start(self, update, context: ContextTypes.DEFAULT_TYPE):
        """
        Affiche la liste des commandes disponibles avec leur explication.
        """
        texte = (
            "/journal\n"
            "Affiche la liste de tous vos ressentis enregistrés dans le journal, avec la date et le texte.\n\n"

            "/agenda\n"
            "Ajoute un événement (DD-MM-YYYY : description).\n\n"

            "/exam\n"
            "Ajoute un examen (DD-MM-YYYY : examen)\n\n"

            "/ressenti\n"
            "Saisis ton ressenti actuel, tu recevras une recommandation\n\n"

            "/oura_ring_4j\n"
            "Affiche les données de sommeil des 4 derniers jours issues de votre compte Oura.\n\n"

            "/recherche <mot>\n"
            "Recherche un mot dans tous vos ressentis et affiche les entrées correspondantes.\n\n"

            "/organisation\n"
            "Affiche un résumé de votre agenda et de vos examens enregistrés.\n\n"

            "/delete\n"
            "Supprime toutes vos données personnelles enregistrées dans le bot."
        )
        await update.message.reply_text(texte)

    # ---------------------- COMMANDE /journal ----------------------
    async def journal(self, update, context):
        """
        Liste tous les ressentis de l'utilisateur, s'ils existent.
        """
        uid = str(update.message.from_user.id)  # ID Telegram de l'utilisateur
        entries = self.dm.get_user(uid)['journal']  # Récupère la liste "journal"
        if not entries:
            await update.message.reply_text("Aucun ressenti.")
            return
        # Construction du message : chaque ligne = date : texte
        msg = "\n".join(f"{e['date']}: {e['text']}" for e in entries)
        await update.message.reply_text(msg)

    # ---------------------- COMMANDE /agenda ----------------------
    async def agenda_start(self, update, context):
        """
        Première étape /agenda : demande la saisie d'un événement.
        """
        await update.message.reply_text("Entrez événement: DD-MM-YYYY : description")
        return AGENDA  # Passe l'état de conversation à AGENDA

    async def agenda_save(self, update, context):
        """
        Deuxième étape /agenda : enregistre l'événement saisi.
        """
        self.dm.add_agenda_event(str(update.message.from_user.id), update.message.text)
        await update.message.reply_text("Événement ajouté.")
        return ConversationHandler.END  # Termine la conversation

    # ---------------------- COMMANDE /exam ----------------------
    async def exam_start(self, update, context):
        """Démarre la conversation /exam."""
        await update.message.reply_text("Entrez examen: DD-MM-YYYY : examen")
        return EXAM

    async def exam_save(self, update, context):
        """Enregistre le texte saisi comme examen."""
        self.dm.add_exam(str(update.message.from_user.id), update.message.text)
        await update.message.reply_text("Examen ajouté.")
        return ConversationHandler.END

    # ---------------------- COMMANDE /ressenti ----------------------
    async def ressenti_start(self, update, context):
        """
        Première étape /ressenti : demande à l’utilisateur d’exprimer son ressenti texte.
        """
        await update.message.reply_text("Exprimez votre ressenti :")
        return RESSENTI

    async def ressenti_save(self, update, context):
        """
        Enregistre le ressenti, récupère données Oura récentes,
        envoie le tout à Cohere pour générer une recommandation.
        """
        uid = str(update.message.from_user.id)
        texte = update.message.text
        # Sauvegarde du ressenti (avec date du jour)
        self.dm.add_journal_entry(uid, texte, datetime.today().strftime("%Y-%m-%d"))

        # Récupération des données Oura du dernier jour (ou dictionnaire vide si pas dispo)
        sleep = self.oura.fetch_sleep_data_last_days(1)[0] if self.oura.fetch_sleep_data_last_days(1) else {}
        readiness = self.oura.fetch_readiness_data_last_days(1)[0] if self.oura.fetch_readiness_data_last_days(1) else {}
        activity = self.oura.fetch_activity_data_last_days(1)[0] if self.oura.fetch_activity_data_last_days(1) else {}

        # Appel Cohere pour générer recommandations
        reco = self.cohere.generate_recommendations(texte, sleep, readiness, activity)

        await update.message.reply_text(f"Ressenti enregistré.\n\n{reco}")
        return ConversationHandler.END

    # ---------------------- COMMANDE /oura_ring_4j ----------------------
    async def oura_ring_4j(self, update, context):
        """
        Affiche les données de sommeil détaillées des 4 derniers jours depuis Oura.
        """
        data = self.oura.fetch_sleep_data_last_days(4)
        if not data:
            await update.message.reply_text("Pas de données Oura.")
            return

        lignes = ["📊 Données - 4 derniers jours :"]
        for jour in data:
            # Conversion secondes → heures pour l'affichage
            total_h = jour.get("total_sleep_duration", 0) / 3600
            deep_h = jour.get("deep_sleep_duration", 0) / 3600
            rem_h = jour.get("rem_sleep_duration", 0) / 3600
            light_h = jour.get("light_sleep_duration", 0) / 3600

            lignes.append(
                f"📅 {jour.get('day', jour.get('summary_date', '?'))}\n"
                f"   ⏱ Total: {total_h:.1f}h | Deep: {deep_h:.1f}h | REM: {rem_h:.1f}h | Light: {light_h:.1f}h\n"
                f"   ❤️ FC moy.: {jour.get('average_heart_rate', 'N/A')} bpm | HRV: {jour.get('average_hrv', 'N/A')} ms\n"
                f"   🌡 Temp. Δ: {jour.get('readiness', {}).get('temperature_deviation', 'N/A')}"
            )

        # chaque bloc avec deux sauts de ligne pour l'affichage
        await update.message.reply_text("\n\n".join(lignes))

    # ---------------------- COMMANDE /recherche ----------------------
    async def recherche(self, update, context):
        """
        Recherche un mot clé dans tous les ressentis de l'utilisateur.
        """
        uid = str(update.message.from_user.id)
        if not context.args:
            await update.message.reply_text("Usage: /recherche mot")
            return
        mot = context.args[0].lower()
        res = [e for e in self.dm.get_user(uid)['journal'] if mot in e['text'].lower()]
        await update.message.reply_text(
            "\n".join(f"{e['date']}: {e['text']}" for e in res) or "Aucun résultat."
        )

    # ---------------------- COMMANDE /organisation ----------------------
    async def organisation(self, update, context):
        """
        Affiche l'agenda et les examens enregistrés pour l'utilisateur.
        """
        u = self.dm.get_user(str(update.message.from_user.id))
        msg = "Agenda:\n" + "\n".join(u['agenda']) + "\nExamens:\n" + "\n".join(u['exams'])
        await update.message.reply_text(msg or "Vide.")

    # ---------------------- COMMANDE /delete ----------------------
    async def delete(self, update, context):
        """
        Efface toutes les données personnelles enregistrées pour cet utilisateur.
        """
        self.dm.clear_user(str(update.message.from_user.id))
        await update.message.reply_text("Toutes vos données ont été supprimées.")
