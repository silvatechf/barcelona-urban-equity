import sqlite3
import pandas as pd
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class BcnDatabase:
    """Relational interface for BCN Smart Housing Audit."""
    
    def __init__(self):
        self.db_name = os.getenv("DB_NAME", "data/bcn_audit.db")
        
        
        os.makedirs(os.path.dirname(self.db_name), exist_ok=True)
        
    def save_full_audit(self, df: pd.DataFrame, table_name: str = "housing_audit"):
        """
        Saves the entire cleaned DataFrame into a relational table.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                logging.info(f" SQL: Database '{self.db_name}' updated.")
        except Exception as e:
            logging.error(f" Database Error (Save): {e}")

    def get_top_districts_report(self):
        """
        Demonstrates SQL Query skills (SELECT, GROUP BY, ORDER BY).
        """
        query = """
            SELECT 
                district, 
                COUNT(*) as properties_audited,
                AVG(rent_price) as avg_rent,
                MAX(rent_price) as max_rent
            FROM housing_audit 
            GROUP BY district 
            ORDER BY avg_rent DESC
        """
        try:
            
            with sqlite3.connect(self.db_name, timeout=10) as conn:
                return pd.read_sql_query(query, conn)
        except Exception as e:
            logging.error(f"❌ Database Error (Query): {e}")
            return pd.DataFrame()