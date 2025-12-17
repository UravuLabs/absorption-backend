from model.svp_1 import svp_1

def humrat(rh, t):
    """
    Humidity ratio

    Inputs:
        rh - relative humidity (fraction 0–1)
        t  - temperature in Kelvin
    """
    p_sat = svp_1(t)
    p_v = rh * p_sat

    return 0.62198 * p_v / (101325 - p_v)