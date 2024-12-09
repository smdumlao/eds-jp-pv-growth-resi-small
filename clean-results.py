"""
This script is designed to delete generated files from the project directory. 
Its purpose is to restore the codebase to its base state, containing only the 
minimum required files necessary to run the analysis. 

Use this script to clean up unnecessary or temporary files that were created 
during the analysis process.
"""

import os
import shutil

def delete_paths(paths):
    for path in paths:
        if os.path.exists(path):
            if os.path.isfile(path):
                try:
                    os.remove(path)
                    print(f"Deleted file: {path}")
                except Exception as e:
                    print(f"Error deleting file {path}: {e}")
            elif os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    print(f"Deleted folder: {path}")
                except Exception as e:
                    print(f"Error deleting folder {path}: {e}")
        else:
            print(f"Path does not exist: {path}")


if __name__ == "__main__":
    paths_to_delete = [
        "fig",
        "data/pv_growth_outlier.csv",
        "data/model_RFC_PV_R_2023.joblib",
        "data/model_RFR_PV_R.joblib",
        "data/shap_values_summary_PV_R.csv",
        "data/model_RFC_PV_S_2023.joblib",
        "data/model_RFR_PV_S.joblib",
        "data/shap_values_summary_PV_S.csv"
    ]

    print("Deleting the following paths:")
    for path in paths_to_delete:
        print(f"- {path}")

    confirm = input("Do you want to proceed? (yes/no): ").strip().lower()
    if confirm == 'yes':
        delete_paths(paths_to_delete)
    else:
        print("Deletion cancelled.")