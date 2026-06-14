import streamlit as st
import pandas as pd
import numpy as np
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_flag_invoice

#------------------------------------------
# Page configuration
#------------------------------------------
st.set_page_config(
     page_title="Vendor Invoice Intelligence Portal",
     page_icon="📦",
     layout="wide"
)

#------------------------------------------
# Header section
#------------------------------------------
st.markdown("""
# 📦 Vendor Invoice Intelligence Portal
### AI-driven Freight Cost Prediction and Invoice Risk Flagging

This internal analytics portal leverages machine learning to
- Forecast Freight Cost accurately
- Detect risk and abnormal vendor invoices
- Reduce financial leakage and manual workload
""")

st.divider()

#-------------------------------------------
#Sidebar
#-------------------------------------------

st.sidebar.title("🔍Model Selection")
selected_model = st.sidebar.radio(
  "Choose Prediction Module",
  [ 
    "Freight cost prediction",
    "Invoice Manual Approval Flag"
  ]
)
st.sidebar.markdown("""
---
**Business Impact**
- 📉Improve cost forecasting
- 🧾Reduce invoice fraud and anomalies
- ⚙️Faster finance operation
""")

#------------------------------------------
# Freight cost prediction 
#------------------------------------------
if selected_model == "Freight cost prediction":
     st.subheader("🚚Freight Cost Prediction")

     st.markdown("""
        **Objective:**
        Predict the freight cost for a vendor invoice using **Invoice Dollars**
        for support budgeting, forecasting and vendor negotiation.
        """)

     with st.form("freight_form"):
          Dollars = st.number_input(
           "Invoice Dollars",
           min_value = 1.0,
           value=18500.0,
          )
          sumbit_freight = st.form_submit_button("💰Predicte freight cost")

          if sumbit_freight:
           input_data = {
             "Dollars": [Dollars]
           }
           prediction = predict_freight_cost(input_data)["Predicted_freight"]
           st.success("Prediction completed successfully.")

           st.metric(
             label="📊 Estimate Freight cost",
             value=f"💲{prediction[0]:,.2f}"
            )

#--------------------------------------------
# Invoice flag prediction
#--------------------------------------------
else:
    st.subheader("✍️ Invoice Manual approval prediction")

    st.markdown("""
        **Objective:**
        Predict whether a vendor invoice should be **flagged for manual approval**
        Based on abnormal cost, freight, and delivery patterns.
        """)         
    
    with st.form("invoice_flag_form"):
         col1, col2, col3 = st.columns(3)

         with col1:
          invoice_quantity = st.number_input(
           "Invoice_Quantity",
           min_value = 1,
           value=50
          )
          Freight = st.number_input(
            "Freight Cost",
             min_value=0.0,
             value=1.75
          )
          
         with col2:
          invoice_dollars = st.number_input(
           "Invoice Dollars",
           min_value = 1.0,
           value=352.95
          )
          total_item_quantity= st.number_input(
            "Total item quantity",
           min_value=1,
           value=162
          )

         with col3:
           total_item_dollars = st.number_input(
            "total item Dollars",
            min_value = 1.0,
            value=2476.0
          )
         sumbit_flag = st.form_submit_button("🧠Evaluate invoice risk")

         if sumbit_flag:
            input_data = {
              "invoice_quantity":[invoice_quantity],
              "invoice_dollars": [invoice_dollars],
              "Freight":[Freight],
              "total_item_quantity": [total_item_quantity],
              "total_item-dollars": [total_item_dollars]
            }

            flag_prediction= predict_flag_invoice(input_data)["Predicted_flag"]
            is_flagged = bool(flag_prediction[0])

            if is_flagged:
                st.error("✍️Invoice required **Manual approval**")
            else:
                st.success("✅ Invoice is **Safe for Auto-approval**")
   