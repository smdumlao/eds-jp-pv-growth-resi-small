import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def scale_data(df, vars_iv=None, var_dv=None, iv_scaler=None, dv_scaler=None):
    """
    scales the corresponding variables if scaler is provided.
    """
    if vars_iv and iv_scaler:
        # Standardize the independent variables
        df[vars_iv] = iv_scaler.fit_transform(df[vars_iv])
    if var_dv and dv_scaler:
        # Standardize the dependent variable
        df[var_dv] = dv_scaler.fit_transform(df[[var_dv]])
    return df, iv_scaler, dv_scaler


def train_and_evaluate(X, y, model, **kwargs):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train, **kwargs)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    return model, r2, mae, mse, rmse


def regression_analysis(
    df, vars_iv, var_dv, model, iv_scaler=None, dv_scaler=None, **kwargs
):
    df_temp = df.copy()
    df_temp, iv_scaler, dv_scaler = scale_data(
        df_temp, vars_iv, var_dv, iv_scaler, dv_scaler
    )
    X = df_temp[vars_iv]
    y = df_temp[var_dv]
    trained_model, r2, mae, mse, rmse = train_and_evaluate(X, y, model, **kwargs)

    if hasattr(trained_model, "feature_importances_"):
        importances = list(trained_model.feature_importances_)
        stats = [r2, mae, mse, rmse] + importances
        keys = ["r2", "mae", "mse", "rmse"] + vars_iv
    elif hasattr(trained_model, "coef_"):
        importances = list(trained_model.coef_)
        stats = [r2, mae, mse, rmse] + importances
        keys = ["r2", "mae", "mse", "rmse"] + vars_iv
    else:
        stats = [r2, mae, mse, rmse]
        keys = ["r2", "mae", "mse", "rmse"]

    return keys, stats, trained_model, dv_scaler


def regression_analysis_yearly(
    df, vars_iv, var_dv, model, iv_scaler=None, dv_scaler=None, **kwargs
):
    logs = []
    trained_models = dict()
    dv_scalers = dict()

    for year in range(2014, 2024):
        df_y = df[df["year"] == year].copy()
        keys, stats, trained_models[year], dv_scalers[year] = regression_analysis(
            df_y, vars_iv, var_dv, model, iv_scaler, dv_scaler, **kwargs
        )
        # trained_models[year] = trained_model
        logs.append([year] + stats)

    columns = ["year"] + keys
    results = pd.DataFrame(logs, columns=columns)
    return results, trained_models, dv_scalers


def find_large_errors(y_test, y_pred, threshold):
    errors = abs(y_test - y_pred)
    large_errors = errors[errors > threshold]
    return large_errors


def get_pred_n_outliers(
    df,
    vars_dv,
    vars_iv,
    model,
    year=None,
    threshold_multiplier=3,
):
    # Filter data for the specified year
    if year is None:
        df_year = df.copy()
    else:
        df_year = df[df["year"] == year].reset_index(drop=True)

    # # Initialize and train the model

    # Predict on the filtered dataset
    X_test = df_year[vars_iv]
    df_year["y_pred"] = model.predict(X_test)
    y = df_year[vars_dv]

    # Calculate residuals
    df_year["residuals"] = y - df_year["y_pred"]

    # Statistical measures
    mean_residual = df_year["residuals"].mean()
    std_residual = df_year["residuals"].std()
    threshold = threshold_multiplier * std_residual

    # Tag outliers
    df_year["outliers"] = np.where(np.abs(df_year["residuals"]) > threshold, 1, 0)

    # Rename the prediction column
    df_year = df_year.rename(columns={"y_pred": f"{vars_dv}_pred"})

    # Adjust outliers to reflect the sign of the residuals
    df_year["outliers"] = df_year.apply(
        lambda row: row["outliers"] * np.sign(row["residuals"]), axis=1
    )

    return df_year


def get_pred_n_outliers_z_score(
    df,
    vars_dv,
    vars_iv,
    model,
    year=None,
    threshold_multiplier=1.96,
):
    # Filter data for the specified year
    if year is None:
        df_year = df.copy()
    else:
        df_year = df[df["year"] == year].reset_index(drop=True)

    # Initialize and train the model

    # Predict on the filtered dataset
    X_test = df_year[vars_iv]
    df_year["y_pred"] = model.predict(X_test)
    y = df_year[vars_dv]

    # Calculate residuals
    df_year["residuals"] = y - df_year["y_pred"]

    # Statistical measures
    mean_residual = df_year["residuals"].mean()
    std_residual = df_year["residuals"].std()
    threshold = threshold_multiplier * std_residual

    # Calculate Z-scores
    df_year["z_score"] = (df_year["residuals"] - mean_residual) / std_residual

    # Tag outliers based on Z-scores
    df_year["outliers"] = np.where(
        np.abs(df_year["z_score"]) > threshold_multiplier, 1, 0
    )

    # Rename the prediction column
    df_year = df_year.rename(columns={"y_pred": f"{vars_dv}_pred"})

    # Adjust outliers to reflect the sign of the residuals
    df_year["outliers"] = df_year.apply(
        lambda row: row["outliers"] * np.sign(row["residuals"]), axis=1
    )

    return df_year
