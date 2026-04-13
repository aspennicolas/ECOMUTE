from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from src.models.trips import TripInput
from src.logger import logger

router = APIRouter(tags=["ML Prediction"])

#Global variable to hold the loaded model
model = None

#Load the model at startup
MODEL_PATH = 'src/ml/trip_predictor.joblib'

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    logger.warning(f"Model file not found at {MODEL_PATH}")


@router.post("/predict/duration")
def predict_duration(trip: TripInput):
    if not model:
        logger.error("Prediction requested but model is not loaded")
        raise HTTPException(status_code=503, detail="Model not available. Please try again later.")
    #Sklearn expects a 2D array for features, so we create a DataFrame with one row.
    features = pd.DataFrame({
        'distance_km': [trip.distance_km],
        'battery_level': [trip.battery_level]
    })

    prediction = model.predict(features)[0] #Get the single prediction value
    logger.info(f"Prediction made: distance={trip.distance_km}km → {round(prediction, 1)} min")
    return {
        "distance_km": trip.distance_km,
        "estimated_minutes": round(prediction, 1) #Round to 1 decimal place for readability
    }