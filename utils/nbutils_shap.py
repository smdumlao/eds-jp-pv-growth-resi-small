import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import shap


def plot_feature_importance_base(df, vars_dv, year):
    # Filter the DataFrame for the year 2023
    df_temp = df[df["year"] == year]

    # Define independent and dependent variables
    vars_iv = ["demand", "land_avail", "taxable_income", "LV", "SPR", "pv_out"]
    X = df_temp[vars_iv]
    y = df_temp[vars_dv]

    # Train the model
    model = RandomForestRegressor(random_state=42)

    model.fit(X, y)

    # Calculate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # Predict and calculate residuals
    predictions = model.predict(X)
    residuals = y - predictions

    # Summary plot
    shap.summary_plot(shap_values, X, feature_names=vars_iv)

    # Bar plot to rank feature importance
    shap.summary_plot(shap_values, X, plot_type="bar", feature_names=vars_iv)

    shap_scores_df = pd.DataFrame(shap_values, columns=vars_iv)

    shap_pred = shap_scores_df.sum(axis=1) + explainer.expected_value

    print("r2:", r2_score(shap_pred, y))

    mean_abs_shap_values = np.mean(np.abs(shap_values), axis=0)
    shap_importance_df = pd.DataFrame.from_dict(
        {"mean_abs": mean_abs_shap_values}, orient="index", columns=vars_iv
    )
    shap_importance_df.loc["%"] = (
        shap_importance_df.div(shap_importance_df.sum(axis=1), axis=0)
        .loc["mean_abs"]
        .to_dict()
    )
    print("Normalized SHAP Feature Importance")
    print(shap_importance_df)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(8, 8)
    shap_scores_df.plot(ax=ax, x="demand", y="land_avail", lw=0, marker=".")
    ax.axvline(x=0, color="r", linestyle="--", linewidth=2)
    ax.axhline(y=0, color="r", linestyle="--", linewidth=2)
