import numpy as np
import pandas as pd

from model.absolute_humidity import absolute_humidity
from model.auto_select_cfm import auto_select_cfm


def run_absorption_simulation(
    weather_df,
    user_cfm=None,
    user_lpm=None,
    M_sol_initial=500.0,
    salts=None,
    x_salts=None,
    t_final=1
):
    """
    Runs absorption simulation for provided weather data

    Inputs:
        weather_df : pandas DataFrame
            Required columns:
            - 'T'  : dry bulb temperature (°C)
            - 'RH' : relative humidity (0–1)

        user_cfm : float | None
        user_lpm : float | None
            If provided → fixed operation
            If None → auto-selection used

    Returns:
        dict (JSON-serializable)
    """

    if salts is None:
        salts = ['CaCl2', 'LiCl', 'MgCl2', 'CaNO32']

    if x_salts is None:
        x_salts = np.array([0.4, 0.0, 0.04, 0.12])

    M_salts = M_sol_initial * x_salts
    nData = len(weather_df)

    hourly_absorption = np.zeros(nData)
    AH_values = np.zeros(nData)
    cfm_used = np.zeros(nData)

    for i in range(nData):
        T_a = float(weather_df.iloc[i]['T'])
        rh_a = float(weather_df.iloc[i]['RH'])

        AH_values[i] = absolute_humidity(T_a, rh_a * 100.0)

        abs_hr, best_cfm = auto_select_cfm(
            T_a,
            rh_a,
            M_sol_initial,
            M_salts,
            salts,
            x_salts,
            t_final,
            cfm=user_cfm,   # ✅ now defined
            lpm=user_lpm
        )

        hourly_absorption[i] = abs_hr
        cfm_used[i] = best_cfm

    return {
        "hourly_absorption": hourly_absorption.tolist(),
        "absolute_humidity": AH_values.tolist(),
        "cfm_used": cfm_used.tolist(),
        "total_water_absorbed": float(np.sum(hourly_absorption))
    }