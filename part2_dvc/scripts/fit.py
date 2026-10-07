import pandas as pd
import yaml
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

def fit_model():
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    
    X_train = pd.read_csv('data/X_train.csv')
    y_train = pd.read_csv('data/y_train.csv').squeeze()
    
    preprocessor = joblib.load('models/preprocessor.pkl')
    
    model = RandomForestRegressor(
        n_estimators=params['n_estimators'],
        max_depth=params['max_depth'],
        random_state=params['random_state'],
        n_jobs=-1
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    pipeline.fit(X_train, y_train)
    
    joblib.dump(pipeline, 'models/model.pkl')

if __name__ == '__main__':
    fit_model()