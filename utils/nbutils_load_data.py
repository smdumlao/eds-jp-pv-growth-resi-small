import pandas as pd
import numpy as np
import os


def load_and_process_data(folder, build_df=True):
    fileloc = os.path.join(folder, "pv_muni_params.csv")
    # definitions
    ftr_pref_muni = ["pref", "muni"]

    # load files
    pv_params = pd.read_csv(fileloc)

    # compute for total
    for year in range(2014, 2024):
        pv_params[f"PV_A_{year}"] = pv_params.filter(regex=rf"^PV_.*_{year}$").sum(
            axis=1
        )

    # available land is defined as the remaining habitable land after the land from buildings and agriculture were removed.
    pv_params["land_avail"] = (
        pv_params["land_habitable"]
        - pv_params["land_buildings"]
        - pv_params["land_agri"]
    )

    # build the dataframe for analysis
    if build_df:
        df = build_df_for_analysis(pv_params)
    else:
        df = None

    return pv_params, df


def build_df_for_analysis(pv_params, years=range(2014, 2024)):
    df = []

    # these data do not change every year
    ftr_pref_muni = ["pref", "muni"]
    col_same_val = [
        "demand",
        "land_avail",
        "taxable_income",
        "pv_out",
    ]
    constant_df = pv_params[ftr_pref_muni + col_same_val]

    # these data changes per year. The independent variables are the value the previous year.
    for year in years:
        # this year's capacity
        col_yearly_y = [
            f"PV_R_{year}",
            f"PV_S_{year}",
            f"PV_M_{year}",
            f"PV_U_{year}",
            f"PV_A_{year}",
        ]
        pv_cap_y = pv_params[col_yearly_y]
        pv_cap_y = 100 * pv_cap_y / pv_cap_y.sum()
        pv_cap_y.columns = ["PV_R", "PV_S", "PV_M", "PV_U", "PV_A"]

        # land value and solar penetration rate
        col_lv_spr = [f"LV_{year}", f"SPR_{year}"]
        lv_spr_df = pv_params[col_lv_spr]
        lv_spr_df.columns = ["LV", "SPR"]

        df_temp = pd.concat([constant_df, lv_spr_df, pv_cap_y], axis=1)
        df_temp.insert(0, "year", year)
        df.append(df_temp)

    df = pd.concat(df).reset_index(drop=True)

    return df


def csv_str_to_df(csv_str, header_row=None, index_col=None):
    # Split the input string into lines
    lines = csv_str.strip().split("\n")

    # Extract the header and rows
    if not header_row is None:
        header = lines[header_row].split(",")
        rows = [line.strip().split(",") for line in lines[header_row + 1 :]]
    else:
        header = None
        rows = [line.strip().split(",") for line in lines]

    # Create the DataFrame
    df = pd.DataFrame(rows, columns=header)
    if index_col in df.columns:
        df = df.set_index(index_col)
        df.index.name = None
    return df


def get_scale_param():
    scale_param = """
    var,unit,scaler,unit_scaled,mean_sno,std_sno
    demand,MWh,1_000,GWh,0,0
    land_avail,ha,1,ha,0,0
    taxable_income,JPY, 1_000_000,M JPY,0,0
    LV,M JPY,1_000,B JPY,0,0
    pv_out,kWh/kW/year,1,kWh/kW/year,0,0
    SPR,unit,0.01,%,2,2
    """

    scale_param = csv_str_to_df(scale_param, header_row=0, index_col="var")
    scale_param["scaler"] = scale_param["scaler"].astype("float")
    scale_param["mean_sno"] = scale_param["mean_sno"].astype("int")
    scale_param["std_sno"] = scale_param["std_sno"].astype("int")

    return scale_param
