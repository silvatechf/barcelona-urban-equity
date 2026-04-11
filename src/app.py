import streamlit as st
import joblib
import pandas as pd
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="BCN Urban Equity Audit", page_icon="🌍", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .main { background-color: #050505; color: #ecf0f1; font-family: 'Inter', sans-serif; }
    
    /* FIX: Sidebar Sliders & Labels to Emerald */
    .stSlider [data-baseweb="typography"], div[data-testid="stThumbValue"] { 
        color: #10b981 !important; 
        font-weight: 600 !important;
    }
    .st-at { background-color: #10b981 !important; } /* Slider color */

    /* Minimalist Alert Banner */
    .minimal-alert {
        border-left: 4px solid #10b981;
        background-color: #0f172a;
        padding: 15px 20px;
        margin-bottom: 30px;
        font-size: 0.95rem;
        color: #10b981;
        font-weight: 500;
    }

    /* Decision-Support Cards */
    .briefing-card {
        background-color: #0f172a; 
        border: 1px solid #1e293b;
        padding: 24px;
        border-radius: 14px;
        height: 100%;
    }

    .card-title {
        color: #10b981;
        font-weight: 800;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    
    .card-text { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }
    
    /* Metrics & Sidebar Styling */
    [data-testid="stMetricValue"] { color: #10b981; font-weight: 800; font-size: 2.2rem; }
    .stMetric { background-color: #0a0a0a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; }
    .stSidebar { background-color: #0a0a0a !important; border-right: 1px solid #1e293b; }
    
    .map-legend {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 8px;
        display: flex;
        justify-content: space-around;
        background: #0f172a;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    # --- HEADER ---
    st.title("🌍 Auditoría de Equidad Urbana - Barcelona")
    
    st.markdown('<div class="minimal-alert"><b>SEÑAL DE AUDITORÍA:</b> Alta correlación detectada entre infraestructura sostenible y estrés habitacional.</div>', unsafe_allow_html=True)

    # ---  SECTION 1: STRATEGIC BRIEFING ---
    briefing_path = "dist/executive_briefing.txt"
    if os.path.exists(briefing_path):
        with open(briefing_path, "r", encoding="utf-8") as f:
            content = f.read()
            parts = [p.strip() for p in content.split('\n') if p.strip()]
            
            def clean_briefing_text(text):
                """Cleans AI prefix artifacts like '0.96).' or 'Paragraph 1:'"""
                import re
                text = re.sub(r'^[\d\.\)]+\s*', '', text) 
                if ":" in text and len(text.split(":")[0]) < 25: 
                    return text.split(":", 1)[1].strip()
                return text

            c1, c2, c3 = st.columns(3)
            titles = ["🎯 Diagnóstico Primario", "📊 Evidencia Estadística", "💡 Recomendación Política"]
            for i, col in enumerate([c1, c2, c3]):
                with col:
                    if i < len(parts):
                        cleaned_content = clean_briefing_text(parts[i])
                        st.markdown(f'''
                            <div class="briefing-card">
                                <div class="card-title">{titles[i]}</div>
                                <div class="card-text">{cleaned_content}</div>
                            </div>
                        ''', unsafe_allow_html=True)
    else:
        st.info("Esperando auditoría...")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 2: SIDEBAR ---
    st.sidebar.image("https://img.icons8.com/fluency/96/city-buildings.png", width=60)
    st.sidebar.header("Parámetros del Modelo")

    m2 = st.sidebar.slider("Superficie de Vivienda (m²)", 30, 200, 70)
    green_access = st.sidebar.slider("Índice de Movilidad Verde", 0.0, 15.0, 8.0)
    vulnerability = st.sidebar.slider("Vulnerabilidad Social", 1, 10, 5)

    model_path = "models/bcn_model.joblib"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        X_input = pd.DataFrame([[green_access, m2, vulnerability]], columns=["green_mobility_access", "sq_meters", "social_vulnerability"])
        prediction = model.predict(X_input)[0]
        st.sidebar.markdown("---")
        st.sidebar.metric(label="ALQUILER ESTIMADO", value=f"€ {prediction:,.0f}", delta="Estrés Habitacional", delta_color="inverse")
    
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📈 Perfil de Riesgo: Gentrificación")
        analysis_img = "dist/bcn_market_analysis.png"
        if os.path.exists(analysis_img):
            st.image(analysis_img, use_container_width=True)

    with col2:
        st.markdown("### 🗺️ Mapa de Distribución Geoespacial")
        map_path = "dist/bcn_interactive_map.html"
        if os.path.exists(map_path):
            with open(map_path, "r", encoding="utf-8") as f:
                html_data = f.read()
                components.html(html_data, height=450, scrolling=False)
            st.markdown('''
                <div class="map-legend">
                    <span>🟢 Hub de Movilidad</span> <span>⚪ Indicador</span> <span>☁️ Radio de Impacto</span>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Barcelona Urban Equity & Sustainability Audit | Framework v1.0")

if __name__ == "__main__":
    main()