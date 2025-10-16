# 🌞 Astral2Mqtt MCP

Microservice de calcul et publication de données astronomiques complètes via l'architecture **MCP JSON-RPC over MQTT** pour NeurHomIA.

**Architecture MCP** : Protocole standardisé JSON-RPC 2.0 over MQTT pour une intégration native avec NeurHomIA.

**Bibliothèques** :
- [astral](https://astral.readthedocs.io/) : Calculs astronomiques précis
- [mcp-mqtt-sdk](https://pypi.org/project/mcp-mqtt-sdk/) : Communication MCP JSON-RPC
- [pydantic](https://pypi.org/project/pydantic/) : Validation des données

---

## 📦 Fonctionnalités

- **🔧 Architecture MCP JSON-RPC** : Communication standardisée JSON-RPC 2.0 sur MQTT
- **🛠️ Outils MCP** : 6 outils (`get_astronomical_data`, `add_location`, `list_locations`, `refresh_all_data`, `health_check`, `get_service_status`)
- **📋 Ressources MCP** : Page de gestion et widget astronomique avec découverte automatique
- **🌍 Multi-localisations** : Support illimité de localisations statiques et dynamiques
- **📊 Données Complètes** : Position solaire/lunaire, événements quotidiens, trajectoires, périodes spéciales
- **⚙️ Configuration Dynamique** : Ajout de localisations en temps réel
- **🏠 Intégration Native** : Compatible NeurHomIA et Home Assistant
- **📡 API Robuste** : JSON-RPC pour contrôle, requêtes et surveillance
- **🐳 Docker Ready** : Déploiement simplifié avec docker-compose

---
## 🚀 Démarrage Rapide

### Avec Docker (Recommandé)

```bash
git clone https://github.com/cce66/astral2mqtt.git
cd astral2mqtt
cp .env.example .env # Configurez votre fichier .env
docker-compose up -d
```

### Installation Manuelle

```bash
pip install -r requirements.txt
python -m src.astral2mqtt.main
```

Pour des instructions détaillées, consultez le [Guide d'Installation](INSTALL.md).

---

## 🔧 Configuration

### Variables d'Environnement

```bash
# Configuration MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=astral_user
MQTT_PASSWORD=astral_password

# Configuration des logs
LOG_LEVEL=INFO

# Configuration du service
ASTRAL_INTERVAL=3600
ASTRAL_HEARTBEAT_INTERVAL=30
```

### Fichier de Configuration

Le fichier `config/mqtt_config.yaml` configure le service :

```yaml
mqtt:
  broker: "localhost"
  port: 1883
  username: "astral_user"
  password: "astral_password"

astral:
  interval: 3600
  heartbeat_interval: 30
  locations:
    default:
      latitude: 48.8566
      longitude: 2.3522

discovery:
  enabled: true
```

---

## 📡 API MCP JSON-RPC

### Outils MCP Disponibles

#### `get_astronomical_data` (Récupération des données astronomiques)
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "get_astronomical_data",
    "arguments": {
      "location_name": "paris"
    }
  },
  "id": "req_001"
}
```

#### `add_location` (Ajout de localisation dynamique)
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "add_location",
    "arguments": {
      "location_name": "maison",
      "latitude": 48.8566,
      "longitude": 2.3522
    }
  },
  "id": "req_002"
}
```

### Topics MQTT MCP
```
mcp/astral2mqtt/jsonrpc/request     # Requêtes JSON-RPC vers le microservice
mcp/astral2mqtt/jsonrpc/response    # Réponses JSON-RPC du microservice
mcp/astral2mqtt/discovery           # Découverte du service
mcp/astral2mqtt/heartbeat           # Maintien de session
mcp/astral2mqtt/events              # Événements astronomiques
mcp/astral2mqtt/logs                # Logs du service
```

---

## 📚 Documentation

- [**Installation**](INSTALL.md) : Guide d'installation détaillé
- [**Configuration**](docs/configuration.md) : Configuration YAML et variables d'environnement
- [**API MQTT**](docs/mqtt-api.md) : API MCP JSON-RPC (outils, ressources, topics)
- [**Intégrations**](docs/integration.md) : Home Assistant et NeurHomIA
- [**Widgets**](docs/widgets.md) : Découverte et utilisation des widgets MCP
- [**Starter Kit MCP**](mcp-microservice-starter-kit/) : Guide pour créer vos propres microservices

---

## 📁 Structure du Projet
```
astral2mqtt/
├── src/astral2mqtt/
│   ├── main.py              # Point d'entrée du service
│   ├── mcp_service.py       # Service MCP principal
│   ├── astral_engine.py     # Moteur de calculs astronomiques
│   ├── config.py            # Chargement de configuration
│   ├── mcp_config.py        # Configuration MCP
│   └── mcp_logger.py        # Système de logging MCP
├── config/
│   └── mqtt_config.yaml     # Configuration MQTT et localisations
├── docs/                    # Documentation complète
├── mcp-microservice-starter-kit/  # Kit de démarrage MCP
├── docker-compose.yml       # Configuration Docker
└── README.md               # Ce fichier
```

---

## 📚 Dépendances

- Python 3.11+
- [mcp-mqtt-sdk](https://pypi.org/project/mcp-mqtt-sdk/) : SDK MCP JSON-RPC MQTT
- [astral](https://pypi.org/project/astral/) : Calculs astronomiques
- [pydantic](https://pypi.org/project/pydantic/) : Validation de données
- [pytz](https://pypi.org/project/pytz/) : Gestion des fuseaux horaires

---

## 💡 Cas d'Usage

- **NeurHomIA** : Interface de gestion complète avec widgets personnalisables
- **Éclairage intelligent** : Activation automatique au crépuscule civil
- **Volets roulants** : Ajustement selon l'azimut et l'élévation solaire
- **Tableaux de bord** : Affichage temps réel via événements MCP
- **Monitoring** : Surveillance de santé via heartbeat MCP
- **Automatisations lunaires** : Basées sur les phases de la lune
- **Gestion solaire** : Contrôle de stores selon trajectoire du soleil
- **Home Assistant** : Intégration domotique complète
- **Panneaux solaires** : Optimisation d'orientation et suivi

---

## 📜 Licence

MIT – Libre d'utilisation, de modification et de partage.

---

## ✨ Auteur : cce66
