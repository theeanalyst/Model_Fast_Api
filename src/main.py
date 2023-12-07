#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn
import numpy as np
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return "Sepsis Prediction App" 

## Load the model
model = joblib.load("src/rf_pipeline.joblib")

# Define a Pydantic model for the input data
class SepsisInput(BaseModel):
    PRG: float
    PL: float
    PR: float
    SK: float
    TS: float
    M11: float
    BD2: float
    Age: float
          
        
# Endpoint for predicting sepsis using a GET request
@app.post("/sepsis/predict")
async def predict_sepsis(PRG: float, PL: float, PR: float, SK: float, TS: float,
                         M11: float, BD2: float, Age: float):
    try:
        # Convert input data to a dictionary
        input_data = {
            'PRG': PRG,
            'PL': PL,
            'PR': PR,
            'SK': SK,
            'TS': TS,
            'M11': M11,
            'BD2': BD2,
            'Age': Age,  
        }


        # Convert input_data to DataFrame
        input_data_df = pd.DataFrame([input_data])

        # Use the loaded model to make predictions

        prediction= model.predict(input_data_df)[0]
        
        sepsis_status = "patient has sepsis" if prediction ==1 else "Patient does not have sepsis"
        
        # Return the prediction
        return {"prediction": sepsis_status}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import nest_asyncio

    nest_asyncio.apply()

    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="info")

