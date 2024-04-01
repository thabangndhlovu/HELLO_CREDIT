# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.regression import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("model")

# Create input/output pydantic models
input_model = create_model("model_input", **{'oper_margin': 59.86275863647461, 'tot_debt_to_tot_eqy': 45.14314651489258, 'tot_debt_to_ebitda': 4.419726371765137, 'ebitda_to_tot_int_exp': 3.0266149044036865, 'return_on_asset': 3.772739887237549, 'asset_turnover': 0.10089917480945587})
output_model = create_model("model_output", prediction=3.5)


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
