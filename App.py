import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium


df = pd.read_csv('1Alabanza_Direc.csv', encoding='utf-8-sig', sep=';')
df['Latitud'] = df['Latitud'].str.replace(',', '.').astype(float)
df['Longitud'] = df['Longitud'].str.replace(',', '.').astype(float)
df["Misa previa"] = df["Misa previa"].fillna("no").str.strip().str.lower()
df["Frecuencia"] = df["Frecuencia"].str.strip().str.lower().str.capitalize()


# Título y logo
col1, col2 = st.columns([1, 6])  # Ajusta proporción según tamaño imagen/título
with col1:
    st.image('espiritu-santo.png', width=75)
with col2:
    st.title("Alabanza en Madrid: Encuentra dónde glorificar a Dios juntos")

with st.container():
    st.markdown("> _\"Te alabaré, Señor, con todo mi corazón, contaré todas tus maravillas.\"_  \n> — **Salmo 9,1**")
    st.markdown("""
    Esta plataforma reúne en un solo lugar todas las **oraciones de alabanza** celebradas en Madrid:  
    📍 **Ubicación**, 🗓️ **día**, ⏰ **hora**, 🔁 **frecuencia** y 🧭 cómo llegar fácilmente.

    ¡Descubre dónde unirte para alabar a Dios en comunidad!
    """)

# Filtros
with st.sidebar:
    st.header("🎛️ Filtros")

    # Filtro por día
    st.markdown("📅 Selecciona uno o más días:")
    dias_seleccionados = []
    for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
        if st.checkbox(dia, True, key=dia):
            dias_seleccionados.append(dia)

    # Filtro por misa previa
    misa_seleccionada = st.selectbox("🕯️ ¿Hay misa previa?", ["Todas", "Sí", "No"])

    # Filtro por frecuencia
    frec_opciones = df['Frecuencia'].dropna().unique().tolist()
    frecuencia_personalizada = st.selectbox("📆 Frecuencia", ["Todas", "Semanal", "Una vez al mes", "Otros"])

    def clasificar_frecuencia(f):
        f_lower = str(f).lower()

        if "semanal" in f_lower:
            return "Semanal"
        elif "y" in f_lower:
            return "Otros"
        elif any(p in f_lower for p in ["último", "primer", "segundo", "tercer", "mensual"]):
            return "Una vez al mes"
        else:
            return "Otros"

df['Frecuencia_categoria'] = df['Frecuencia'].apply(clasificar_frecuencia)


df_filtrado = df.copy()

if dias_seleccionados:
    df_filtrado = df_filtrado[df_filtrado['Dia'].isin(dias_seleccionados)]

if misa_seleccionada == "Sí":
    df_filtrado = df_filtrado[df_filtrado["Misa previa"] != "no"]
elif misa_seleccionada == "No":
    df_filtrado = df_filtrado[df_filtrado["Misa previa"] == "no"]

if frecuencia_personalizada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Frecuencia_categoria"] == frecuencia_personalizada]


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

with st.sidebar:
    st.header("📢 Comparte esta app")
    st.markdown("""
    <a href="https://wa.me/?text=Descubre%20las%20oraciones%20de%20alabanza%20en%20Madrid%20con%20mapa,%20horarios%20y%20cómo%20llegar:%20https://mapa-alabanza-madrid.streamlit.app/"
    target="_blank">
    <button style='background-color:#25D366; color:white; border:none; padding:10px 16px; border-radius:5px; font-size:16px; cursor:pointer;'>
        Compartir por WhatsApp 📲
    </button>
    </a>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("📝 Incluye tu oración de alabanza")
    st.markdown("""
    Si quieres que incluyamos tu oración de alabanza, por favor completa este formulario:
    [🧾 Formulario de inclusión](https://forms.gle/Wf8KeyjqswDLubkk7)
    """)

st.success("¡Gracias por contribuir con tu oración!")

with st.sidebar:
    st.header("📣 Para recibir los carteles")
    st.markdown("""
    [💬 Únete al grupo de whatsapp](https://chat.whatsapp.com/GGb3jXatphAIDwQqd4cUw9)
    """)

#git add App.py
#git commit -m "Arreglar popup para mostrar enlace de Google Maps en marcador"
#git push origin main


#git pull origin main --rebase
#git push origin main

