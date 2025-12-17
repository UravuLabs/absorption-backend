import numpy as np
from model.vapor_pressure_salts import vapor_pressure_salts
from model.absorption_step import absorption_step

def run_hour_simulation(cfm, lpm, T_a, rh_a,
                        M_sol_initial, M_salts, salts, x_salts, t_final):

    M_sol = M_sol_initial
    water_vec = []

    for _ in range(int(t_final)):
        total_x = np.sum(M_salts) / M_sol
        p = {'M_sol': M_sol}

        _, _, _, _, rho_sol = vapor_pressure_salts(
            T_a + 2, T_a, rh_a, salts, x_salts, p)

        w = absorption_step(
            cfm, lpm, rho_sol, total_x,
            T_a, rh_a, T_a + 2, salts, M_salts, p)

        M_sol += w
        water_vec.append(w)

    return np.sum(water_vec)