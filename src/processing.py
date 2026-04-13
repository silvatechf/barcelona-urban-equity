import pandas as pd
import logging

class DataCleaner:
    """Vectorized cleaning and validation for Barcelona Social & Housing Data."""
    
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        logging.info("--- Data Integrity & Cleaning Phase ---")
        
    
        null_report = df.isnull().sum()
        logging.info(f"Columns found in CSV: {df.columns.tolist()}")
        logging.info(f"Null values per column before cleaning:\n{null_report}")
        
       
        df = df.drop_duplicates()
        if 'rent_price' in df.columns:
            df = df.dropna(subset=['rent_price'])
        
        
        cols_to_convert = [
            'rent_price', 'sq_meters', 'lat', 'lon', 
            'social_vulnerability', 'green_mobility_access', 'air_pollution_index'
        ]
        
        for col in cols_to_convert:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        
        df = df.dropna() 
        logging.info(f"Cleaning complete. Valid rows: {len(df)}")
        
        return df
