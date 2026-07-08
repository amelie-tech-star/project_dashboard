import os
import re
import pandas as pd
from pathlib import Path


def get_FILE_loc(project_dir, project, file_dir, identifiant, extension, pattern_ref, date):
    pattern_file = pattern_ref + "_" + identifiant + "_" + date + extension
    
    print("########## GET FILE LOCATION FOR: ##########")
    print(pattern_file)
    project_dir_current = project_dir + project + file_dir
    
    print(project_dir_current)
    
    if Path(project_dir_current).exists() and Path(project_dir_current).is_dir():
        print("Le répertoire existe.")
    else:
        print("Le répertoire n'existe pas.")
    
    found_file = None
    
    for root, dirs, files in os.walk(project_dir_current):
        for file_resource in files:
            result = re.search(pattern_file, file_resource)
            if result:
                found_file = file_resource
                print(f"MATCH {identifiant}  = {file_resource}")
                break

    returned_file = ""
    if found_file != None:
        print(f"Le fichier trouvé est {found_file}")
        returned_file = project_dir_current + found_file
    else:
        print("Le fichier n'a pas été trouvé.")   
        
    return returned_file

def get_FILE_dataframe(project_list, date, project_dir, dir_pilotage, pattern_ref):

    FILE_dataframe = pd.DataFrame()
    
    for project in project_list:

        #############
        # TBD       #
        #############
        FILE_dataframe.loc[project, 'TBD'] = get_FILE_loc(project_dir, project, dir_pilotage, "GP", ".xlsx", pattern_ref, date)

        ################
        # VISIO GP     #
        ################
        FILE_dataframe.loc[project, 'GP'] = get_FILE_loc(project_dir, project, dir_pilotage, "GP", ".vsdx", pattern_ref, date)

        #############
        # SCHEDULE  #
        #############
        FILE_dataframe.loc[project, 'Schedule'] = get_FILE_loc(project_dir, project, f"{dir_pilotage}6_Schedule\\", "Schedule", ".mpp", pattern_ref, date)

        #############
        # RESOURCE  #
        #############
        FILE_dataframe.loc[project, 'Resource'] = get_FILE_loc(project_dir, project, f"{dir_pilotage}\\..\\..\\____ R0-R9-REALISATION\\", "Fiche_demande_de_travaux", ".xlsx", pattern_ref, date)

        #############
        # EVM       #
        #############
        FILE_dataframe.loc[project, 'Cost'] = get_FILE_loc(project_dir, project, f"{dir_pilotage}7_Cost\\", "Cost", ".xlsm", pattern_ref, date)


    return FILE_dataframe
