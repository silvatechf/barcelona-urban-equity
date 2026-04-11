import pandas as pd
import logging

class DataCleaner:
    """Vectorized cleaning and validation for Barcelona Social & Housing Data."""
    
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        logging.info("--- Data Integrity & Cleaning Phase ---")
        
        # 1. Identificação de Nulos (Requisito Barcelona Activa)
        null_report = df.isnull().sum()
        logging.info(f"Columns found in CSV: {df.columns.tolist()}")
        logging.info(f"Null values per column before cleaning:\n{null_report}")
        
        # 2. Tratamento Explícito
        # Removemos duplicatas e garantimos que o preço (nossa variável alvo) exista
        df = df.drop_duplicates()
        if 'rent_price' in df.columns:
            df = df.dropna(subset=['rent_price'])
        
        # 3. Transformação de Tipos (Dinâmica)
        # Em vez de colunas fixas, tentamos converter tudo que for numérico
        # Isso evita o KeyError se mudarmos os nomes das colunas sociais
        cols_to_convert = [
            'rent_price', 'sq_meters', 'lat', 'lon', 
            'social_vulnerability', 'green_mobility_access', 'air_pollution_index'
        ]
        
        for col in cols_to_convert:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 4. Finalização
        df = df.dropna() # Remove qualquer linha que falhou na conversão numérica
        logging.info(f"Cleaning complete. Valid rows: {len(df)}")
        
        return df