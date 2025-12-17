from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from geopy.geocoders import Nominatim  # <- for converting location names
from model.main_absorption_simulation import run_absorption_simulation
from services.weather import load_weather_by_location

app = FastAPI(title="Water Absorption API", version="1.0.0")

# ---- CORS Middleware ----
origins = [
    "https://musical-jelly-d9a6cc.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    location: str
    month: int  # 1-12
    cfm: float | None = None
    lpm: float | None = None
    auto_mode: bool = True
    M_sol_initial: float = 500.0
    t_final: int = 1


geolocator = Nominatim(user_agent="water_absorption_app")


@app.post("/simulate")
def simulate(req: SimulationRequest):
    # Convert location name to lat/lon
    loc = geolocator.geocode(req.location)
    if not loc:
        raise HTTPException(status_code=400, detail="Location not found")

    weather_df = load_weather_by_location(loc.latitude, loc.longitude)
    if weather_df.empty:
        raise HTTPException(status_code=400, detail="Weather data unavailable")

    results = run_absorption_simulation(
        weather_df=weather_df,
        M_sol_initial=req.M_sol_initial,
        t_final=req.t_final,
        user_cfm=req.cfm,
        user_lpm=req.lpm,
        auto_mode=req.auto_mode
    )

    hourly = np.array(results["hourly_absorption"])
    monthly = hourly.reshape(12, -1).sum(axis=1)

    return {
        "monthly_water_absorption": monthly.tolist(),
        "hourly_water_absorption": hourly.tolist(),
        "cfm_used": results["cfm_used"],
        "total_water_absorbed": results["total_water_absorbed"]
    }