import streamlit as st
import asyncio
from hevai_api import send_booking_assistant_message, get_valid_timezones, validate_timezone
import uuid
import hashlib
import os
from dotenv import load_dotenv
import logging
import pytz
import datetime

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.title("Asistente de Reservas HEVA")

# Inicialización del estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "provider_id" not in st.session_state:
    st.session_state.provider_id = None

if "timezone" not in st.session_state:
    st.session_state.timezone = "America/New_York"  # Zona horaria predeterminada

# Diccionario de nombres de providers
PROVIDER_NAMES = {
    1: "Luxe Hair Restoration Clinic",
    2: "Radiant Skin Dermatology Center",
    3: "Bright Smile Dental Clinic",
    5: "Dr. Espinal Plastic Surgery",
    6: "Dr. Molina Cirujano Plastico Reconstructiva y Estetica",
    7: "Dra. Güilamo",
    8: "Dr. Welbin Paredes",
    9: "Dr. Jesus Abreu",
    10: "Dr Carlos Alverto Lopez Collado",
    11: "Dr. José León MD",
    12: "Dr. Yoiner Manuel Cedeño Rodríguez (Centro Cosme Surgery)",
    13: "Dr. Diego Valentín Tello ",
    14: "Dr. Humberto González O.",
    15: "Dra. Danivel Céspedes",
    16: "Dr. Daniel Lluberes",
    17: "Dra. Brendha Ogando",
    18: "Dra. Adriana Salcedo ",
    19: "Dr. Castillejos",
    20: "Dr. Bary G. Bigay",
    21: "Dr. Josué Safadit",
    22: "Dra. Thaulys  Luna",
    23: "Dra. Alexandrish Karvendrish Cirugía Plástica",
    24: "Dr. Erik Alvarez Sores",
    25: "Dr. Ivan Silva",
    26: "Dra. Romy Campos",
    28: "Dr. Nishita's Cosmetic Clinic",
    29: "Dr. Carlos Gutiérrez Banda",
    30: "Dr. Luis Ornelas",
    31: "Xavier Sanchez"
}

# Lista de zonas horarias más comunes para facilitar la selección al usuario
POPULAR_TIMEZONES = [
    "UTC",
    "America/New_York",      # Eastern Time
    "America/Chicago",       # Central Time
    "America/Denver",        # Mountain Time
    "America/Los_Angeles",   # Pacific Time
    "America/Mexico_City",   # Mexico
    "America/Bogota",        # Colombia
    "America/Santiago",      # Chile
    "America/Argentina/Buenos_Aires",  # Argentina
    "Europe/Madrid",         # España
    "Europe/London",         # Reino Unido
    "Europe/Paris",          # Europa Central
    "Asia/Tokyo",            # Japón
    "Asia/Shanghai",         # China
    "Asia/Kolkata",          # India (anteriormente Calcutta)
    "Asia/Dubai",            # UAE
    "Australia/Sydney"       # Australia
]

# Función para validar y actualizar la zona horaria
def update_timezone(timezone):
    """
    Valida y actualiza la zona horaria seleccionada por el usuario
    
    Args:
        timezone: La zona horaria seleccionada
        
    Returns:
        bool: True si la zona horaria es válida y se actualizó, False en caso contrario
    """
    # Verificar que la zona horaria seleccionada sea válida
    if validate_timezone(timezone):
        st.session_state.timezone = timezone
        return True
    else:
        return False

# Barra lateral para el token de acceso y configuraciones
with st.sidebar:
    access_token = st.text_input("Introduce el Provider Access Token", type="password")
    
    # Selector de zona horaria con opciones comunes/populares
    st.subheader("Configuración de Zona Horaria")
    
    # Radio button para elegir entre zonas populares o mostrar todas
    timezone_option = st.radio(
        "Seleccionar de:",
        ["Zonas horarias populares", "Todas las zonas horarias", "Buscar zona horaria"],
        index=0
    )
    
    # Mostrar el selector apropiado basado en la elección del usuario
    if timezone_option == "Zonas horarias populares":
        selected_timezone = st.selectbox(
            "Selecciona tu zona horaria:",
            options=POPULAR_TIMEZONES,
            index=POPULAR_TIMEZONES.index(st.session_state.timezone) if st.session_state.timezone in POPULAR_TIMEZONES else 0,
            format_func=lambda x: x.replace("_", " "),
            help="Selecciona la zona horaria más cercana a tu ubicación actual",
            key="popular_timezone_select"
        )
        # Validación y actualización
        if selected_timezone != st.session_state.timezone:
            if update_timezone(selected_timezone):
                st.success(f"Zona horaria actualizada: {selected_timezone}")
            else:
                st.error(f"Zona horaria inválida: {selected_timezone}")
                
    elif timezone_option == "Todas las zonas horarias":
        # Obtener todas las zonas horarias válidas
        all_timezones = get_valid_timezones()
        
        # Organizar por continentes/regiones para facilitar la navegación
        regions = {}
        for tz in all_timezones:
            region = tz.split("/")[0] if "/" in tz else "Otros"
            if region not in regions:
                regions[region] = []
            regions[region].append(tz)
        
        # Selector de región
        region_options = sorted(regions.keys())
        selected_region = st.selectbox(
            "Selecciona una región:",
            options=region_options,
            index=region_options.index(st.session_state.timezone.split("/")[0]) if "/" in st.session_state.timezone and st.session_state.timezone.split("/")[0] in region_options else 0
        )
        
        # Selector de zona horaria dentro de la región seleccionada
        region_timezones = sorted(regions[selected_region])
        region_timezone_index = 0
        if st.session_state.timezone in region_timezones:
            region_timezone_index = region_timezones.index(st.session_state.timezone)
            
        selected_timezone = st.selectbox(
            "Selecciona tu zona horaria:",
            options=region_timezones,
            index=region_timezone_index,
            format_func=lambda x: x.replace("_", " "),
            help="Selecciona la zona horaria más cercana a tu ubicación actual",
            key="all_timezones_select"
        )
        
        # Validación y actualización
        if selected_timezone != st.session_state.timezone:
            if update_timezone(selected_timezone):
                st.success(f"Zona horaria actualizada: {selected_timezone}")
            else:
                st.error(f"Zona horaria inválida: {selected_timezone}")
    
    else:  # Opción de búsqueda
        # Campo de búsqueda para zonas horarias
        search_query = st.text_input(
            "Buscar zona horaria:",
            help="Introduce parte del nombre de una ciudad o región para buscar (ej: 'New York', 'Tokyo', 'Europe')"
        )
        
        if search_query:
            # Filtrar zonas horarias que coincidan con la búsqueda
            all_timezones = get_valid_timezones()
            filtered_timezones = [tz for tz in all_timezones if search_query.lower() in tz.lower()]
            
            if filtered_timezones:
                selected_timezone = st.selectbox(
                    "Resultados de la búsqueda:",
                    options=filtered_timezones,
                    format_func=lambda x: x.replace("_", " "),
                    key="search_timezone_select"
                )
                
                # Validación y actualización
                if st.button("Establecer esta zona horaria"):
                    if update_timezone(selected_timezone):
                        st.success(f"Zona horaria actualizada: {selected_timezone}")
                    else:
                        st.error(f"Zona horaria inválida: {selected_timezone}")
            else:
                st.warning(f"No se encontraron zonas horarias que coincidan con '{search_query}'")
    
    # Mostrar información de la zona horaria actual
    try:
        tz = pytz.timezone(st.session_state.timezone)
        current_time = datetime.datetime.now(tz)
        time_str = current_time.strftime("%H:%M:%S")
        date_str = current_time.strftime("%d/%m/%Y")
        
        st.info(f"Zona horaria actual: {st.session_state.timezone}")
        st.info(f"Hora local: {time_str}")
        st.info(f"Fecha local: {date_str}")
        st.info(f"UTC Offset: {current_time.utcoffset()}")
    except Exception as e:
        st.error(f"Error al obtener información de la zona horaria: {str(e)}")
    
    # Verificar token de acceso
    if access_token:
        # Verificar contra los provider hashes
        provider_found = False
        for i in [*range(1, 4), *range(5, 32)]:  # Modificado para incluir hasta el provider 31
            env_hash = os.getenv(f'PROVIDER_HASH_{i}')
            if env_hash and access_token.lower() == env_hash.lower():
                st.session_state.provider_id = i
                provider_found = True
                provider_name = PROVIDER_NAMES.get(i, f"Provider {i}")
                st.success(f"Token válido para: {provider_name}")
                break
        
        if not provider_found:
            st.error("Token de acceso inválido")
            logging.warning("Intento de acceso con token inválido")

# Debug log
logging.debug("Estado de autenticación: %s", "Autenticado" if st.session_state.provider_id else "No autenticado")
logging.debug(f"Zona horaria seleccionada: {st.session_state.timezone}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    if st.session_state.provider_id is None:
        st.error("Por favor, introduce un token de acceso válido primero")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                response = asyncio.run(send_booking_assistant_message(
                    provider_id=st.session_state.provider_id,
                    conversation_id=st.session_state.conversation_id,
                    user_message=prompt,
                    timezone=st.session_state.timezone,  # Usar la zona horaria seleccionada
                    base_url=os.getenv("base_url")
                ))
                # Procesar la respuesta para mostrarla correctamente
                import ast
                try:
                    # Usar literal_eval para interpretar la cadena correctamente
                    cleaned_response = ast.literal_eval(response)
                except (ValueError, SyntaxError) as e:
                    # Si falla la interpretación literal, intentar con decodificación simple
                    logging.debug(f"Error en literal_eval: {e}")
                    cleaned_response = response.strip('"').encode().decode('unicode_escape')
                except Exception as e:
                    # Si todo lo demás falla, usar la respuesta original
                    logging.error(f"Error procesando respuesta: {e}")
                    cleaned_response = response
                
                message_placeholder.markdown(cleaned_response)
                st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")
