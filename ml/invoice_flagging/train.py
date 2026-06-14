from model_evaluation import train_random_forest, evaluate_model
import joblib
from data_preprocessing import load_invoice_data, apply_labels, split_data, scaled_features

features = ['Freight','invoice_dollars','invoice_quantity','total_item_dollars','total_item_quantity']
target = 'flag_invoice'

def main():
 
   #load data
   df = load_invoice_data()
   df = apply_labels(df)

   #prepare data
   X_train, X_test, y_train, y_test = split_data(df , features,target)
   X_train_scaled, X_test_scaled = scaled_features(X_train,X_test,'models/scaler.pkl')

   #train model
   grid_search = train_random_forest(X_train_scaled,y_train)

   #evaluate model
   evaluate_model(
    grid_search.best_estimator_,
    X_test_scaled,
    y_test,
    " Random Forest Classifier"
   )

   #save best model 
   joblib.dump(grid_search.best_estimator_,"models/predict_flag_invoice.pkl")


if __name__== "__main__":
  main()