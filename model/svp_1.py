import math

def svp_1(T):
    """
    Saturation vapor pressure using Goff & Gratch (1946)

    Input:
        T  - Temperature in Kelvin

    Output:
        SVP - Saturation vapor pressure (Pa)
    """
    Ts = 373.15
    Ps = 101324.6

    log10SVP = (
        -7.90298 * (Ts / T - 1)
        + 5.02808 * math.log10(Ts / T)
        - 1.3816e-7 * (10 ** (11.344 * (1 - T / Ts)) - 1)
        + 8.1328e-3 * (10 ** (3.49149 * (1 - Ts / T)) - 1)
        + math.log10(Ps)
    )

    return 10 ** log10SVP