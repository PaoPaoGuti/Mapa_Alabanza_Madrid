import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

df = pd.read_csv('1Alabanza_Direc.csv', encoding='utf-8-sig', sep=';')
df['Latitud'] = df['Latitud'].str.replace(',', '.').astype(float)
df['Longitud'] = df['Longitud'].str.replace(',', '.').astype(float)

# Título y logo
col1, col2 = st.columns([1, 6])  # Ajusta proporción según tamaño imagen/título
with col1:
    st.image('espiritu-santo.png', width=75)
with col2:
    st.title("Mapa de Alabanzas en Madrid")

# Filtrado por día
with st.sidebar:
    st.header("🎛️ Filtros")
    dias_seleccionados = []
    cols = st.columns(1)
    st.markdown("Selecciona uno o más días:")
    for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
        if st.checkbox(dia, True, key=dia):
            dias_seleccionados.append(dia)

df_filtrado = df[df['Dia'].isin(dias_seleccionados)] if dias_seleccionados else df

st.markdown(f"🔥 **{len(df_filtrado)} oraciones de alabanza encontradas** para: {', '.join(dias_seleccionados) if dias_seleccionados else 'Todos los días'}")

# Crear mapa centrado en Madrid
mapa = folium.Map(location=[40.63094569557773, -3.724584186759364], zoom_start=10)
for _, row in df_filtrado.iterrows():
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={row['Latitud']},{row['Longitud']}"
    contenido = contenido = f"""
<div style="width:300px;">
    <h4 style="margin-bottom: 5px;">{row['Frecuencia']}</h4>
    <p style="margin: 0;"><strong>⛪ Lugar:</strong> {row['Nombre']}</p>
    <p style="margin: 0;"><strong>🗓️ Día:</strong> {row['Dia']}</p>
    <p style="margin: 0;"><strong>🕖 Hora:</strong> {row['Hora']}</p>
    <p style="margin: 0;"><strong>🕯️ Misa previa:</strong> {row['Misa previa']}</p>
    <p style="margin-top: 8px;"><a href="{maps_url}" target="_blank">🧭 Cómo llegar 🚗🚇</a></p>
</div>
"""
    folium.Marker(
        location=[row['Latitud'], row['Longitud']],
        popup=contenido,
            icon=folium.CustomIcon(
                icon_image='espiritu-santo.png',
                icon_size=(30, 30)
            ),
        tooltip=row['Nombre']
    ).add_to(mapa)

# Mostrar mapa
st_folium(mapa, width=700, height=500)