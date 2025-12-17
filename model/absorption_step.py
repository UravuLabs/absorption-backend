import numpy as np
from model.dydx_gen1 import dydx_gen1
from model.vapor_pressure_salts import vapor_pressure_salts
from model.humrat import humrat
from model.svp_1 import svp_1

def absorption_step(cfm, lpm, rho_sol, x_total, T_a, rh_a, T_s, salts, M_salts, p):

    rho_a = 1.164
    A_t = 300.0
    M_w = 18.02

    m_a = cfm * 0.02832 / 60.0 * rho_a
    m_s_i = rho_sol * lpm / (1000 * 60)

    M_ratio = M_salts / np.sum(M_salts)

    w_a = humrat(rh_a, T_a + 273.15)
    y_ai = w_a / (1 + w_a)

    x_o = x_total
    for _ in range(30):
        x_avg = 0.5 * (x_total + x_o)
        mf = x_avg * M_ratio

        slope = dydx_gen1(x_avg, T_s, T_a, rh_a, salts, M_ratio, p)
        k = 1 / (1 + slope)

        _, _, w_film, _, _ = vapor_pressure_salts(T_s, T_a, rh_a, salts, mf, p)
        y_film = w_film

        m_v = k * A_t * (y_ai - y_film)
        m_s_out = m_s_i + m_v
        x_o = (x_total * m_s_i) / m_s_out

    return max(0.0, m_v * 3600)