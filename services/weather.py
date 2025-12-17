import pandas as pd
from meteostat import Point, Hourly


def load_weather_by_location(lat: float, lon: float) -> pd.DataFrame:
    location = Point(lat, lon)
    data = Hourly(location).fetch()

    if data.empty:
        return pd.DataFrame()

    df = pd.DataFrame()
    df["T"] = data["temp"]
    df["RH"] = data["rhum"] / 100.0

    return df.reset_index(drop=True)