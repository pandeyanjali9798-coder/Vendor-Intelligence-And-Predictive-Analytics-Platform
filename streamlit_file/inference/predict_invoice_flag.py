import joblib
import pandas as pd
from pathlib import Path
Model_path = Path(__file__).parent.parent / "models" / "predict_flag_invoice.pkl"

def load_model(model_path: str = Model_path):
   """
   Load flag invoice prediction model
   """
   with open(model_path, "rb") as f:
        model = joblib.load(f)
   return model

def predict_flag_invoice(input_data):
    """
    predict flag invoice for new invoice :

    parameter
    ---------
    input_data : dict
    ---------

    return
    --------
    pd.dataframe with predict flag invoice
    """
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df["Predicted_flag"] = model.predict(input_df).round()
    return input_df

if __name__  == "__main__":
   Sample_data = {
      "Dollars": [18500,9000,3000,200]
   }
   prediction = predict_flag_invoice(Sample_data)
   print(prediction)
