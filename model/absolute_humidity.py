import numpy as np

def absolute_humidity(T, RH):
    """
    Calculates absolute humidity in g/m³

    Inputs:
      T  - Air temperature in °C (float)
      RH - Relative humidity in % (float)

    Output:
      AH - Absolute humidity in g/m³ (float)
    """

    T = float(T)
    RH = float(RH)

    # Saturation vapor pressure (Magnus formula, hPa)
    P_sat = 6.112 * np.exp((17.67 * T) / (T + 243.5))

    # Actual vapor pressure (hPa)
    P_v = (RH / 100.0) * P_sat

    # Absolute humidity (g/m³)
    AH = (216.7 * P_v) / (T + 273.15)

    return AH