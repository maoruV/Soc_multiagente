import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

    # Gmail Configuration
    GOOGLE_APLICATION_CREDENTIALS = os.getenv("GOOGLE_APLICATION_CREDENTIALS")
    GMAIL_TOKEN = os.getenv("GMAIL_TOKEN")

    # SOC Configuration
    SOC_EMAIL_RECIPIENT = os.getenv("SOC_EMAIL_RECIPIENT")
    SOC_EMAIL_SENDER = os.getenv("SOC_EMAIL_SENDER")
    
    # APIs opcionales para threat intelligence
    # ABUSE_IP_DB_API_KEY = os.getenv("ABUSE_IP_DB_API_KEY")
    # URLVOID_API_KEY = os.getenv("URLVOID_API_KEY")
    
    # Configuracion del SOC
    WEBHOOK_PORT = 8000
    DASHBOARD_PORT = 8501
    
    # Validacion de configuracion critica
    @classmethod
    def validate_required_config(cls):
        """Valida que la configuracion critica este completa"""
        required_keys = [
           ( "GROQ_API_KEY", cls.GROQ_API_KEY),
           ( "TAVILY_API_KEY", cls.TAVILY_API_KEY),
           ( "VIRUSTOTAL_API_KEY", cls.VIRUSTOTAL_API_KEY)
        ]
        missing_keys = [key for key, value in required_keys if not value]
        if missing_keys:
            raise ValueError(f"Variables de entorno requeridas no configuradas: {', '.join(missing_keys)}")
        
        return True
    
config = Config()