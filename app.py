import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd

# 1. Configuración
st.set_page_config(page_title="Kuyay Cuentos", page_icon="🌟")

# 2. El "Enchufe" al Excel (Aquí es donde fallaba)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.sidebar.success("✅ Conexión al Excel lista")
except Exception as e:
    st.sidebar.error("❌ Falta configurar la llave (Secrets)")

st.title("🌟 BIENVENIDO A KUYAY")

if 'usuario' not in st.session_state:
    nombre = st.text_input("¿Cómo te llamas, amiguito?")
    if st.button("INGRESAR"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
else:
    st.write(f"### ¡Hola {st.session_state.usuario}!")
    
    # BOTÓN PARA GUARDAR EN EXCEL
    if st.button("GUARDAR MI NOMBRE EN EL EXCEL"):
        try:
            # 1. Leer lo que ya hay en la Hoja 1
            df_viejo = conn.read(worksheet="Hoja 1")
            
            # 2. Crear la nueva fila
            nueva_data = pd.DataFrame([{"Alumno": st.session_state.usuario, "Puntaje": "Conectado"}])
            
            # 3. Juntarlos y subir
            df_final = pd.concat([df_viejo, nueva_data], ignore_index=True)
            conn.update(worksheet="Hoja 1", data=df_final)
            
            st.success("¡Logrado! Tu nombre ya está en el Excel de la Profe.")
            st.balloons()
        except Exception as e:
            st.error(f"Error al guardar: {e}")