import numpy as np
from model.vapor_pressure_salts import vapor_pressure_salts

def dydx_gen1(x_g, T_s, T_a, rh_a, salts, M_salts_ratio, p):
    delta = 0.001

    mf_l = np.maximum(x_g - delta, 0.0) * M_salts_ratio
    mf_r = np.maximum(x_g + delta, 0.0) * M_salts_ratio

    _, _, w_l, _, _ = vapor_pressure_salts(T_s, T_a, rh_a, salts, mf_l, p)
    _, _, w_r, _, _ = vapor_pressure_salts(T_s, T_a, rh_a, salts, mf_r, p)

    y_l = w_l / (1 + w_l)
    y_r = w_r / (1 + w_r)

    return (y_r - y_l) / (-2 * delta)