import pandas as pd
import shutil
from model import management_files
import re
import os
from pathlib import Path

FILE_dataframe = pd.DataFrame()
project_list = ['25-0030 - FLYCERA']
project_dir = '\\\\dfs\\AIX\\KNS\\Doc_KN\\XXX affaires\\2025\\'
pattern_ref = '[0-9][0-9]-[0-9][0-9][0-9][0-9].A[0-9][0-9][0-9].[0-9][0-9][0-9]'
dir_pilotage = '\\__ A2-GESTION DE PROJET\\A227-229 Suivi Projet\\'
date = '2026-03-31'
new_date = '2026-04-30'
file_list = ["TBD", "Scope", "Schedule", "Cost", "Forecast", "Resource", "Procurement", "Stakeholders"]
old_file = {}
new_file = {}

FILE_dataframe= management_files.get_FILE_dataframe(project_list, date, project_dir)

def replace_and_increment(match):
    original_number = match.group(1)  # Extraire "01"
    incremented_number = int(original_number) + 1  # Convertir en entier et incrémenter
    return f"_{incremented_number:02}_"  # Reformater en deux chiffres

for project in project_list:
    for index in file_list:
        old_file[index] = FILE_dataframe.loc[project, index]
        new_file[index] = Path(old_file[index].replace(date, new_date))
        new_file[index].with_name (re.sub(r"(\d{2})_", replace_and_increment, new_file[index].name))
        if os.path.exists(old_file[index]):
            if os.path.exists(os.path.dirname(new_file[index])) and not Path(new_file[index]).exists():
                #print("Le répertoire {0} existe.".format(os.path.dirname(new_file[index])))
                shutil.copy2(Path(old_file[index]), Path(new_file[index]))
            else:
                print("Le répertoire {0} n'existe pas ou \nle fichier {1} existe déjà.\n".format(os.path.dirname(new_file[index]), new_file[index]))

    # Ajouter la date à Forecast
    old_forecast_name = Path(FILE_dataframe.loc[project, 'Forecast'])
    #print(old_forecast_name)
    #print(old_forecast_name.parent)
    # Ajouter la date juste avant l'extension
    new_forecast_name = old_forecast_name.parent /Path(*["7_COST", "_ZBA"]) / "{0}_{1}{2}".format(old_forecast_name.stem, date, old_forecast_name.suffix)

    print("New forecast {0}".format(new_forecast_name))
    # Déplacer le nouveau fichier dans _ZBA
    if not Path(new_forecast_name).exists():
        shutil.copy2(Path(old_forecast_name), Path(new_forecast_name))
