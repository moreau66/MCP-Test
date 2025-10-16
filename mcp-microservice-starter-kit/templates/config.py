"""
Configuration pour les microservices MCP
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration centralisée pour les microservices MCP."""
    
    # Configuration MQTT
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_USERNAME: str = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "")
    MQTT_QOS: int = int(os.getenv("MQTT_QOS", "1"))
    MQTT_RETAIN: bool = os.getenv("MQTT_RETAIN", "false").lower() == "true"
    
    # Configuration du service
    SERVICE_ID: str = os.getenv("SERVICE_ID", "basic-microservice")
    API_KEY: str = os.getenv("API_KEY", "change-this-secure-key")
    
    # Configuration de la découverte
    DISCOVERY_INTERVAL: int = int(os.getenv("DISCOVERY_INTERVAL", "30"))
    HEARTBEAT_INTERVAL: int = int(os.getenv("HEARTBEAT_INTERVAL", "10"))
    
    # Configuration des logs
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")  # "json" ou "text"
    
    # Configuration de sécurité
    ENABLE_AUTHENTICATION: bool = os.getenv("ENABLE_AUTHENTICATION", "true").lower() == "true"
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    # Configuration du monitoring
    MONITORING_ENABLED: bool = os.getenv("MONITORING_ENABLED", "true").lower() == "true"
    METRICS_INTERVAL: int = int(os.getenv("METRICS_INTERVAL", "30"))
    HEALTH_CHECK_ENABLED: bool = os.getenv("HEALTH_CHECK_ENABLED", "true").lower() == "true"
    
    # Configuration du cache
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL_DEFAULT: int = int(os.getenv("CACHE_TTL_DEFAULT", "300"))
    
    # Configuration des timeouts
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    RESPONSE_TIMEOUT: int = int(os.getenv("RESPONSE_TIMEOUT", "30"))
    
    # Configuration Docker (pour les microservices conteneurisés)
    CONTAINER_NAME: Optional[str] = os.getenv("CONTAINER_NAME")
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
    
    # Configuration de développement
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    MOCK_EXTERNAL_SERVICES: bool = os.getenv("MOCK_EXTERNAL_SERVICES", "false").lower() == "true"
    
    def __post_init__(self):
        """Validation et normalisation de la configuration."""
        # Validation du service_id
        if not self.SERVICE_ID or not self.SERVICE_ID.replace("-", "").replace("_", "").isalnum():
            raise ValueError("SERVICE_ID doit contenir uniquement des lettres, chiffres, tirets et underscores")
        
        # Validation de l'API key
        if self.ENABLE_AUTHENTICATION and len(self.API_KEY) < 8:
            raise ValueError("API_KEY doit contenir au moins 8 caractères")
        
        # Validation des intervalles
        if self.DISCOVERY_INTERVAL < 5:
            raise ValueError("DISCOVERY_INTERVAL doit être d'au moins 5 secondes")
        
        if self.HEARTBEAT_INTERVAL < 5:
            raise ValueError("HEARTBEAT_INTERVAL doit être d'au moins 5 secondes")
    
    def get_mqtt_topics(self) -> dict:
        """Retourne les topics MQTT pour ce service."""
        return {
            "discovery": f"mcp/discovery/{self.SERVICE_ID}",
            "heartbeat": f"mcp/heartbeat/{self.SERVICE_ID}",
            "request": f"mcp/services/{self.SERVICE_ID}/jsonrpc/request",
            "response": f"mcp/services/{self.SERVICE_ID}/jsonrpc/response",
            "events": f"mcp/events/{self.SERVICE_ID}",
            "logs": f"mcp/logs/{self.SERVICE_ID}",
            "metrics": f"mcp/metrics/{self.SERVICE_ID}"
        }
    
    def get_permissions_config(self) -> dict:
        """Retourne la configuration des permissions."""
        return {
            "basic": ["health.check", "echo.message"],
            "state:read": ["state.get"],
            "state:write": ["state.set"],
            "admin": ["*"]  # Accès à toutes les méthodes
        }
    
    def to_dict(self) -> dict:
        """Convertit la configuration en dictionnaire."""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

# Instance globale de configuration
config = Config()

# Configuration spécifique pour différents environnements
class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement."""
    DEBUG_MODE: bool = True
    LOG_LEVEL: str = "DEBUG"
    MOCK_EXTERNAL_SERVICES: bool = True
    RATE_LIMIT_ENABLED: bool = False

class ProductionConfig(Config):
    """Configuration pour l'environnement de production."""
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "INFO"
    MOCK_EXTERNAL_SERVICES: bool = False
    RATE_LIMIT_ENABLED: bool = True

class TestingConfig(Config):
    """Configuration pour les tests."""
    DEBUG_MODE: bool = True
    LOG_LEVEL: str = "DEBUG"
    MOCK_EXTERNAL_SERVICES: bool = True
    RATE_LIMIT_ENABLED: bool = False
    SERVICE_ID: str = "test-microservice"

def get_config_for_environment(env: str = None) -> Config:
    """
    Retourne la configuration appropriée selon l'environnement.
    
    Args:
        env: Environnement cible ("development", "production", "testing")
        
    Returns:
        Instance de configuration appropriée
    """
    env = env or os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()