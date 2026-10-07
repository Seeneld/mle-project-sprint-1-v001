import pandas as pd
import yaml
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib

def preprocess():
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    
    df = pd.read_csv('data/cleaned_data.csv')
    
    X = df.drop(columns=[params['target_col']])
    y = df[params['target_col']]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=params['test_size'], 
        random_state=params['random_state']
    )
    
    cat_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
    num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
        ]
    )
    
    os.makedirs('data', exist_ok=True)
    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)
    y_train.to_csv('data/y_train.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(preprocessor, 'models/preprocessor.pkl')

if __name__ == '__main__':
    preprocess()