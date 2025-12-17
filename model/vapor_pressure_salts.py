import numpy as np
from model.solution_density import solution_density
from model.humrat import humrat
from model.svp_1 import svp_1

def vapor_pressure_salts(T_C, T_a, rh_a, salts, mass_fracs, p):
    ionParams = {
        'Li': {'xi': 181.9875, 'alpha': -0.3409, 'beta': 0.0301},
        'Ca': {'xi': 363.7876, 'alpha': -0.6849, 'beta': 0.1039},
        'Cl': {'xi': -181.8698, 'alpha': 0.0639, 'beta': 0.0003},
        'Mg': {'xi': 363.6704, 'alpha': -0.6195, 'beta': 0.1039},
        'NO3': {'xi': -181.6861, 'alpha': 0.1082, 'beta': -0.0174},
    }

    saltData = {
        'LiCl': {'M': 42.39, 'ions': [('Li', 1), ('Cl', 1)]},
        'CaCl2': {'M': 110.98, 'ions': [('Ca', 1), ('Cl', 2)]},
        'MgCl2': {'M': 95.3, 'ions': [('Mg', 1), ('Cl', 2)]},
        'CaNO32': {'M': 164.088, 'ions': [('Ca', 1), ('NO3', 2)]},
    }

    T_K = T_C + 273.15
    mass_fracs = np.clip(mass_fracs, 0.0, 0.999)
    massfrac_H2O = max(1e-6, 1.0 - np.sum(mass_fracs))

    molality = {}
    for salt, mf in zip(salts, mass_fracs):
        info = saltData[salt]
        moles = (mf * p['M_sol'] * 1000.0) / info['M']
        for ion, c in info['ions']:
            kg_H2O = massfrac_H2O * p['M_sol']
            m_i = (moles * c) / kg_H2O
            molality[ion] = molality.get(ion, 0.0) + m_i

    sum_xi_m = sum(ionParams[i]['xi'] * m for i, m in molality.items())
    sum_ab = sum(
        ionParams[i]['alpha'] * m**1.5 +
        ionParams[i]['beta'] * m**2
        for i, m in molality.items()
    )
    sum_m = sum(molality.values())

    temp_factor = (T_K / 273.15)**2
    ln_term = np.log(55.51 / (55.51 + sum_m))

    psat_w = (23.271 - (3879.198 / (T_K - 42.7356)))
    p_v = svp_1(T_a + 273.15)

    ln_p = psat_w - ((sum_ab / ((1 + sum_xi_m) * temp_factor)) - 1) * ln_term
    p_solution = np.exp(ln_p)

    P_kpa = p_solution / 1000.0
    w_sol = 0.62198 * P_kpa / (101.325 - P_kpa)

    rho_sol = solution_density(T_C, salts, mass_fracs)
    w_air = humrat(rh_a, T_a + 273.15)

    return p_solution, p_v, w_sol, w_air, rho_sol