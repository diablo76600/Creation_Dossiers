# -*- Coding: utf-8 -*-

from datetime import timedelta, date
from pathlib import Path


def create_directory(path):
    """Crée un répertoire avec des sous-répertoires."""
    path.mkdir(parents=True, exist_ok=True)

def get_formatted_date(date, index_folder, index_prime):
    """Formatte une date avec un index et une option spécifique 
        en fonction du jour de la semaine."""
    jour = date.isoweekday()
    formatted_date = date.strftime(f"[{index_folder}] %a-%d-%m-%Y")
    if jour == 2:
        formatted_date += " [ÉVALS]​"
    elif jour == 6:
        index_prime += 1
        formatted_date += f" [PRIME-{index_prime}]"
    return formatted_date, index_prime

def manage_directory_creation(
    date, folder_number, index_folder, index_prime, current_folder, subfolders
):
    """Gère la création d'un répertoire avec des sous-dossiers optionnels 
        en fonction des paramètres fournis."""
    folder_name = f"Semaine {folder_number}"
    folder_path = Path(current_folder) / folder_name
    create_directory(folder_path)
    path_format, index_prime = get_formatted_date(date, index_folder, index_prime)
    folder_path = folder_path / Path(path_format)
    create_directory(folder_path)
    for subfolder in subfolders:
        if subfolder:
            subfolder_path = folder_path / subfolder
            create_directory(subfolder_path)
    return folder_path.as_posix(), index_prime

def create_folder(start_date, end_date, current_folder, subfolders, checkbox):
    # sourcery skip: simplify-boolean-comparison
    """Crée un répertoire avec des sous-répertoires."""
    if end_date < start_date:
        return False

    current_date = start_date
    paths = []
    folder_num = 1
    week_num = start_date.isocalendar()[1]
    index_folder = 1
    index_prime = 0
    day_bool = start_date.isoweekday() == 6

    while current_date <= end_date:
        if checkbox.isChecked() and day_bool:
            paths.extend(
                create_paths(current_date, folder_num, index_folder,
                    index_prime, current_folder, subfolders, checkbox))
            current_date += timedelta(days=2)
            index_folder += 2
            index_prime += 1
            week_num = current_date.isocalendar()[1]
            day_bool = False
        else:
            path, index_prime = manage_directory_creation(
                current_date, folder_num, index_folder, index_prime,
                current_folder, subfolders)
            paths.append(path)
            current_date += timedelta(days=1)
            index_folder += 1
            if week_num != current_date.isocalendar()[1]:
                folder_num += 1
                week_num = current_date.isocalendar()[1]
    write_paths_to_file(paths, current_folder)
    return True

def create_paths(current_date, folder_num,
    index_folder, index_prime, current_folder, subfolders, checkbox):
    weekend_paths = []
    for _ in range(2):
        path, index_prime = manage_directory_creation(
            current_date, folder_num, index_folder, index_prime, 
            current_folder, subfolders)
        weekend_paths.append(path)
        current_date += timedelta(days=1)
        index_folder += 1
    return weekend_paths

def write_paths_to_file(paths, current_folder):
    with open(Path(current_folder) / "Chemins.txt", "w") as f:
        for path in paths:
            f.write(f'"{path}"\n')
            index = path.find("/[")
            f.write(f'"{path[:index]} [ACTUELLE]{path[index:]}"\n')
