import numpy as np

from model.air_density import air_density
from model.lpm_from_cfm import lpm_from_cfm
from model.run_hour_simulation import run_hour_simulation


def auto_select_cfm(
    T_a,
    rh_a,
    M_sol_initial,
    M_salts,
    salts,
    x_salts,
    t_final,
    cfm=None,
    lpm=None
):
    """
    Selects CFM automatically OR uses user-defined CFM & LPM.

    Modes:
    ------
    1. User-defined mode:
       If cfm and lpm are provided → run once and return result

    2. Auto-selection mode:
       If cfm or lpm is None → sweep CFM range and select best

    Returns:
    --------
    total_absorbed_water (kg), selected_cfm
    """

    # --------------------------------------------------
    # MODE 1: USER-DEFINED CFM & LPM
    # --------------------------------------------------
    if cfm is not None and lpm is not None:
        total_abs = run_hour_simulation(
            int(cfm),
            float(lpm),
            T_a,
            rh_a,
            M_sol_initial,
            M_salts,
            salts,
            x_salts,
            t_final
        )
        return float(total_abs), int(cfm)

    # --------------------------------------------------
    # MODE 2: AUTO-SELECTION
    # --------------------------------------------------
    cfm_list = np.arange(10000, 40001, 1000)

    best_cfm = int(cfm_list[0])
    best_abs = 0.0

    rho_air = air_density(T_a, rh_a * 100.0)

    for cfm_try in cfm_list:
        lpm_try = lpm_from_cfm(
            int(cfm_try),
            LbyG=1.2,
            rho_air=rho_air,
            rho_liq=1380.0
        )

        total_abs = run_hour_simulation(
            int(cfm_try),
            lpm_try,
            T_a,
            rh_a,
            M_sol_initial,
            M_salts,
            salts,
            x_salts,
            t_final
        )

        # Early exit if target achieved
        if total_abs >= 80.0:
            return float(total_abs), int(cfm_try)

        # Track best so far
        if total_abs > best_abs:
            best_abs = total_abs
            best_cfm = int(cfm_try)

    return float(best_abs), best_cfm