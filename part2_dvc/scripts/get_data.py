import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml

def get_data():
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    
    load_dotenv()
    engine = create_engine(
        f"postgresql://{os.getenv('DB_DESTINATION_USER')}:{os.getenv('DB_DESTINATION_PASSWORD')}@"
        f"{os.getenv('DB_DESTINATION_HOST')}:{os.getenv('DB_DESTINATION_PORT')}/{os.getenv('DB_DESTINATION_NAME')}"
    )
    
    df = pd.read_sql("SELECT * FROM cleaned_flats", engine)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/cleaned_data.csv', index=False)

if __name__ == '__main__':
    get_data()