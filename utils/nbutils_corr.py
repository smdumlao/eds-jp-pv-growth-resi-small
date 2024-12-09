import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

from utils.japan_admin_data import prefecture_dict_en_to_no, prefecture_dict_jp_to_en


def plot_demand_cap_corr(demand, pv_cap, axs=None, ylabel=None, xlabel=None):
    if axs is None:
        fig, axs = plt.subplots(1, 2)
        fig.set_size_inches(12, 6)
    # Calculate the correlation coefficient
    correlation_coefficient = np.corrcoef(demand, pv_cap)[0, 1]

    # Perform linear regression
    m, b = np.polyfit(demand, pv_cap, 1)
    x_val = range(0, 30, 1)
    y_pred = m * x_val + b

    def plot_values(ax):
        ax.scatter(demand, pv_cap, color="blue", s=5)
        ax.plot(x_val, y_pred, color="red")

        # Annotating the correlation coefficient
        ax.text(
            0.05,
            0.95,
            f"Correlation coefficient: {correlation_coefficient:.2f}",
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment="top",
        )

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)

    for ax in axs:
        plot_values(ax)

    return fig, axs


def plot_corr_matrix_with_p_values(
    df, method="pearson", figsize=(10, 8), title="Correlation Matrix Heatmap"
):
    # Validate the method parameter
    if method not in ["pearson", "spearman"]:
        raise ValueError("Method must be either 'pearson' or 'spearman'")

    # Calculate correlation matrix
    correlation_matrix = df.corr(method=method)

    # Initialize a matrix for p-values
    p_matrix = pd.DataFrame(
        np.zeros_like(correlation_matrix), columns=df.columns, index=df.columns
    )

    # Calculate p-values
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            if i == j:
                p_matrix.iloc[i, j] = np.nan
            else:
                if method == "pearson":
                    _, p_value = pearsonr(df.iloc[:, i], df.iloc[:, j])
                elif method == "spearman":
                    _, p_value = spearmanr(df.iloc[:, i], df.iloc[:, j])
                p_matrix.iloc[i, j] = p_value

    fig, ax = plt.subplots(figsize=figsize)

    # Adjust alpha of the colormap
    cax = ax.imshow(
        correlation_matrix, cmap="coolwarm", interpolation="none", alpha=0.75
    )
    fig.colorbar(cax, ax=ax)

    ax.set_xticks(range(len(correlation_matrix)))
    ax.set_yticks(range(len(correlation_matrix)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    ax.set_title(f"{title} ({method.capitalize()})")

    for i in range(len(correlation_matrix)):
        for j in range(len(correlation_matrix)):
            # Determine significance level
            p_value = p_matrix.iloc[i, j]
            if p_value < 0.001:
                significance = "***"
            elif p_value < 0.01:
                significance = "**"
            elif p_value < 0.05:
                significance = "*"
            else:
                significance = ""

            # Build the text to display
            coeff = correlation_matrix.iloc[i, j]
            if np.isnan(p_value):
                if coeff == 1:
                    text = ""
                else:
                    text = f"{coeff:.2f}"
            else:
                text = f"{coeff:.2f}\n({p_value:.3f})\n{significance}"

            ax.text(j, i, text, ha="center", va="center", color="black", fontsize=10)

    return fig, ax


def set_splits(ax, splits):
    if not isinstance(splits, list):
        splits = [splits]
    for split in splits:
        ax.axhline(y=split, color="k")
        ax.axvline(x=split, color="k")


def set_lims_demand_pv_corr(axs, ylabel=None, xlabel=None):
    axs[0].set_ylim(0, 500)
    axs[0].set_xlim(0, 25)

    axs[1].set_ylim(0, 100)
    axs[1].set_xlim(0, 5)

    for ax in axs:
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)


def plot_corr_matrix(correlation_matrix, figsize=(10, 8)):
    fig, ax = plt.subplots(figsize=figsize)

    cax = ax.imshow(correlation_matrix, cmap="coolwarm", interpolation="none")
    fig.colorbar(cax, ax=ax)

    ax.set_xticks(range(len(correlation_matrix)))
    ax.set_yticks(range(len(correlation_matrix)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    ax.set_title("Correlation Matrix Heatmap")

    for i in range(len(correlation_matrix)):
        for j in range(len(correlation_matrix)):
            ax.text(
                j,
                i,
                f"{correlation_matrix.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                color="black",
            )

    return fig, ax


def plot_growth_rate(pv_params, pv_cols, ylim=None, ylabel=None, barcolor="blue"):
    pv_params_pref_cap = pv_params[["pref"] + pv_cols]
    pv_params_pref_cap = pv_params_pref_cap.groupby("pref").sum()
    pv_params_pref_cap.index = pv_params_pref_cap.index.map(prefecture_dict_jp_to_en)
    jp_mean_pct_change = pv_params_pref_cap.sum().pct_change().mean()
    print("Japan Mean PCT Change:", jp_mean_pct_change)

    dfx = pv_params_pref_cap.copy()

    # Calculate the yearly growth rate
    growth_rate = dfx.pct_change(axis=1)

    # Fill any NaN values that arise from percentage change calculation (first column will be NaN)
    growth_rate.fillna(0, inplace=True)

    # Calculate the mean growth rate for each prefecture
    growth_rate["mean_growth"] = growth_rate.iloc[:, 1:].mean(axis=1)

    # Calculate the mean and standard deviation of the mean growth rates
    mean_growth_rate = growth_rate["mean_growth"].mean()
    std_growth_rate = growth_rate["mean_growth"].std()
    print("Prefecture Mean PCT Change:", mean_growth_rate)
    # print("Prefecture Var PCT Change:", growth_rate['mean_growth'].var())
    print("Prefecture Std PCT Change:", growth_rate["mean_growth"].std())

    # Compute the Z-score for each prefecture's mean growth rate
    growth_rate["z_score"] = (
        growth_rate["mean_growth"] - mean_growth_rate
    ) / std_growth_rate

    # Define a threshold for identifying outliers (e.g., Z-score > 1.64 for a 90% confidence interval)
    z_score_threshold = 1.64

    growth_rate["id"] = growth_rate.index.map(prefecture_dict_en_to_no)
    growth_rate = growth_rate.sort_values("id")

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(10, 4)
    growth_rate["mean_growth"].mul(100).plot(ax=ax, kind="bar", color=barcolor)
    ax.axhline(y=jp_mean_pct_change * 100, color="k", ls=":")
    ax.set_xlabel(None)
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)
    ax.axhline(y=jp_mean_pct_change * 100, color="k", ls=":")
    ax.axhline(y=(jp_mean_pct_change - 1.64 * std_growth_rate) * 100, color="r", ls=":")
    ax.axhline(y=(jp_mean_pct_change + 1.64 * std_growth_rate) * 100, color="r", ls=":")

    ax.axhline(y=jp_mean_pct_change * 100, color="k", ls=":")
    growth_rate[
        ~growth_rate["z_score"].between(-z_score_threshold, z_score_threshold)
    ].sort_values("z_score")

    return fig, ax


def get_correl_type_from_title(ax):
    title = ax.get_title()
    if "pearson" in title.lower():
        correl_type = "pearson"
    elif "spearman" in title.lower():
        correl_type = "spearman"
    else:
        correl_type = "unknown"

    return correl_type


vars_iv_rename_cols = {
    "demand": "DEMAND",
    "land_avail": "LANDAV",
    "taxable_income": "TAXIN",
    "pv_out": "PVOUT",
    "LV": "LANDVL",
    "SPR": "PENERT",
}
