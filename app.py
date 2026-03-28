import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(page_title="Kuyay Cuentos", page_icon="🌟")

# CONEXIÓN
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🌟 BIENVENIDO A KUYAY")

if 'usuario' not in st.session_state:
    nombre = st.text_input("¿Cómo te llamas, amiguito?")
    if st.button("INGRESAR"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
else:
    st.write(f"### ¡Hola {st.session_state.usuario}! Vamos a leer.")
    
    # Prueba de guardado directo
    if st.button("PROBAR CONEXIÓN CON EXCEL"):
        try:
            # Creamos una fila de prueba
            nueva_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Alumno": st.session_state.usuario,
                "Cuento": "Prueba de Sistema",
                "Puntaje": "Conectado"
            }])
            
            # Leemos y actualizamos
            df_antiguo = conn.read(worksheet="Hoja 1")
            df_final = pd.concat([df_antiguo, nueva_fila], ignore_index=True)
            conn.update(worksheet="Hoja 1", data=df_final)
            
            st.success("✅ ¡CONEXIÓN EXITOSA! Revisa tu Excel de Google.")
            st.balloons()
        except Exception as e:
            st.error(f"Error técnico: {e}")

    # Aquí puedes luego pegar tus cuentos del Cóndor y el Zorro