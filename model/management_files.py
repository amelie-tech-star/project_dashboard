import os
import re
import pandas as pd

def get_FILE_dataframe(project_list, date, project_dir ):

    FILE_dataframe = pd.DataFrame()
    
    for project in project_list:

        #############
        # SCHEDULE  #
        #############
        pattern_sched = 'DP0[0-9][0-9][0-9][0-9][0-9]PLG00[0-9]_[0-9][0-9]_WBS_'+ date + '.mpp'
        project_dir_sched = project_dir + project + '\\CLASSEUR_AFFAIRE\\0SUIVI____04_Pilotages\\6_SCHEDULE-NP\\'
        try:
            for root, dirs, files in os.walk(project_dir_sched):
                for file_sched in files:
                    if re.search(pattern_sched, file_sched):
                       raise Exception()
        except Exception:
            print(file_sched)

        FILE_dataframe.loc[project, 'Schedule'] = project_dir_sched + file_sched

        #############
        # FORECAST  #
        #############
        FILE_dataframe.loc[project, 'Forecast'] = project_dir + project + '\\CLASSEUR_AFFAIRE\\0SUIVI____04_Pilotages\\' + project + '.xls'

        ########
        # EVM  #
        ########
        pattern_cost = 'DP0[0-9][0-9][0-9][0-9][0-9]PMG00[0-9]_[0-9][0-9]_Cost_'+ date + '.xlsm'
        project_dir_cost = project_dir + project + '\\CLASSEUR_AFFAIRE\\0SUIVI____04_Pilotages\\7_COST-NP\\'
        try:
            for root, dirs, files_cost in os.walk(project_dir_cost):
                for file_cost in files_cost:
                    print (f"{file_cost}")
                    if re.search(pattern_cost, file_cost):
                       raise Exception()
        except Exception:
            print(file_cost)

        FILE_dataframe.loc[project, 'Cost'] = project_dir_cost + file_cost

        ########
        # TBD  #
        ########
        pattern_int = 'DP0[0-9][0-9][0-9][0-9][0-9]RAV00[0-9]_[0-9][0-9]_Tableau_de_bord-NP_'+ date + '.xlsm'
        project_dir_int = project_dir + project + '\\CLASSEUR_AFFAIRE\\0SUIVI____04_Pilotages\\4_INTEGRATION\\'
        try:
            for root, dirs, files_int in os.walk(project_dir_int):
                for file_int in files_int:
                    if re.search(pattern_int, file_int):
                       raise Exception()
        except Exception:
            print(file_int)
        print(f"{file_int}")
        FILE_dataframe.loc[project, 'TBD'] = project_dir_int + file_int

    return FILE_dataframe
