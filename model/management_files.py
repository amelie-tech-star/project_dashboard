import os
import re
import pandas as pd

def get_FILE_dataframe(project_list, date, project_dir ):

    FILE_dataframe = pd.DataFrame()
    
    pattern_ref = '[0-9][0-9]-[0-9][0-9][0-9][0-9].A[0-9][0-9][0-9].[0-9][0-9][0-9].[A-Z][0-9]'
    dir_pilotage = '\\__ A2-GESTION DE PROJET\\A227-229 Suivi Projet\\'
    
    for project in project_list:

        #############
        # SCHEDULE  #
        #############
        pattern_sched = pattern_ref + '_Schedule_'+ date + '.mpp'
        project_dir_sched = project_dir + project + dir_pilotage + '6_Schedule\\'
        print (project_dir_sched)
        try:
            for root, dirs, files in os.walk(project_dir_sched):
                for file_sched in files:
                    if re.search(pattern_sched, file_sched):
                       raise Exception()
        except Exception:
            print(file_sched)

        print(f"SCHEDULE  = {file_sched}")
        FILE_dataframe.loc[project, 'Schedule'] = project_dir_sched + file_sched

        #############
        # FORECAST  #
        #############
        
        FILE_dataframe.loc[project, 'Forecast'] = project_dir + project + dir_pilotage + '..\\' + project + '.xlsx'
        print(f"FORECAST  = {FILE_dataframe.loc[project, 'Forecast']}")

        ########
        # EVM  #
        ########
        pattern_cost = pattern_ref + '_Cost_'+ date + '.xlsm'
        project_dir_cost = project_dir + project + dir_pilotage + '7_Cost\\'
        try:
            for root, dirs, files_cost in os.walk(project_dir_cost):
                for file_cost in files_cost:
                    if re.search(pattern_cost, file_cost):
                       raise Exception()
        except Exception:
            print(file_cost)

        print(f"COST  = {file_cost}")
        FILE_dataframe.loc[project, 'Cost'] = project_dir_cost + file_cost

        ########
        # TBD  #
        ########
        pattern_int = pattern_ref + '_TBD_'+ date + '.xlsm'
        project_dir_int = project_dir + project + dir_pilotage + '4_Integration\\'
        try:
            for root, dirs, files_int in os.walk(project_dir_int):
                for file_int in files_int:
                    if re.search(pattern_int, file_int):
                       raise Exception()
        except Exception:
            print(file_int)
        
        print(f"TBD  = {file_int}")
        FILE_dataframe.loc[project, 'TBD'] = project_dir_int + file_int

    return FILE_dataframe
