# -*- Coding: utf-8 -*-

from datetime import timedelta
from pathlib import Path


def create_directory(path):
    """Crée un répertoire avec des sous-répertoires """
    path.mkdir(parents=True, exist_ok=True)

def format_date(date, index, index_prime):
    """Formatte une date avec un index et une option spécifique en fonction du jour de la semaine."""
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

def create_folder(start_date, end_date, current_folder, subfolders):
    """Crée des dossiers à partir d'une date de début jusqu'à une date de fin dans un répertoire donné avec des sous-dossiers optionnels."""
    if end_date < start_date:
        return False

    current_date = start_date
    current_folder_path = Path(current_folder)
    chemins = []
    folder_num = 1
    week_num = start_date.isocalendar()[1]
    index = 1
    index_prime = 0

    while current_date <= end_date:
        if week_num != current_date.isocalendar()[1]:
            folder_num += 1
            week_num = current_date.isocalendar()[1]

        dossier_name = f"Semaine {folder_num}"
        dossier_path = current_folder_path / dossier_name
        create_directory(dossier_path)
        
        path_format, index_prime = format_date(current_date, index, index_prime)
        dossier_path = dossier_path / Path(path_format)
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
            indice = path.find("/[")
            f.write(f'"{path[:indice]} [ACTUELLE]{path[indice:]}"\n')

    return True
