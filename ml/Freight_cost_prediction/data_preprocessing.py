import pandas as pd
import numpy as  np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split

def load_vendor_invoice_data(db_path):
   """
   Loading the data from sql.
   """
   engine = create_engine(db_path)
   query = "Select *From vendor_invoice"
   df = pd.read_sql(query,engine)
   return df

def prepare_features(df: pd.DataFrame):
   """
   Select features and the target variable.
   
   """
   x = df[["Dollars"]]
   y = df['Freight']
   return x,y


def split_data(x,y,test_size=0.2,random_state=42):
    """
    split and train the dataset.

    """
    return train_test_split(x,y,test_size=test_size,random_state=random_state)

 