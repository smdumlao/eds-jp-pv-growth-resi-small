import pandas as pd
import numpy as np
import re


def format_mean_std(df, column_name, mean_sno=1, std_sno=2, spacer=" ", std_per=False):
    mean_value = df[column_name].mean()
    std_dev = df[column_name].std()

    if mean_sno == 0:
        mean_value = round(mean_value)
    else:
        mean_value = round(mean_value, mean_sno)

    if std_sno == 0:
        std_dev = round(std_dev)
    else:
        std_dev = round(std_dev, std_sno)

    if std_per:
        format_str = (
            f"{mean_value:.{mean_sno}f}{spacer}±{abs(100*std_dev/mean_value):.1f}%"
        )
    else:
        format_str = f"{mean_value:.{mean_sno}f}{spacer}±{std_dev:.{std_sno}f}"

    return format_str


def apply_scale(df_orig, scale_dict):
    df = df_orig.copy()
    for col, scale in scale_dict.items():
        if col in df.columns:
            df[col] = df[col].div(scale)
    return df


def get_pref_muni_isin(df, index_list):
    return df[df[["pref", "muni"]].apply(tuple, axis=1).isin(index_list)]


def calc_n_show_mean_std(df, scale_param, std_per=False):
    stats = dict()
    for key in scale_param.index:
        stats[key] = format_mean_std(
            df,
            key,
            mean_sno=scale_param.loc[key, "mean_sno"],
            std_sno=scale_param.loc[key, "std_sno"],
            spacer=" ",
            std_per=std_per,
        )
    return stats


def get_cluster_actual_stats(df, cluster_index, scale_param, std_per=False):
    stats = dict()
    scale_dict = scale_param["scaler"].to_dict()

    for cluster_no, cluster_indx in cluster_index.items():
        df_temp = get_pref_muni_isin(df, cluster_indx)
        df_temp = apply_scale(df_temp, scale_dict)
        df_temp = df_temp[scale_dict.keys()]
        stats[cluster_no] = calc_n_show_mean_std(df_temp, scale_param, std_per=std_per)
    stats = pd.DataFrame(stats).T
    return stats


def align_spacing(series):
    """
    Used to standardize the output of `format_mean_std` for each column or rows.
    Usage: df.apply(align_spacing, axis=0) for column wise alignment axis =1 for row-wise.
    """

    def extract_length(s):
        # Extract the part between ± and %
        match = re.search(r"±\s*(.*?)%", s)
        if match:
            return len(match.group(1))
        return 0

    def pad_string(s, max_length):
        # Extract the part between ± and %, then pad with spaces
        match = re.search(r"±\s*(.*?)%", s)
        if match:
            current_length = len(match.group(1))
            padding = " " * (max_length - current_length)
            return re.sub(r"±\s*(.*?)%", f"±{padding}\\1%", s)
        return s

    # Find the maximum length of characters between ± and %
    max_length = series.apply(extract_length).max()

    # Adjust the spacing for each row
    return series.apply(lambda x: pad_string(x, max_length))
