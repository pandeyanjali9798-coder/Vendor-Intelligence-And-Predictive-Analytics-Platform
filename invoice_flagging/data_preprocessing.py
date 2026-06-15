import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

def load_invoice_data():
    engine = create_engine("mysql+pymysql://root:Anjali%409798@127.0.0.1:3306/inventory_database")

    query = """
WITH purchase_agg AS(
SELECT 
p.PONumber,
COUNT(Distinct p.Brand) as total_brands,
SUM(p.Quantity)  as total_item_quantity,
SUM(p.Dollars)  as total_item_dollars,
AVG(
DATEDIFF(
     STR_TO_DATE(p.ReceivingDate, '%%Y-%%m-%%d'),
     STR_TO_DATE(p.PODate, '%%Y-%%m-%%d')
     )
)AS avg_receiving_delays
FROM purchases p
GROUP BY PONumber
)
SELECT
vi.PONumber,
vi.Quantity as invoice_quantity,
vi.Dollars as invoice_dollars,
vi.Freight,
DATEDIFF(
     STR_TO_DATE(vi.InvoiceDate, '%%Y-%%m-%%d'),
     STR_TO_DATE(vi.PODate, '%%Y-%%m-%%d')
     ) AS days_po_to_invoice,
DATEDIFF(
     STR_TO_DATE(vi.PayDate, '%%Y-%%m-%%d'),
     STR_TO_DATE(vi.InvoiceDate, '%%Y-%%m-%%d')
     ) AS days_to_pays,
pa.total_brands,
pa.total_item_quantity,
pa.total_item_dollars,
pa.avg_receiving_delays

FROM vendor_invoice vi
LEFT JOIN purchase_agg pa
 ON pa.PONumber = vi.PONumber
"""

    df = pd.read_sql(query,engine)
    engine.dispose()
    return df

def create_invoice_risk_label(row):
    #Invoice total mismatch with items-level total
    if(abs(row["invoice_dollars"] - row["total_item_dollars"]) >5):
        return 1
     #Abnormally high receiving delays
    if row["avg_receiving_delays"]>10:
        return 1

    return 0

def apply_labels(df):
    df["flag_invoice"] = df.apply(create_invoice_risk_label,axis=1)
    return df

def split_data(df,features,target):
    x = df[features]
    y = df[target]
    return train_test_split(x,y,test_size=0.2,random_state=42)

def scaled_features(x_train,x_test,scaled_path):
     scaled = StandardScaler()
     X_train_scaled = scaled.fit_transform(x_train)
     X_test_scaled = scaled.transform(x_test)

     joblib.dump(scaled,'models/scaler.pkl')
     return X_train_scaled, X_test_scaled
 