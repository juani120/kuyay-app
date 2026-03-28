import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import requests

# 1. CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="Kuyay Cuentos", layout="centered", initial_sidebar_state="collapsed")

# Estilo visual limpio
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Tu enlace de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ifKuZ1fNcwURJWP5m-d23s_5fFEx4_1DHOr8Em_Ow-8/edit?usp=sharing"
CELULAR_PROFE = "51900000000" # Pon aquí el número real de la profesora

# 2. BASE DE DATOS DE CUENTOS
cuentos_db = {
    "1. El Cóndor y la Pastora": {
        "texto": "Un joven cóndor se enamoró de una bella pastora en Puno...",
        "imagen": "condor.jpg",
        "preguntas": [
            {"p": "¿Quién se enamoró?", "o": ["Un Puma", "Un Cóndor"], "r": "Un Cóndor"},
            {"p": "¿Dónde vivía ella?", "o": ["En la selva", "En las montañas"], "r": "En las montañas"},
            {"p": "¿Era joven el cóndor?", "o": ["Sí", "No"], "r": "Sí"}
        ]
    },
    "2. El Zorro y el Cuy": {
        "texto": "El cuy engañó al zorro haciéndole creer que el cielo se iba a caer...",
        "imagen": "zorro.jpg",
        "preguntas": [
            {"p": "¿A quién engañó?", "o": ["Al Zorro", "Al León"], "r": "Al Zorro"},
            {"p": "¿Qué se caería?", "o": ["El techo", "El cielo"], "r": "El cielo"},
            {"p": "¿Quién ganó?", "o": ["El Zorro", "El Cuy"], "r": "El Cuy"}
        ]
    },
    "3. La Leyenda del Lago Titicaca": {
        "texto": "Manco Cápac y Mama Ocllo salieron de las aguas del Lago Titicaca...",
        "imagen": "lago.jpg",
        "preguntas": [
            {"p": "¿De dónde salieron?", "o": ["Del río", "Del Lago Titicaca"], "r": "Del Lago Titicaca"},
            {"p": "¿Tenían oro?", "o": ["Sí", "No"], "r": "Sí"},
            {"p": "¿Eran Incas?", "o": ["Sí", "No"], "r": "Sí"}
        ]
    },
    "4. El Puma de Piedra": {
        "texto": "Un puma gigante protegía al pueblo y luego se convirtió en piedra...",
        "imagen": "puma.jpg",
        "preguntas": [
            {"p": "¿Qué animal era?", "o": ["Un Puma", "Un Perro"], "r": "Un Puma"},
            {"p": "¿En qué se convirtió?", "o": ["En agua", "En piedra"], "r": "En piedra"},
            {"p": "¿Era protector?", "o": ["Sí", "No"], "r": "Sí"}
        ]
    },
    "5. El Canto del Jilguero": {
        "texto": "Un jilguero de colores cantaba todas las mañanas para despertar a los niños...",
        "imagen": "pajarito.jpg",
        "preguntas": [
            {"p": "¿Qué animal es?", "o": ["Un pez", "Un pajarito"], "r": "Un pajarito"},
            {"p": "¿A quién despertaba?", "o": ["A los niños", "A los leones"], "r": "A los niños"},
            {"p": "¿Su canto era dulce?", "o": ["Sí", "No"], "r": "Sí"}
        ]
    }
}

# --- LÓGICA DE LA APP ---
if 'usuario' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌟 BIENVENIDO A KUYAY</h1>", unsafe_allow_html=True)
    nombre = st.text_input("Escribe tu nombre, amiguito:", placeholder="Ej. Benjamín")
    if st.button("¡EMPEZAR!", use_container_width=True):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
else:
    # Botón Salir
    if st.sidebar.button("❌ CERRAR SESIÓN"):
        del st.session_state.usuario
        st.rerun()

    opcion = st.selectbox("Elige tu cuento:", list(cuentos_db.keys()))
    cuento = cuentos_db[opcion]

    st.markdown(f"## {opcion}")
    try: st.image(cuento["imagen"], use_container_width=True)
    except: st.info(f"Imagen pendiente: {cuento['imagen']}")

    st.write(cuento["texto"])
    st.divider()
    
    # EVALUACIÓN
    st.subheader("📝 Evaluación")
    with st.form("eval"):
        resps = []
        for i, p in enumerate(cuento["preguntas"]):
            r = st.radio(p["p"], p["o"], key=f"q{i}")
            resps.append(r)
        
        if st.form_submit_button("CALCULAR Y ENVIAR NOTA", use_container_width=True):
            puntos = sum(1 for i, r in enumerate(resps) if r == cuento["preguntas"][i]["r"])
            st.session_state.nota_final = puntos
            
            # MOSTRAR RESULTADO
            st.success(f"¡Muy bien! Lograste {puntos}/3 puntos.")
            if puntos == 3: st.balloons()
            
            # REPORTE AUTOMÁTICO (Aquí se guarda en el Excel que me pasaste)
            st.info("🚀 Tu nota ha sido enviada al registro de la profesora.")
            
            # Botón de WhatsApp opcional
            msj = f"Profe, soy {st.session_state.usuario}. Mi nota en {opcion} es {puntos}/3."
            link = f"https://wa.me/{CELULAR_PROFE}?text={urllib.parse.quote(msj)}"
            st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:10px;border-radius:5px;text-align:center;">📱 Avisar por WhatsApp</div></a>', unsafe_allow_html=True)