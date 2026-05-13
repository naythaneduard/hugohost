import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
# Configuración básica y tema oscuro nativo
st.set_page_config(page_title="Catalogo de Datos Masivos", layout="wide")
sns.set_theme(style="dark", palette="pastel")
plt.rcParams.update({
    'figure.facecolor': '#0e1117',
    'axes.facecolor': '#0e1117',
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white'
})
 
st.title("Catalogo Estadistico de Resultados")
 
# Carga de datos masivos
try:
    df = pd.read_csv("datos_masivos_examen.csv")
except FileNotFoundError:
    st.error("No se encontró el archivo 'datos_masivos_examen.csv'")
    st.stop()
 
# --- SECCIÓN 1: CATÁLOGO DE MÉTRICAS ---
st.header("Resumen de Variables")
cols = st.columns(3)
 
metricas = {
    "Precio Venta": df['precio'],
    "Nivel de Stock": df['stock'],
    "Calificacion": df['calificacion']
}
 
for i, (nombre, serie) in enumerate(metricas.items()):
    with cols[i % 3]:
        with st.container(border=True):
            st.subheader(nombre)
            st.write(f"**Media:** {serie.mean():.2f}")
            st.write(f"**Mediana:** {serie.median():.2f}")
            st.write(f"**Moda:** {serie.mode()[0]}")
 
# --- SECCIÓN 2: CATÁLOGO DE GRÁFICOS ---
st.divider()
st.header("Visualizaciones del Catalogo")
 
tab1, tab2, tab3 = st.tabs(["Frecuencias Categoria", "Distribucion Precios", "Datos Crudos"])
 
with tab1:
    col_a, col_b = st.columns(2)
    frec = df['categoria'].value_counts()
   
    with col_a:
        st.write("**Frecuencia Absoluta (Categorias)**")
        fig, ax = plt.subplots()
        frec.plot(kind='bar', ax=ax, color='#8ecae6')
        plt.xticks(rotation=45)
        st.pyplot(fig)
       
    with col_b:
        st.write("**Frecuencia Relativa (%)**")
        fig, ax = plt.subplots()
        frec.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=140)
        ax.set_ylabel('')
        st.pyplot(fig)
 
with tab2:
    st.write("**Poligono de Frecuencias y Acumulada (Precios)**")
   
    # --- SOLUCIÓN AL PROBLEMA DE LA IMAGEN image_70cb20.png ---
    # Creamos los bins y los convertimos a string inmediatamente para evitar el JSON
    df['rango_precio'] = pd.cut(df['precio'], bins=10).apply(lambda x: f"{x.left:.2f} - {x.right:.2f}")
   
    frec_precio = df['rango_precio'].value_counts().sort_index()
   
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(frec_precio.index, frec_precio.values, marker='o', label='Absoluta', color='#ffb703')
    ax.plot(frec_precio.index, frec_precio.cumsum().values, marker='s', label='Acumulada', color='#fb8500')
   
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)
 
with tab3:
    with st.expander("Ver inventario completo de registros"):
        # Mostramos el DataFrame limpio
        st.dataframe(df, use_container_width=True)