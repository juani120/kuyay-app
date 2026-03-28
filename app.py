import streamlit as st

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Kuyay Cuentos", page_icon="🌟")

# 2. TÍTULO PRINCIPAL
st.title("🌟 BIENVENIDO A KUYAY")
st.subheader("Cuentos Mágicos del Perú")

# 3. SISTEMA DE BIENVENIDA (ESTADO DE SESIÓN)
if 'usuario' not in st.session_state:
    # Pantalla de inicio para pedir el nombre
    st.write("### ¡Hola! Para empezar, dinos quién eres.")
    nombre = st.text_input("Escribe tu nombre aquí amiguito:")
    
    if st.button("¡EMPEZAR AVENTURA!"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun() # Esto recarga la página con el nombre guardado
        else:
            st.warning("Por favor, escribe un nombre para continuar.")
else:
    # Pantalla cuando ya puso su nombre
    st.write(f"## ¡Qué alegría verte, {st.session_state.usuario}! 👋")
    st.write("---")
    st.success("¡La aplicación está funcionando correctamente!")
    
    st.info("Pronto aquí verás los cuentos del Cóndor y el Zorro.")
    
    # Botón por si quiere entrar con otro nombre
    if st.button("Cambiar de nombre"):
        del st.session_state.usuario
        st.rerun()