#!/usr/bin/env python3
"""
Template de base pour un microservice MCP JSON-RPC over MQTT
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional

from mcp_mqtt_sdk import MCPMicroservice, mcp_tool, mcp_resource
from config import config

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BasicMicroservice(MCPMicroservice):
    """
    Template de microservice MCP de base.
    
    Ce template fournit une structure de base pour créer des microservices
    compatibles avec l'architecture MCP JSON-RPC over MQTT.
    """
    
    def __init__(self):
        """Initialise le microservice avec la configuration."""
        super().__init__(
            service_id=config.SERVICE_ID,
            mqtt_host=config.MQTT_BROKER_HOST,
            mqtt_port=config.MQTT_BROKER_PORT,
            mqtt_username=config.MQTT_USERNAME,
            mqtt_password=config.MQTT_PASSWORD,
            api_key=config.API_KEY
        )
        
        # État interne du microservice
        self.state = {}
        self.start_time = time.time()
        self.request_count = 0
        
        logger.info(f"Microservice {config.SERVICE_ID} initialisé")
    
    def get_service_metadata(self) -> Dict[str, Any]:
        """Retourne les métadonnées du microservice."""
        return {
            "service_id": config.SERVICE_ID,
            "name": "Microservice de Base",
            "description": "Template de base pour microservices MCP",
            "version": "1.0.0",
            "protocol_version": "1.0",
            "author": "Votre Nom",
            "category": "utility",
            "tags": ["template", "basic", "utility"]
        }
    
    @mcp_tool(
        name="health.check",
        description="Vérifie l'état de santé du microservice",
        category="monitoring",
        permissions=["basic"]
    )
    def health_check(self) -> Dict[str, Any]:
        """
        Vérifie l'état de santé du microservice.
        
        Returns:
            Dict contenant les informations de santé
        """
        uptime = time.time() - self.start_time
        
        health_info = {
            "status": "healthy",
            "service_id": config.SERVICE_ID,
            "version": "1.0.0",
            "uptime_seconds": round(uptime, 2),
            "request_count": self.request_count,
            "timestamp": datetime.now().isoformat(),
            "memory_usage_mb": self._get_memory_usage(),
            "cpu_usage_percent": self._get_cpu_usage()
        }
        
        self.request_count += 1
        logger.info(f"Health check effectué: {health_info}")
        
        return health_info
    
    @mcp_tool(
        name="echo.message",
        description="Retourne le message fourni en écho",
        category="utility",
        permissions=["basic"]
    )
    def echo_message(self, message: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Retourne le message fourni en écho avec des métadonnées.
        
        Args:
            message: Le message à répéter
            metadata: Métadonnées optionnelles à inclure
            
        Returns:
            Dict contenant le message et les métadonnées
        """
        self.request_count += 1
        
        response = {
            "echo": message,
            "timestamp": datetime.now().isoformat(),
            "service_id": config.SERVICE_ID,
            "request_number": self.request_count
        }
        
        if metadata:
            response["metadata"] = metadata
        
        logger.info(f"Echo traité: {message[:50]}...")
        
        return response
    
    @mcp_tool(
        name="state.set",
        description="Définit une valeur dans l'état du microservice",
        category="utility",
        permissions=["state:write"]
    )
    def set_state(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Définit une valeur dans l'état du microservice.
        
        Args:
            key: Clé de l'état
            value: Valeur à stocker
            
        Returns:
            Dict confirmant la mise à jour
        """
        self.state[key] = value
        self.request_count += 1
        
        logger.info(f"État mis à jour: {key} = {value}")
        
        return {
            "status": "updated",
            "key": key,
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    @mcp_tool(
        name="state.get",
        description="Récupère une valeur de l'état du microservice",
        category="utility",
        permissions=["state:read"]
    )
    def get_state(self, key: str, default: Any = None) -> Dict[str, Any]:
        """
        Récupère une valeur de l'état du microservice.
        
        Args:
            key: Clé de l'état à récupérer
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            Dict contenant la valeur
        """
        value = self.state.get(key, default)
        self.request_count += 1
        
        return {
            "key": key,
            "value": value,
            "exists": key in self.state,
            "timestamp": datetime.now().isoformat()
        }
    
    @mcp_resource(
        uri="service/status",
        name="Statut du Service",
        description="Informations complètes sur l'état du microservice",
        mimeType="application/json",
        resourceType="data"
    )
    def get_service_status(self) -> Dict[str, Any]:
        """
        Ressource fournissant l'état complet du microservice.
        
        Returns:
            Dict contenant toutes les informations de statut
        """
        uptime = time.time() - self.start_time
        
        return {
            "service_info": self.get_service_metadata(),
            "runtime": {
                "uptime_seconds": round(uptime, 2),
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "current_time": datetime.now().isoformat(),
                "request_count": self.request_count
            },
            "state": {
                "keys_count": len(self.state),
                "keys": list(self.state.keys())
            },
            "system": {
                "memory_usage_mb": self._get_memory_usage(),
                "cpu_usage_percent": self._get_cpu_usage()
            }
        }
    
    def _get_memory_usage(self) -> float:
        """Retourne l'utilisation mémoire approximative."""
        try:
            import psutil
            process = psutil.Process()
            return round(process.memory_info().rss / 1024 / 1024, 2)
        except ImportError:
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Retourne l'utilisation CPU approximative."""
        try:
            import psutil
            return round(psutil.cpu_percent(interval=0.1), 2)
        except ImportError:
            return 0.0
    
    def on_shutdown(self):
        """Appelé lors de l'arrêt du microservice."""
        logger.info(f"Arrêt du microservice {config.SERVICE_ID}")
        logger.info(f"Statistiques finales: {self.request_count} requêtes traitées")

if __name__ == "__main__":
    # Création et démarrage du microservice
    service = BasicMicroservice()
    
    try:
        logger.info(f"Démarrage du microservice {config.SERVICE_ID}")
        service.run()
    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}")
    finally:
        service.on_shutdown()