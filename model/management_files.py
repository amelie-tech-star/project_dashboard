import os
import re
import pandas as pd

pattern_ref = '[0-9][0-9]-[0-9][0-9][0-9][0-9].A[0-9][0-9][0-9].[0-9][0-9][0-9].[A-Z][0-9]'
dir_pilotage = '\\__ A2-GESTION DE PROJET\\A229-Suivi Projet\\'
#dir_pilotage = '\\C4 Offres & Devis Commerciaux internes\\'

def get_FILE_loc(project_dir, project, file_dir, identifiant, extension, date):
    pattern_file = pattern_ref + "_" + identifiant + "_" + date + extension
    print(pattern_file)
    project_dir_current = project_dir + project + dir_pilotage + file_dir
    print(project_dir_current)
    
    found_file = None
    
    for root, dirs, files in os.walk(project_dir_current):
        for file_resource in files:
            if re.search(pattern_file, file_resource):
                found_file = file_resource
                print(f"{identifiant}  = {file_resource}")
                break
        if found_file:
                break

    return project_dir_current + file_resource

def get_FILE_dataframe(project_list, date, project_dir ):

    FILE_dataframe = pd.DataFrame()
    
    for project in project_list:

        #############
        # TBD       #
        #############
        FILE_dataframe.loc[project, 'TBD'] = get_FILE_loc(project_dir, project, "4_Integration\\", "GP", ".xlsx", date)

        ################
        # WBS          #
        ################
        FILE_dataframe.loc[project, 'Scope'] = get_FILE_loc(project_dir, project, "5_Scope\\", "WBS", ".vsdx", date)

        #############
        # SCHEDULE  #
        #############
        FILE_dataframe.loc[project, 'Schedule'] = get_FILE_loc(project_dir, project, "6_Schedule\\", "Shedule", ".mpp", date)

        #############
        # FORECAST  #
        #############
        #FILE_dataframe.loc[project, 'Forecast'] = get_FILE_loc(project_dir, project, "..\\A250-TDB\\", project, ".xlsx", date)

        #############
        # EVM       #
        #############
        FILE_dataframe.loc[project, 'Cost'] = get_FILE_loc(project_dir, project, "7_Cost\\", "Cost", ".xlsm", date)

        #############
        # RESOURCES #
        #############
        FILE_dataframe.loc[project, 'Resource'] = get_FILE_loc(project_dir, project, "9_Resource\\", "OBS", ".vsdx", date)

        ################
        # PROCUREMENT  #
        ################
        FILE_dataframe.loc[project, 'Procurement'] = get_FILE_loc(project_dir, project, "12_Procurement\\", "Procurement", ".vsdx", date)

        ################
        # STAKEHOLDERS #
        ################
        FILE_dataframe.loc[project, 'Stakeholders'] = get_FILE_loc(project_dir, project, "13_Stakeholders\\", "Stakeholders", ".vsdx", date)

    return FILE_dataframe
