# -*- Coding: utf-8 -*-

from datetime import timedelta
from pathlib import Path


def create_directory(path):
    """Crée un répertoire avec des sous-répertoires """
    path.mkdir(parents=True, exist_ok=True)

def format_date(date, index_folder, index_prime):
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
    formatted_date = f"[{index_folder}] {jour}-{jour_numero}-{mois_annee}{option}"
    return formatted_date, index_prime


def create_folder(start_date, end_date, current_folder, subfolders, checkbox):
    """Crée des dossiers à partir d'une date de début jusqu'à une date de fin dans un répertoire donné avec des sous-dossiers optionnels."""
    if end_date < start_date:
        return False

    def manage_directory_creation(date, folder_number, index_folder, index_prime):
        """Gère la création d'un répertoire avec des sous-dossiers optionnels en fonction des paramètres fournis."""
        folder_name = f"Semaine {folder_number}"
        folder_path = Path(current_folder) / folder_name
        create_directory(folder_path)
        path_format, index_prime = format_date(date, index_folder, index_prime)
        folder_path = folder_path / Path(path_format)
        create_directory(folder_path)
        for subfolder in subfolders:
            if subfolder:
                subfolder_path = folder_path / subfolder
                create_directory(subfolder_path)
        return folder_path.as_posix(), index_prime

    current_date = start_date
    paths = []
    folder_num = 1
    week_num = start_date.isocalendar()[1]
    index_folder = 1
    index_prime = 0

    while current_date <= end_date:
        if checkbox.isChecked() and current_date.strftime("%a") == "Sam":
            for _ in range(2):
                path, index_prime = manage_directory_creation(
                    current_date, folder_num, index_folder, index_prime
                )
                paths.append(path)
                current_date += timedelta(days=1)
                index_folder += 1
            checkbox.setChecked(False)
            week_num = current_date.isocalendar()[1]

        if week_num != current_date.isocalendar()[1]:
            folder_num += 1
            week_num = current_date.isocalendar()[1]

        path, index_prime = manage_directory_creation(
            current_date, folder_num, index_folder, index_prime
        )
        paths.append(path)
        current_date += timedelta(days=1)
        index_folder += 1

    with open(Path(current_folder) / "Chemins.txt", "w") as f:
        for path in paths:
            f.write(f'"{path}"\n')
            index = path.find("/[")
            f.write(f'"{path[:index]} [ACTUELLE]{path[index:]}"\n')

    return True
