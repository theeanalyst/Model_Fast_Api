# import libraries
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException,Query

app = FastAPI()

###create home
@app.get('/')
def home():
    return{'message':'Welcome to Sepsis Prediction Using Fastapi'}

## Load the model
model = joblib.load("src/rf_pipeline.joblib")  
        
# Endpoint for predicting sepsis using a GET request
@app.post("/predict")
def predict_sepsis(
        PRG: int = Query(..., description="Plasma_glucose"),
        PL: int = Query(..., description="Blood_Work_R1"),
        PR: int = Query(..., description="Blood_Pressure"), 
        SK: int = Query(..., description="Blood_Work_R2"),
        TS: int = Query(..., description="Blood_Work_R3"),
        M11: float = Query(..., description="BMI"),
        BD2: float = Query(..., description="Blood_Work_R4"),
        Age: int = Query(..., description="Age")
):
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
        
        sepsis_status = "patient has sepsis" if prediction == 1 else "Patient does not have sepsis"
        
        # Return the prediction
        return {"prediction": sepsis_status}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import nest_asyncio

    nest_asyncio.apply()

    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="info")