import joblib
import pandas as pd

Model_path = "models/predict_freight_model.pkl"

def load_model(model_path: str = Model_path):
   """
   Load freight cost prediction model
   """
   with open(model_path, "rb") as f:
        model = joblib.load(f)
   return model

def predict_freight_cost(input_data):
    """
    predict freight cost for new invoice :

    parameter
    ---------
    input_data : dict
    ---------

    return
    --------
    pd.dataframe with predict freight cost
    """
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df["Predicted_freight"] = model.predict(input_df).round()
    return input_df

if __name__  == "__main__":
   Sample_data = {
      "Dollars": [18500,9000,3000,200]
   }
   prediction = predict_freight_cost(Sample_data)
   print(prediction)
   print(models.feature_names_in_)
