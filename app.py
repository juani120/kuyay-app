import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Kuyay Cuentos", page_icon="🌟")

# 2. CONEXIÓN A GOOGLE SHEETS
# Este bloque busca los "Secrets" que pegamos en Streamlit
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Falta configurar los Secrets: {e}")

st.title("🌟 BIENVENIDO A KUYAY")

# 3. SISTEMA DE USUARIO
if 'usuario' not in st.session_state:
    nombre = st.text_input("¿Cómo te llamas, amiguito?")
    if st.button("INGRESAR"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
        else:
            st.warning("Por favor, escribe tu nombre.")
else:
    st.write(f"### ¡Hola {st.session_state.usuario}! Vamos a probar el sistema.")
    
    # 4. BOTÓN DE PRUEBA DE GUARDADO
    if st.button("ENVIAR NOTA DE PRUEBA"):
        try:
            # Leemos lo que ya hay en el Excel (Hoja 1)
            df_existente = conn.read(worksheet="Hoja 1", ttl=0)
            
            # Creamos la nueva fila con los datos
            nueva_fila = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Alumno": st.session_state.usuario,
                "Cuento": "Prueba de Conexión",
                "Puntaje": "3/3"
            }])
            
            # Juntamos los datos viejos con el nuevo
            df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
            
            # Subimos todo al Excel
            conn.update(worksheet="Hoja 1", data=df_actualizado)
            
            st.success("✅ ¡CONEXIÓN EXITOSA! Revisa tu Excel ahora mismo.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error al conectar con el Excel: {e}")
            st.info("Asegúrate de que la hoja de tu Excel se llame exactamente 'Hoja 1'.")

    # Botón para cerrar sesión si deseas entrar con otro nombre
    if st.button("Cerrar Sesión"):
        del st.session_state.usuario
        st.rerun()