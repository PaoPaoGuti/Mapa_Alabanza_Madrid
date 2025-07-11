import pandas as pd
import folium
import streamlit as st
import streamlit_geolocation
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval, get_geolocation
from geopy.distance import geodesic


df = pd.read_csv('1Alabanza_Direc.csv', encoding='utf-8-sig', sep=';')
df['Latitud'] = df['Latitud'].str.replace(',', '.').astype(float)
df['Longitud'] = df['Longitud'].str.replace(',', '.').astype(float)

# Título y logo
col1, col2 = st.columns([1, 6])  # Ajusta proporción según tamaño imagen/título
with col1:
    st.image('espiritu-santo.png', width=75)
with col2:
    st.title("Alabanza en Madrid")

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

# Filtro por proximidad
usar_ubicacion = st.sidebar.checkbox("Mostrar solo oraciones cerca de mí (15 km)")
user_coords = None

if usar_ubicacion:
    result = streamlit_js_eval(
        js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
        key="get_location",
        want_return=True
    )

    if result and isinstance(result, dict):
        lat = result.get("latitude")
        lon = result.get("longitude")

        if lat and lon:
            user_coords = (lat, lon)
            st.success(f"📍 Ubicación detectada: lat={lat}, lon={lon}")
        else:
            st.warning("No se pudo obtener latitud y longitud correctamente.")
    else:
        st.warning("No se pudo obtener la ubicación. Verifica los permisos del navegador.")




st.markdown(f"🔥 **{len(df_filtrado)} oraciones de alabanza encontradas** para: {', '.join(dias_seleccionados) if dias_seleccionados else 'Todos los días'}")

# Crear mapa centrado en Madrid
mapa = folium.Map(location=[40.63094569557773, -3.724584186759364], zoom_start=10)
for _, row in df_filtrado.iterrows():
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={row['Latitud']},{row['Longitud']}"
    contenido = contenido = f"""
    <div style="width:250px;">
        <h4 style="margin-bottom: 4px;">{row['Frecuencia']}</h4>
        <p style="margin: 0;"><strong>⛪ Lugar:</strong> {row['Nombre']}</p>
        <p style="margin: 0;"><strong>🗓️ Día:</strong> {row['Dia']}</p>
        <p style="margin: 0;"><strong>🕖 Hora:</strong> {row['Hora']}</p>
        <p style="margin: 0;"><strong>🕯️ Misa previa:</strong> {row['Misa previa']}</p>
        <p style="margin-top: 8px;"><a href="{maps_url}" target="_blank">📍🧭 Cómo llegar 🚗🚇</a></p>
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


'''git add App.py
git commit -m "Arreglar popup para mostrar enlace de Google Maps en marcador"
git push origin main


git pull origin main --rebase
git push origin main'''