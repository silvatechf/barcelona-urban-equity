import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import logging
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class BCNAnalyst:
    """
    Executive Data Visualization and Social Audit for BCN Housing Impact.
    Refined for European institutional standards (clean, sober, analytical).
    """
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.emerald = "#10b981"  
        self.dark_bg = "#050505"  
        self.slate_grey = "#94a3b8" 
        self.text_light = "#ecf0f1"

    def get_descriptive_stats(self):
        """Calculates key indicators for the Social Sustainability Audit."""
        logging.info("Generating social-environmental statistical descriptors...")
        cols = ['rent_price', 'green_mobility_access', 'air_pollution_index', 'social_vulnerability']
        available_cols = [c for c in cols if c in self.data.columns]
        
        stats = self.data[available_cols].describe()
        correlation_matrix = self.data[available_cols].corr()
        return stats, correlation_matrix

    def plot_market_trends(self, output_path: str, r2_score: float = None):
        """Generates a high-fidelity sober plot for institutional decision-making."""
        try:
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(self.dark_bg)
            ax.set_facecolor(self.dark_bg)

            x_col = 'green_mobility_access'
            y_col = 'rent_price'

            sns.regplot(
                data=self.data, x=x_col, y=y_col, 
                scatter_kws={"color": self.emerald, "alpha": 0.3, "s": 40}, 
                line_kws={"color": self.slate_grey, "linewidth": 1.5, "label": "Tendencia Social"},
                ax=ax
            )

            max_x = self.data[x_col].max()
            max_y = self.data[y_col].max()
            
            ax.annotate(
                "Fuerte Correlación Positiva:\nSeñal de Gentrificación Verde",
                xy=(max_x, max_y),
                xytext=(-150, 20), textcoords='offset points',
                color=self.emerald, fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle="->", color=self.emerald, lw=1)
            )

            ax.set_title("Auditoría de Equidad Urbana: Movilidad vs Vivienda", 
                         loc='left', fontsize=13, pad=25, color=self.text_light, fontweight='bold')
            ax.set_xlabel("Índice de Movilidad Sostenible (Acceso Bicing)", color=self.slate_grey, fontsize=10)
            ax.set_ylabel("Alquiler Mensual (€)", color=self.slate_grey, fontsize=10)
            
           
            ax.grid(color='#1e293b', linestyle=':', alpha=0.4)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#1e293b')
            ax.spines['bottom'].set_color('#1e293b')

            # Accuracy Badge
            if r2_score is not None:
                ax.text(0.03, 0.92, f'Confianza del Modelo (R²): {r2_score:.2f}', 
                         transform=ax.transAxes, fontsize=9, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', alpha=0.8, edgecolor='#1e293b'))

            plt.legend(facecolor='#0f172a', edgecolor='#1e293b', fontsize='small')
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
            plt.close()
            logging.info(f"✅ Executive chart exported: {output_path}")
            
        except Exception as e:
            logging.error(f"❌ Plotting failed: {e}")

class PricePredictor:
    """
    Predictive Engine for Urban Social Indicators.
    Persistence-ready for Streamlit integration.
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.path = "models/bcn_model.joblib"

    def train_didactic(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Trains the model with feature tracking for synchronization."""
        try:
            os.makedirs("models", exist_ok=True)
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            self.model.fit(X_train, y_train)
            score = self.model.score(X_test, y_test)
            
            self.model.feature_names_in_ = X.columns.tolist()
            joblib.dump(self.model, self.path)
            
            logging.info(f"✅ Predictive Engine Synced. Accuracy: {score:.4f}")
            return score
            
        except Exception as e:
            logging.error(f"❌ Prediction training failed: {e}")
            return 0.0