# Import du module Fernet pour le chiffrement symétrique (cryptographie)
from cryptography.fernet import Fernet

# Import de json pour sérialiser / désérialiser les données
import json

# Import d'os pour la gestion des fichiers et chemins
import os


class UserDataManager:
    """
    Classe qui gère les données des utilisateurs (journal, agenda, examens)
    avec chiffrement symétrique via Fernet.
    
    ✔ Les données sont sauvegardées dans un fichier chiffré (ex: userdata.enc)
    ✔ La clé de chiffrement est sauvegardée séparément (ex: secret.key)
    ✔ Chaque utilisateur possède son propre espace de données 
      dans la structure interne `self.data`
    """

    def __init__(self, filepath='userdata.enc', key_file='secret.key'):
        """
        Initialise le gestionnaire.
        
        - filepath : chemin du fichier contenant les données chiffrées.
        - key_file : fichier contenant la clé symétrique Fernet.
        """
        # ✅ Si le fichier contenant la clé de chiffrement n'existe pas
        if not os.path.exists(key_file):
            # Génère une nouvelle clé Fernet
            key = Fernet.generate_key()
            # Sauvegarde cette clé dans le fichier key_file
            with open(key_file, 'wb') as f:
                f.write(key)

        # ✅ Lecture de la clé de chiffrement existante
        with open(key_file, 'rb') as f:
            self.key = f.read()

        # Création de l'objet Fernet pour chiffrer/déchiffrer les données
        self.cipher = Fernet(self.key)

        # Stocke le chemin du fichier de données chiffrées
        self.filepath = filepath

        # ✅ Charge les données en mémoire depuis le fichier
        self._load()

    def _load(self):
        """
        Charge les données depuis le fichier chiffré dans self.data.
        Si le fichier n'existe pas ou s'il est illisible → initialise un dict vide.
        """
        if not os.path.exists(self.filepath):
            # Pas de données → on commence avec un dictionnaire vide
            self.data = {}
            return

        # Lecture du contenu du fichier chiffré
        with open(self.filepath, 'rb') as f:
            enc = f.read()

        try:
            # ✅ Déchiffre les données
            dec = self.cipher.decrypt(enc)
            # Convertit le JSON décodé en dictionnaire Python
            self.data = json.loads(dec)
        except Exception:
            # En cas d'erreur de déchiffrement ou parsing JSON → on réinitialise
            self.data = {}

    def _save(self):
        """
        Chiffre le dictionnaire self.data et l'écrit dans le fichier.
        """
        # Convertit self.data en JSON puis en bytes
        json_bytes = json.dumps(self.data).encode()
        # ✅ Chiffre les données avec Fernet
        enc = self.cipher.encrypt(json_bytes)

        # Écrit le texte chiffré dans le fichier
        with open(self.filepath, 'wb') as f:
            f.write(enc)

    def get_user(self, uid):
        """
        Retourne les données de l'utilisateur `uid`.
        Si aucune donnée n'existe pour cet utilisateur → initialise la structure vide.
        
        Structure par défaut :
        {
            "journal": [],
            "agenda": [],
            "exams": []
        }
        """
        return self.data.setdefault(uid, {
            "journal": [],
            "agenda": [],
            "exams": []
        })

    def add_journal_entry(self, uid, text, date):
        """
        Ajoute une entrée dans le journal de l'utilisateur.
        - uid : identifiant utilisateur
        - text : contenu du ressenti
        - date : date associée à l'entrée
        """
        self.get_user(uid)['journal'].append({"text": text, "date": date})
        self._save()  # Sauvegarde après modification

    def add_agenda_event(self, uid, text):
        """
        Ajoute un événement à l'agenda de l'utilisateur.
        - text : description de l'événement
        """
        self.get_user(uid)['agenda'].append(text)
        self._save()

    def add_exam(self, uid, text):
        """
        Ajoute un examen à la liste de l'utilisateur.
        - text : description (date + matière)
        """
        self.get_user(uid)['exams'].append(text)
        self._save()

    def clear_user(self, uid):
        """
        Supprime toutes les données enregistrées pour un utilisateur.
        """
        if uid in self.data:
            del self.data[uid]  # Efface le dictionnaire
            self._save()
