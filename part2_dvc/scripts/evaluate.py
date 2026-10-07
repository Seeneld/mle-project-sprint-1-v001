import pandas as pd
import yaml
import os
import json
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_model():
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    
    X_test = pd.read_csv('data/X_test.csv')
    y_test = pd.read_csv('data/y_test.csv').squeeze()
    
    pipeline = joblib.load('models/model.pkl')
    
    y_pred = pipeline.predict(X_test)
    
    metrics = {
        'mae': float(mean_absolute_error(y_test, y_pred)),
        'rmse': float(mean_squared_error(y_test, y_pred, squared=False)),
        'r2': float(r2_score(y_test, y_pred))
    }
    
    os.makedirs('cv_results', exist_ok=True)
    with open('cv_results/metrics.json', 'w') as fd:
        json.dump(metrics, fd, indent=4)

if __name__ == '__main__':
    evaluate_model()