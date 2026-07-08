import pandas as pd
import shutil
from model import management_files
import re
import os
from pathlib import Path
from configparser import ConfigParser

FILE_dataframe = pd.DataFrame()

# Parse the config.ini file
config = ConfigParser()
config.read("config.ini")

# Get configuration
project_list = [p.strip() for p in config["General"]["project_list"].split(",")]
project_dir = config["General"]["project_dir"]
pattern_ref = config["General"]["pattern_ref"]
dir_pilotage  = config["General"]["dir_pilotage"]
date = config["General"]["date"]
new_date = config["General"]["new_date"]

file_list = ["TBD", "GP", "Schedule", "Cost", "Resource" ]
old_file = {}
new_file = {}

FILE_dataframe = management_files.get_FILE_dataframe(project_list, date, project_dir, dir_pilotage, pattern_ref)

def replace_and_increment(match):
    original_number = match.group(1)  # Extraire "01"
    incremented_number = int(original_number) + 1  # Convertir en entier et incrémenter
    return f"_{incremented_number:02}_"  # Reformater en deux chiffres

for project in project_list:
    for index in file_list:
        print(f"########## COPY FILE {index} ##########")
        old_file[index] = FILE_dataframe.loc[project, index]
        new_file[index] = Path(old_file[index].replace(date, new_date))
        new_file[index].with_name (re.sub(r"(\d{2})_", replace_and_increment, new_file[index].name))
        if os.path.exists(old_file[index]):
            if os.path.exists(os.path.dirname(new_file[index])) and not Path(new_file[index]).exists():
                #print("Le répertoire {0} existe.".format(os.path.dirname(new_file[index])))
                print (f"Le fichier {new_file[index]} est crée");
                shutil.copy2(Path(old_file[index]), Path(new_file[index]))
            else:
                print("Le répertoire {0} n'existe pas ou \nle fichier {1} existe déjà.\n".format(os.path.dirname(new_file[index]), new_file[index]))

