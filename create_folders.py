# -*- Coding: utf-8 -*-

from datetime import timedelta
from pathlib import Path


def create_directory(path):
    # Créer le répertoire avec gestion des parents et de l'existence
    path.mkdir(parents=True, exist_ok=True)


# Fonction pour formater la date selon le modèle souhaité et mettre à jour index_prime
def format_date(date, index, index_prime):
    day_mapping = {"Sam": f" [PRIME-{index_prime + 1}]", "Mar": " [ÉVALS]"}
    jour = date.strftime("%a")
    formatted_date = (
        f"[{index}] {date.strftime('%a-%d-%m-%Y')}{day_mapping.get(jour, '')}"
    )
    index_prime += 1 if jour == "Sam" else 0
    return formatted_date, index_prime


def creer_dossier(start_date, end_date, current_folder, subfolders):
    current_date = start_date
    current_folder_path = Path(current_folder)
    chemins = []
    index = 1
    index_prime = 0

    while current_date <= end_date:
        week_number = current_date.strftime("%V")
        dossier_name = (
            f"Semaine {int(week_number) - int(start_date.strftime('%V')) + 1}"
        )
        dossier_path = current_folder_path / dossier_name
        create_directory(dossier_path)

        formatted_date, index_prime = format_date(current_date, index, index_prime)
        dossier_path = dossier_path / formatted_date
        create_directory(dossier_path)

        for subfolder in subfolders:
            if subfolder:
                subfolder_path = dossier_path / subfolder
                create_directory(subfolder_path)

        chemins.append(dossier_path.as_posix())
        current_date += timedelta(days=1)
        index += 1

    with open(current_folder_path / "Chemins.txt", "w") as f:
        for path in chemins:
            f.write(f'"{path}"\n')
            f.write(f'"{path} [ACTUELLE]"\n')
    return True
