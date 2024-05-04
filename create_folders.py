# -*- Coding: utf-8 -*-

from pathlib import Path
from datetime import timedelta
import locale

# Définir la localisation en français
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


# Fonction pour formater la date selon le modèle souhaité et mettre à jour index_prime
def format_date(date, index, index_prime):
    option = ""
    jour = date.strftime("%a")
    jour_numero = date.strftime("%d")
    mois_annee = date.strftime("%m-%Y")
    if jour == "Sam":
        index_prime += 1
        option = f" [PRIME-{index_prime}]"
    elif jour == "Mar":
        option = " [ÉVALS]​"
    formatted_date = f"[{index}] {jour}-{jour_numero}-{mois_annee}{option}"
    return formatted_date, index_prime


# Fonction pour créer les dossiers avec leurs sous-dossiers "Photos"
def creer_dossier(start_date, end_date, current_folder, subfolders):
    current_date = start_date

    start_week_offset = (
        start_date - timedelta(days=start_date.weekday())
    ).isocalendar()[1] - 1

    # Contrôle si date de fin < date de début
    if end_date < current_date:
        return False
    index = 1  # Index pour les numéros de dossier
    chemins = []  # Liste pour stocker les chemins des dossiers créés
    index_prime = 0  # Initialisation de index_prime
    while current_date <= end_date:
        # Récupération du numéro de semaine
        semaine_numero = (
            current_date - timedelta(days=current_date.weekday())
        ).isocalendar()[1] - start_week_offset
        # Création du nom de dossier formaté avec la semaine
        dossier_name = "Semaine {}".format(semaine_numero)
        # Création du chemin complet du dossier
        dossier_path = Path(current_folder) / dossier_name
        # Vérifier si le dossier de la semaine existe, sinon le créer
        dossier_path.mkdir(parents=True, exist_ok=True)
        # Création du dossier de la semaine et mise à jour de index_prime
        formatted_date, index_prime = format_date(current_date, index, index_prime)
        dossier_path = dossier_path / formatted_date
        dossier_path.mkdir(parents=True, exist_ok=True)
        # Créer les sous-dossiers dans le dossier de la semaine
        for subfolder in subfolders:
            if subfolder:
                subfolder_path = dossier_path / subfolder
                subfolder_path.mkdir(parents=True, exist_ok=True)
        # Ajouter le chemin à la liste
        chemins.append(dossier_path.as_posix())
        # Passage à la date suivante
        current_date += timedelta(days=1)
        # Incrémenter l'index pour le prochain numéro de dossier
        index += 1

    # Création du fichier chemin.txt
    with open(Path(current_folder) / "Chemins.txt", "w") as f:
        # Écrire chaque chemin dans le fichier, en les séparant par des sauts de ligne
        for path in chemins:
            f.write(f'"{path}"\n')
            f.write(f'"{path} [ACTUELLE]"\n')
    return True
