# -*- Coding: utf-8 -*-

from datetime import timedelta
from pathlib import Path

# Crée un répertoire avec des répertoires parents .
def create_directory(path):
    # Créer le répertoire avec gestion des parents et de l'existence
    path.mkdir(parents=True, exist_ok=True)


# Fonction pour formater la date selon le modèle souhaité
def format_date(date, index, index_prime):
    day_mapping = {"Sam": f" [PRIME-{index_prime + 1}]", "Mar": " [ÉVALS]"}
    jour = date.strftime("%a")
    formatted_date = (
        f"[{index}] {date.strftime('%a-%d-%m-%Y')}{day_mapping.get(jour, '')}"
    )
    index_prime += 1 if jour == "Sam" else 0
    return formatted_date, index_prime

# Crée des dossiers à partir d'une date de début jusqu'à une date de fin dans un répertoire donné avec des sous-dossiers optionnels.
def create_folder(start_date, end_date, current_folder, subfolders):
    # Date actuelle pour commencer la création de dossier
    current_date = start_date
    # Chemin du dossier principal
    current_folder_path = Path(current_folder)
    # Liste pour stocker les chemins des dossiers créés
    chemins = []
    # Index pour numéroter les dossiers
    index = 1
    # Initialisation de l'index_prime pour gérer les options de dossier
    index_prime = 0

    # Boucle pour créer les dossiers pour chaque jour
    while current_date <= end_date:
        # Numéro de semaine actuel
        week_number = current_date.strftime("%V")
        # Nom du dossier de la semaine
        dossier_name = (
            f"Semaine {abs(int(week_number) - int(start_date.strftime('%V')) + 1)}"
        )
        # Chemin complet du dossier de la semaine
        dossier_path = current_folder_path / dossier_name
        # Création du dossier de la semaine
        create_directory(dossier_path)

        # Formatage de la date et gestion des options de dossier
        formatted_date, index_prime = format_date(current_date, index, index_prime)
        # Chemin complet du dossier avec la date formatée
        dossier_path = dossier_path / formatted_date
        # Création du dossier avec la date formatée
        create_directory(dossier_path)

        # Boucle pour créer les sous-dossiers dans le dossier principal
        for subfolder in subfolders:
            if subfolder:
                # Chemin complet du sous-dossier
                subfolder_path = dossier_path / subfolder
                # Création du sous-dossier
                create_directory(subfolder_path)

        # Ajout du chemin à la liste des chemins
        chemins.append(dossier_path.as_posix())
        # Passage à la date suivante
        current_date += timedelta(days=1)
        # Incrémentation de l'index pour le prochain numéro de dossier
        index += 1

    # Écriture des chemins dans un fichier texte
    with open(current_folder_path / "Chemins.txt", "w") as f:
        for path in chemins:
            # Écriture du chemin dans le fichier
            f.write(f'"{path}"\n')
            # Ajout de l'option [ACTUELLE] au chemin et écriture dans le fichier
            indice = path.find("/[")
            f.write(f'"{path[: indice]} [ACTUELLE]{path[indice:]}"\n')
    # Retourne True pour indiquer la réussite de la création des dossiers
    return True
