import streamlit as st
import json
import datetime
import os
import pandas as pd

# Configuración visual
st.set_page_config(page_title="AguaApp CDMX", page_icon="💧", layout="wide")

# Archivos de datos (Bases de Datos locales)
ARCHIVO_REPORTES = "reportes.json"
ARCHIVO_INTERESADOS = "interesados_beta.json"
ALCALDIAS = sorted(["Azcapotzalco", "Benito Juárez", "Coyoacán", "Cuajimalpa", "Cuauhtémoc", "Gustavo A. Madero", "Iztacalco", "Iztapalapa", "Magdalena Contreras", "Miguel Hidalgo", "Milpa Alta", "Tláhuac", "Tlalpan", "Venustiano Carranza", "Xochimilco", "Álvaro Obregón"])

# --- FUNCIONES DE AYUDA (El motor de la app) ---
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            return json.load(f)
    return []

def guardar_dato(archivo, nuevo_dato):
    datos = cargar_datos(archivo)
    datos.append(nuevo_dato)
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)

# --- NAVEGACIÓN ---
st.sidebar.title("💧 AguaApp CDMX")
menu = st.sidebar.radio("Menú:", ["Mapa Público", "Reportar (Testers)", "Próxima Fase (1,000)"])

# --- PÁGINA 1: MAPA PÚBLICO (Lo que ve la población general) ---
if menu == "Mapa Público":
    st.title("📊 Disponibilidad de Agua en CDMX")
    st.write("Datos actualizados por la comunidad de voluntarios.")
    
    datos = cargar_datos(ARCHIVO_REPORTES)
    if datos:
        df = pd.DataFrame(datos)
        # Mostramos un resumen rápido
        resumen = df.groupby('alcaldia')['estado'].last().reset_index()
        st.subheader("Estado actual por alcaldía:")
        st.dataframe(resumen, use_container_width=True)
    else:
        st.info("Aún no hay reportes registrados para hoy.")

# --- PÁGINA 2: PANEL DE TESTERS (Donde entran tus 250 voluntarios) ---
elif menu == "Reportar (Testers)":
    st.title("📝 Panel de Reporte Exclusivo")
    
    # 1. El Candado de Seguridad
    st.info("Esta sección es solo para voluntarios autorizados.")
    codigo_acceso = st.text_input("Ingresa el Código de Invitación:", type="password")

    # 2. Verificación del código
    if codigo_acceso == "AGUA_BETA_2026": # <--- Este es tu código, cámbialo si quieres
        st.success("🔓 Acceso Autorizado")
        
        correo = st.text_input("Tu correo electrónico:")
        
        if correo:
            st.divider()
            alcaldia = st.selectbox("¿En qué alcaldía estás?", ALCALDIAS)
            st.write("¿Cómo está el servicio en este momento?")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("❌ NO HAY AGUA", use_container_width=True):
                    guardar_dato(ARCHIVO_REPORTES, {
                        "correo": correo, "estado": "NO", "alcaldia": alcaldia, 
                        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.error("Reporte de escasez enviado. ¡Gracias!")
            
            with c2:
                if st.button("✅ SÍ HAY / REGRESÓ", use_container_width=True):
                    guardar_dato(ARCHIVO_REPORTES, {
                        "correo": correo, "estado": "SI", "alcaldia": alcaldia, 
                        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success("Reporte de servicio activo enviado.")
    
    elif codigo_acceso != "":
        st.error("🚫 Código incorrecto. Solicítalo al administrador del proyecto.")

# --- PÁGINA 3: LISTA DE ESPERA (Marketing / Crecimiento) ---
elif menu == "Próxima Fase (1,000)":
    st.title("🚀 Próximamente: 1,000 Testers")
    st.write("Estamos preparando la siguiente fase. Si quieres participar, regístrate:")
    
    nuevo_correo = st.text_input("Tu correo:")
    if st.button("Registrarme para la Fase 2"):
        if "@" in nuevo_correo:
            guardar_dato(ARCHIVO_INTERESADOS, {
                "correo": nuevo_correo, "fecha": str(datetime.datetime.now())
            })
            st.balloons()
            st.success("¡Registrado! Te avisaremos pronto.")