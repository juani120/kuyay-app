import streamlit as st
import pandas as pd
from datetime import datetime
from st_gsheets_connection import GSheetsConnection
# 1. CONFIGURACIÓN
st.set_page_config(page_title="Kuyay Cuentos", layout="centered")

# --- CONEXIÓN DIRECTA ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Error de conexión. Revisa los Secrets.")

# 2. FUNCIÓN PARA GUARDAR
def enviar_a_google(nombre, cuento, nota):
    try:
        # Leemos lo que ya hay
        df_existente = conn.read(worksheet="Hoja 1", ttl=0)
        
        # Creamos la nueva fila
        nueva_fila = pd.DataFrame({
            "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "Alumno": [nombre],
            "Cuento": [cuento],
            "Puntaje": [f"{nota}/3"]
        })
        
        # Juntamos y subimos
        df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
        conn.update(worksheet="Hoja 1", data=df_final)
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# --- LÓGICA DE LA APP (IGUAL QUE ANTES) ---
if 'usuario' not in st.session_state:
    st.title("🌟 BIENVENIDO A KUYAY")
    nombre = st.text_input("¿Cómo te llamas?")
    if st.button("INGRESAR"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
else:
    st.write(f"Hola, {st.session_state.usuario}")
    # ... (resto de tu código de cuentos) ...
    if st.button("ENVIAR NOTA DE PRUEBA"):
        exito = enviar_a_google(st.session_state.usuario, "Prueba", 3)
        if exito:
            st.success("✅ ¡MIRA TU EXCEL! Ya debe aparecer.")