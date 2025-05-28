import aiohttp
import json
from typing import Dict, Any, List, Optional
import logging
from urllib.parse import urljoin
import asyncio
import pytz  # Importamos pytz para validar las zonas horarias
from config import API_MAX_RETRIES, API_RETRY_DELAY, API_TIMEOUT

# Lista de todas las zonas horarias
ALL_TIMEZONES = list(pytz.all_timezones)

async def _try_send_message(session, url, payload, headers, attempt):
    """Helper function to send message with logging"""
    logging.info(f"Intento #{attempt} de enviar mensaje")
    async with session.post(url, json=payload, headers=headers) as response:
        response_text = await response.text()
        logging.debug(f"Response status: {response.status}")
        logging.debug(f"Response body: {response_text}")
        
        if response.status == 500:
            raise aiohttp.ClientResponseError(
                request_info=response.request_info,
                history=response.history,
                status=response.status,
                message=f"Internal Server Error: {response_text}"
            )
        elif response.status != 200:
            raise aiohttp.ClientResponseError(
                request_info=response.request_info,
                history=response.history,
                status=response.status,
                message=f"API Error: {response_text}"
            )
        return response_text

def validate_timezone(timezone: str) -> bool:
    """
    Valida si la zona horaria proporcionada es válida
    
    Args:
        timezone: La zona horaria a validar
        
    Returns:
        bool: True si la zona horaria es válida, False en caso contrario
    """
    return timezone in pytz.all_timezones

def get_valid_timezones() -> List[str]:
    """
    Retorna la lista completa de zonas horarias válidas
    
    Returns:
        List[str]: Lista de todas las zonas horarias válidas
    """
    return ALL_TIMEZONES

async def send_booking_assistant_message(
    provider_id: int,
    conversation_id: str,
    user_message: str,
    timezone: Optional[str] = None,
    base_url: str = "http://localhost:8000"
) -> str:
    """
    Sends a message to the booking assistant with retry logic
    
    Args:
        provider_id: ID del proveedor
        conversation_id: ID de la conversación
        user_message: Mensaje del usuario
        timezone: Zona horaria del cliente (opcional)
        base_url: URL base del servidor
        
    Returns:
        str: Respuesta del servidor
    """
    logging.info(f"Sending message to booking assistant - Provider: {provider_id}, Conversation: {conversation_id}")
    
    MAX_RETRIES = API_MAX_RETRIES
    RETRY_DELAY = API_RETRY_DELAY  # segundos

    # Si no se proporciona timezone, usar UTC
    timezone = timezone or "UTC"
    logging.info(f"Usando zona horaria: {timezone}")

    payload = {
        "provider_id": provider_id,
        "conversation_id": conversation_id,
        "user_message": user_message
    }
    
    # Preparar headers con la timezone
    headers = {
        "clienttimezone": timezone
    }
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)) as session:
        url = urljoin(base_url, "booking-assistant")
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return await _try_send_message(session, url, payload, headers, attempt)
            except aiohttp.ClientResponseError as e:
                if e.status == 500 and attempt < MAX_RETRIES:
                    logging.warning(f"Intento {attempt} falló con error 500. Reintentando...")
                    await asyncio.sleep(RETRY_DELAY * attempt)  # Delay exponencial
                    continue
                elif e.status == 500 and attempt == MAX_RETRIES:
                    error_msg = ("Lo siento, estamos experimentando dificultades técnicas en este momento. "
                               "Por favor, contacta a soporte técnico si el problema persiste.")
                    logging.error(f"Todos los reintentos fallaron: {str(e)}")
                    return error_msg
                else:
                    raise
            except Exception as e:
                logging.error(f"Error inesperado: {str(e)}")
                raise


