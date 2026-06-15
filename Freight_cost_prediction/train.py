
import joblib
from pathlib import Path

from data_preprocessing import load_vendor_invoice_data, prepare_features, split_data
from model_evalution import (
    train_linear_regression,
    train_decision_tree,
    train_random_forest,
    evaluate_model
)

def main():
    db_path = "mysql+pymysql://root:Anjali%409798@127.0.0.1:3306/inventory_dataset_db"
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    # load dataset
    df = load_vendor_invoice_data(db_path)

    # prepare dataset
    x ,y = prepare_features(df)
    x_train,x_test,y_train,y_test = split_data(x,y)

    # model train
    lr_model = train_linear_regression(x_train,y_train)
    dt_model = train_decision_tree(x_train,y_train)
    rf_model =  train_random_forest(x_train,y_train)
    # select best model(lowest mae)
    result = []
    result.append(evaluate_model(lr_model,x_test,y_test,'Linear Regression'))
    result.append(evaluate_model(dt_model,x_test,y_test,'Decision Tree Regression'))
    result.append(evaluate_model(rf_model,x_test,y_test,'random forest Regression'))

    best_model_info = min(result, key=lambda x:x['mae'])
    best_model_name = best_model_info['model_name']

    best_model = {
        "Linear Regression" : lr_model,
        "Decision Tree ": dt_model,
        "Random Forest" : rf_model
     }[best_model_name]

    #save best model
    model_path = model_dir / "predict_freight_model.pkl"
    joblib.dump(best_model,model_path)

    print(f"\Best model saved: {best_model_name}")
    print(f"model path:{model_path}")

if __name__ == "__main__":
   main()