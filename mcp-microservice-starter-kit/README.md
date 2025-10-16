# MCP Microservice Starter Kit

Guide de démarrage rapide pour développer des microservices compatibles avec l'architecture MCP JSON-RPC over MQTT de NeurHomIA.

## 🚀 Démarrage rapide

### 1. Installation

```bash
# Cloner ce starter-kit
git clone <repository-url>
cd mcp-microservice-starter-kit

# Installer le SDK Python
pip install mcp-mqtt-sdk

# Copier le template de base
cp templates/basic_microservice.py my_service.py
cp templates/config.py .
```

### 2. Configuration

```python
# config.py
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
SERVICE_ID = "my-unique-service"
API_KEY = "your-secure-api-key"
```

### 3. Premier microservice

```python
from mcp_mqtt_sdk import MCPMicroservice, mcp_tool

class MyService(MCPMicroservice):
    
    @mcp_tool(
        name="hello.world",
        description="Retourne un message de bienvenue",
        category="utility"
    )
    def hello_world(self, name: str = "World") -> dict:
        return {"message": f"Hello, {name}!"}

if __name__ == "__main__":
    service = MyService("my-service")
    service.run()
```

### 4. Lancement

```bash
python my_service.py
```

## 📚 Documentation

- [`QUICKSTART.md`](./QUICKSTART.md) - Guide pas-à-pas détaillé
- [`API_REFERENCE.md`](./API_REFERENCE.md) - Documentation complète de l'API
- [`EXAMPLES.md`](./EXAMPLES.md) - Exemples pratiques
- [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md) - Résolution des problèmes

## 🏗️ Structure du projet

```
mcp-microservice-starter-kit/
├── schemas/           # Schémas JSON de validation
├── templates/         # Templates de code
├── tools/            # Outils de développement
├── examples/         # Exemples complets
└── docs/            # Documentation détaillée
```

## 🔧 Outils inclus

- **Validateur** : `python tools/validate_microservice.py`
- **Client de test** : `python tools/test_client.py`
- **Moniteur MQTT** : `python tools/mqtt_monitor.py`

## 📦 Exemples disponibles

- **Calculatrice simple** : `examples/simple_calculator/`
- **Capteurs IoT** : `examples/iot_sensors/`
- **Domotique** : `examples/home_automation/`
- **Station météo** : `examples/weather_station/`

## 🛡️ Sécurité

- Authentification par clé API
- Chiffrement des communications
- Validation des permissions par méthode

## 📞 Support

- Documentation officielle : [docs/PRECONISATIONS.md](../PRECONISATIONS.md)
- Exemples de microservices : [GitHub Repository]
- Communauté : [Discord/Forum]