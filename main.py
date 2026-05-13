import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Ventas Cafeteria", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: #d4a373; }
    h1, h2, h3 { color: #faedcd !important; }
    [data-testid="stMetricValue"] { color: #faedcd !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #d4a373 !important;
        border-radius: 15px;
        background-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

df = pd.read_csv("ventas_cafeteria.csv")

st.title("Sistema de Monitoreo: Cafeterias Premium")
st.divider()

with st.sidebar:
    st.header("Resumen del Dia")
    st.metric("Ventas Totales", f"${df['Precio'].sum():,.0f}")
    st.metric("Promedio Ticket", f"${df['Precio'].mean():.2f}")
    st.metric("Espera Media", f"{df['Tiempo_Espera_Min'].mean():.1f} min")
    st.metric("Satisfaccion", f"{df['Puntaje_Satisfaccion'].mean():.1f}/10")
    st.divider()
    st.write("Datos actualizados de 6 sucursales.")

col_main_left, col_main_right = st.columns([1, 1])

plt.style.use('dark_background')
PALETA_CAFE = ["#603808", "#8B4513", "#D2691E", "#BC8F8F", "#DEB887", "#F5DEB3"]

with col_main_left:
    with st.container(border=True):
        st.subheader("Ventas por Sucursal (Frec. Absoluta)")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='Sucursal', palette=PALETA_CAFE, ax=ax1)
        plt.xticks(rotation=45)
        st.pyplot(fig1)

with col_main_right:
    with st.container(border=True):
        st.subheader("Mix de Bebidas (Frec. Relativa)")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        df['Bebida'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=PALETA_CAFE, ax=ax2, startangle=90)
        ax2.set_ylabel('')
        st.pyplot(fig2)

st.divider()
with st.container(border=True):
    st.subheader("Analisis de Precios y Frecuencia Acumulada")
    df['rango_p'] = pd.cut(df['Precio'], bins=8).apply(lambda x: f"${x.left:.0f}-${x.right:.0f}")
    frec_p = df['rango_p'].value_counts().sort_index()
    
    fig3, ax3 = plt.subplots(figsize=(14, 5))
    ax3.plot(frec_p.index, frec_p.values, marker='o', color='#faedcd', label='Poligono (Absoluta)', linewidth=3)
    
    ax3.plot(frec_p.index, frec_p.cumsum().values, marker='s', color='#d4a373', label='Frec. Acumulada', linestyle='--')
    
    plt.legend()
    st.pyplot(fig3)

with st.expander("Explorar Registros del Catalogo"):
    st.dataframe(df, use_container_width=True)
