import math

def air_density(T, RH):
    """
    Moist air density (kg/m³)

    Inputs:
        T  - °C
        RH - % (0–100)
    """
    R_d = 287.058
    R_v = 461.495

    T_k = T + 273.15
    RH_frac = RH / 100.0

    p_ws = 610.94 * math.exp(17.625 * T / (T + 243.04))
    p_w = RH_frac * p_ws
    p_atm = 101325
    p_dry = p_atm - p_w

    return (p_dry / (R_d * T_k)) + (p_w / (R_v * T_k))