def solution_density(T_C, salts, mass_fracs):
    rho_w = 1000.0 * (
        1.0 - ((T_C + 288.9414) /
        (508929.2 * (T_C + 68.12963))) *
        (T_C - 3.9863)**2
    )

    density_increments = {
        'LiCl': 500.0,
        'CaCl2': 800.0,
        'MgCl2': 750.0,
        'CaNO32': 600.0
    }

    temp_factor = 1.0 - 0.00025 * (T_C - 20.0)

    delta_rho = 0.0
    for salt, mf in zip(salts, mass_fracs):
        if salt in density_increments:
            delta_rho += density_increments[salt] * mf

    return rho_w + delta_rho * temp_factor