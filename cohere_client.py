# Import des modules nécessaires
import os  # Gestion des variables d'environnement
from cohere import ClientV2  # Client officiel Cohere API v2 pour chat
from dotenv import load_dotenv  # Pour charger les variables dans un fichier .env

# Charge les variables d'environnement depuis le fichier .env (ex: COHERE_API_KEY)
load_dotenv()

class CohereClient:
    """
    Client Cohere Chat V2 pour générer des recommandations basées sur le ressenti
    et les données collectées depuis Oura Ring.
    """

    def __init__(self, api_key=None):
        """
        Initialise le client Cohere avec la clé API.
        - api_key: optionnel, si non fourni, sera pris depuis la variable d'environnement COHERE_API_KEY.
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")  # Récupère la clé API
        if not self.api_key:
            # Si la clé n'est pas trouvée, on lève une erreur explicite
            raise ValueError("COHERE_API_KEY manquant")
        # Instancie le client Cohere v2 avec la clé API
        self.co = ClientV2(api_key=self.api_key)

    def generate_recommendations(self, ressenti, sleep, readiness, activity):
        """
        Prépare un prompt enrichi avec le ressenti utilisateur + données Oura,
        puis envoie ce prompt à l'API Cohere Chat pour générer une recommandation.

        Params:
        - ressenti : chaîne de caractères, le texte saisi par l'utilisateur exprimant son ressenti
        - sleep : dict, données sommeil récentes extraites d'Oura (score, durée, etc.)
        - readiness : dict, données readiness (HRV, repos, score readiness)
        - activity : dict, données activité physique (score, pas, calories)

        Retour:
        - une chaîne avec la recommandation générée, ou "Erreur" en cas de problème.
        """

        # Construction du prompt textuel à envoyer en message user
        prompt = (
            f"Un étudiant exprime ce ressenti : \"{ressenti}\"\n\n"
            "Données Oura :\n"
            f"- Score sommeil : {sleep.get('score', 'N/A')}\n"
            f"- HRV : {readiness.get('hrv', 'N/A')}\n"
            f"- Readiness : {readiness.get('score', 'N/A')}\n"
            f"- Score activité : {activity.get('score', 'N/A')}\n"
            "En te basant sur ces infos, donne des recommandations pratiques "
            "sur : Organisation et gestion du temps, Activité physique régulière, "
            "Techniques de relaxation, Qualité du sommeil, Aménagement environnement, "
            "Pauses et micro-siestes."
        )

        try:
            # Appel à la méthode chat() du client Cohere v2
            # modèle utilisé : "command-r-plus-08-2024" (modèle de coaching)
            # messages : une liste de dictionnaires avec les rôles system et user
            response = self.co.chat(
                model="command-r-plus-08-2024",
                messages=[
                    # Message système pour fixer le contexte du bot
                    {"role": "system", "content": "Tu es un coach pour étudiants stressés."},
                    # Message utilisateur avec le prompt détaillé
                    {"role": "user", "content": prompt}
                ],
                max_tokens=160,      # Limite la taille de la réponse générée
                temperature=0.7,    # Contrôle la créativité / aléatoire du texte généré
            )
            # La réponse texte est contenue dans response.message.content, qui est une liste
            # On accède au premier élément puis à son texte, puis on strip pour enlever espaces inutiles
            return response.message.content[0].text.strip()

        except Exception as e:
            # En cas d'erreur d'appel API, on affiche l'erreur en console
            print("Erreur Cohere :", e)
            # Et on renvoie un message simple d'erreur au bot
            return "Erreur"
