import vt
from langchain_tavily import TavilySearch
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    get_gmail_credentials,
    build_resource_service
)
from langchain.tools import tool
from config import config
from datetime import datetime, timedelta

# Validar configuracion al importar
config.validate_required_config()

# 1. TavilySearch - Herramienta pre-construida
search_tool = TavilySearch(
    max_results=3,
    tavily_api_key=config.TAVILY_API_KEY
)

# 2. GmailTools - herramienta pre-construida
cred = get_gmail_credentials(
    token_file=config.GMAIL_TOKEN,
    client_sercret_file=config.GOOGLE_APLICATION_CREDENTIALS,
    scopes=["https://mail.google.com/"]
)


gmail_toolkit = GmailToolkit(api_resource=build_resource_service(credentials=cred) )
gmail_tools = gmail_toolkit.get_tools()

# 3. VirusTotal - herramienta personalizada
@tool
def virustotal_checker(indicator: str, indicator_type: str) -> str:
    """
    Realiza una busqueda en VirusTotal para obtener informacion sobre un indicador de interes.
    
    Args:
        indicator: El indicador a analizar (IP, dominio, URL o hash)
        indicator_type: El tipo de indicador ('ip', 'url' o 'hash')
    """
    try:
        with vt.Client(config.VIRUSTOTAL_API_KEY) as client:
        
            # Determinar el tipo de busqueda
            if indicator_type == 'ip':
                analysis = client.get_object(f'/ip-addresses/{indicator}')
            elif indicator_type == 'url':
                analysis = client.get_object(f'/urls/{indicator}')
            elif indicator_type == 'hash':
                analysis = client.get_object(f'/files/{indicator}')
            else:
                return f"Tipo de indicador no soportado: {indicator_type}"
            
            # Obtener estadisticas relevantes
            stats = analysis.last_analysis_stats
            malicious = stats.get('malicious', 0)
            suspicious = stats.get("suspicious", 0)
            total = sum(stats.values())
            
            if malicious > 5:
                theat_level = "MALICIOSO"
            elif suspicious > 0 or suspicious > 3:
                threat_level = "SOSPECHOSO"
            else:
                threat_level = "LIMPIO"
            
            return f"""ANALISIS VIRUTOTAL
            Indicador: {indicator}
            Detecciones: {malicious} de {total} motores
            Clasificacion: {threat_level}
            Analisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            
    except Exception as e:
        return f"Error en VirusTotal: {str(e)}"
    
# 4. Treat Intelligence - herramientas personalizadas

    
# Lista de herramientas disponibles
tools = [search_tool, virustotal_checker] + gmail_tools

