import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.stats.weightstats import DescrStatsW

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Data Insights Pro", layout="wide", initial_sidebar_state="expanded")

# CSS para estilo Premium (Bordes neón y fondos profundos)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00fbff !important; font-size: 32px; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #1f1f1f !important;
        border-radius: 20px;
        background-color: #0d0d0d;
        transition: 0.3s;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #00fbff !important;
        box-shadow: 0px 0px 15px rgba(0, 251, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("datos_masivos_examen.csv")
    return df

df = load_data()

# --- SIDEBAR: FILTROS INTERACTIVOS ---
with st.sidebar:
    st.title("🎛️ Controles")
    st.write("Filtra el catálogo en tiempo real")
    categoria_sel = st.multiselect("Seleccionar Categoría", options=df['categoria'].unique(), default=df['categoria'].unique())
    precio_range = st.slider("Rango de Precio", float(df['precio'].min()), float(df['precio'].max()), (float(df['precio'].min()), float(df['precio'].max())))
    
    st.divider()
    st.info("Este dashboard procesa 1,000 registros mediante análisis estadístico avanzado.")

# Filtrado de datos
df_filtrado = df[(df['categoria'].isin(categoria_sel)) & (df['precio'].between(precio_range[0], precio_range[1]))]

# --- CABECERA ---
st.title("🚀 Dashboard de Análisis Masivo")
st.markdown("### Catálogo Automatizado de Resultados Estadísticos")

# --- SECCIÓN 1: MÉTRICAS DINÁMICAS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    with st.container(border=True):
        st.metric("Media de Precio", f"${df_filtrado['precio'].mean():.2f}")
with c2:
    with st.container(border=True):
        st.metric("Mediana Stock", f"{df_filtrado['stock'].median():.0f}")
with c3:
    with st.container(border=True):
        st.metric("Moda Calificación", f"{df_filtrado['calificacion'].mode()[0]:.1f}")
with c4:
    with st.container(border=True):
        st.metric("Total Registros", f"{len(df_filtrado)}")

st.divider()

# --- SECCIÓN 2: VISUALIZACIÓN AVANZADA ---
t1, t2, t3 = st.tabs(["📊 Análisis de Frecuencias", "📈 Distribución y Acumulados", "📑 Tabla Maestra"])

with t1:
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.container(border=True):
            st.write("**Frecuencia Absoluta por Categoría**")
            fig_bar = px.bar(df_filtrado['categoria'].value_counts().reset_index(), 
                             x='categoria', y='count', 
                             color='count', color_continuous_scale='Viridis',
                             template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with col_right:
        with st.container(border=True):
            st.write("**Frecuencia Relativa (Participación)**")
            fig_pie = px.pie(df_filtrado, names='categoria', hole=0.5,
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)

with t2:
    with st.container(border=True):
        st.write("**Polígono de Frecuencias y Curva Acumulada**")
        
        # Procesamiento para Polígono
        bins = 15
        counts, bin_edges = np.histogram(df_filtrado['precio'], bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        cum_sum = counts.cumsum()

        fig_mix = go.Figure()
        # Línea de Polígono
        fig_mix.add_trace(go.Scatter(x=bin_centers, y=counts, mode='lines+markers', 
                                     name='Frec. Absoluta', line=dict(color='#00fbff', width=4)))
        # Línea de Acumulada
        fig_mix.add_trace(go.Scatter(x=bin_centers, y=cum_sum, mode='lines', 
                                     name='Frec. Acumulada', fill='tozeroy', line=dict(color='#ff007c')))
        
        fig_mix.update_layout(template="plotly_dark", xaxis_title="Rangos de Precio", yaxis_title="Cantidad")
        st.plotly_chart(fig_mix, use_container_width=True)

with t3:
    st.write("Listado detallado basado en filtros aplicados:")
    st.dataframe(df_filtrado.style.background_gradient(subset=['calificacion'], cmap='Blues'), use_container_width=True)

# Footer
st.caption("Generado automáticamente para Examen Práctico 2026 | Tecnología Streamlit + Plotly")
