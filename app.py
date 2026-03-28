import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PANTALLA
st.set_page_config(page_title="Kuyay Cuentos", layout="centered")

# 2. CONEXIÓN CON TU EXCEL (Busca los Secrets que pegamos antes)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Error de conexión. Verifica los Secrets en Streamlit.")

# 3. BASE DE DATOS DE CUENTOS
cuentos_db = {
    "1. El Cóndor y la Pastora": {
        "texto": "Un joven cóndor se enamoró de una bella pastora en Puno...",
        "imagen": "condor.png",
        "r": "Un Cóndor"
    },
    "2. El Zorro y el Cuy": {
        "texto": "El cuy engañó al zorro con el cielo que se caía...",
        "imagen": "zorro.png",
        "r": "El Cuy"
    }
}

# 4. LÓGICA DE LA APP
if 'usuario' not in st.session_state:
    st.title("🌟 BIENVENIDO A KUYAY")
    nombre = st.text_input("¿Cómo te llamas, amiguito?")
    if st.button("INGRESAR"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
else:
    opcion = st.selectbox("Elige tu cuento:", list(cuentos_db.keys()))
    cuento = cuentos_db[opcion]
    
    st.header(opcion)
    try: st.image(cuento["imagen"], use_container_width=True)
    except: st.info("Imagen no encontrada")
    
    st.write(cuento["texto"])
    
    # Evaluación simple
    res = st.radio("¿Quién es el personaje principal?", ["Un Puma", "Un Cóndor", "El Cuy"])
    
    if st.button("ENVIAR NOTA"):
        puntos = "3/3" if res == cuento["r"] else "0/3"
        
        # GUARDADO EN GOOGLE SHEETS
        try:
            df_existente = conn.read(worksheet="Hoja 1")
            nueva_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Alumno": st.session_state.usuario,
                "Cuento": opcion,
                "Puntaje": puntos
            }])
            df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
            conn.update(worksheet="Hoja 1", data=df_final)
            st.success(f"¡Muy bien {st.session_state.usuario}! Nota guardada en el Excel.")
            if puntos == "3/3": st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")