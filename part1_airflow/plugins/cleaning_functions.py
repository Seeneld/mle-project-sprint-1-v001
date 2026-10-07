import pandas as pd

def remove_duplicates(df):
    return df.drop_duplicates()

def handle_missing_values(df):
    df = df.dropna(subset=['price', 'total_area', 'rooms', 'floor'])
    df['ceiling_height'] = df['ceiling_height'].fillna(df['ceiling_height'].median())
    df['kitchen_area'] = df['kitchen_area'].fillna(df['kitchen_area'].median())
    df['living_area'] = df['living_area'].fillna(df['living_area'].median())
    return df

def remove_outliers(df):
    df = df[
        (df['price'] > 0) & 
        (df['total_area'] > 0) & 
        (df['floor'] > 0) & 
        (df['rooms'] >= 0) &
        (df['rooms'] <= 10) &
        (df['price'] < df['price'].quantile(0.99)) &
        (df['total_area'] < df['total_area'].quantile(0.99))
    ]
    return df

def clean_data(df):
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    return df