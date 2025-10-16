📱 Bluetooth2MQTT MCP

Une passerelle intelligente entre Bluetooth et MQTT compatible avec l'architecture NeurHomIA MCP JSON-RPC over MQTT
🎯 Aperçu

Bluetooth2MQTT MCP est une passerelle avancée entre vos périphériques Bluetooth et un broker MQTT, entièrement compatible avec l'architecture MCP (Model Context Protocol) JSON-RPC over MQTT de NeurHomIA. Elle permet de surveiller, gérer et contrôler vos périphériques Bluetooth via une API standardisée, parfait pour l'intégration dans des systèmes de domotique intelligents.
✨ Fonctionnalités MCP 2.0

    🔄 JSON-RPC 2.0 : API standardisée pour toutes les interactions Bluetooth
    🔍 Auto-découverte : Publication automatique des capacités du service
    💓 Heartbeat : Surveillance de l'état du service en temps réel
    🛠️ Outils MCP : 12 outils Bluetooth exposés via l'API standardisée
    📊 Ressources MCP : Widgets et pages configurables dynamiquement
    🔐 Authentification : Système d'API keys intégré avec permissions granulaires
    📡 Événements : Publication d'événements Bluetooth en temps réel
    📱 Périphériques Gérés : Système de gestion similaire aux localisations d'Astral2Mqtt
    🎯 Données Par Périphérique : Topics MQTT individuels pour chaque périphérique géré
    🎛️ Widgets Dynamiques : Génération automatique de widgets pour chaque périphérique
    🔗 Appairage Bluetooth : Gestion complète de l'appairage et de la connexion
    🏠 Découverte automatique Home Assistant
    📝 Logs structurés JSON avec contexte MCP

🏗️ Architecture MCP

┌─────────────┐    JSON-RPC     ┌─────────────┐    JSON-RPC     ┌─────────────────────┐
│  NeurHomIA  │◄───over MQTT───►│ Broker MQTT │◄───over MQTT───►│ Bluetooth2MQTT MCP  │
│  (Frontend) │                 │  (Mosquitto)│                 │     (Service)       │
└─────────────┘                 └─────────────┘                 └─────────────────────┘
                                                                           │
                                                                           ▼
                                                                 ┌─────────────────────┐
                                                                 │ Périphériques       │
                                                                 │ Bluetooth (BLE)     │
                                                                 │ • Smartphones       │
                                                                 │ • Montres           │
                                                                 │ • Écouteurs         │
                                                                 │ • Capteurs IoT      │
                                                                 └─────────────────────┘

🚀 Installation rapide
Avec Docker Compose (Recommandé)

# Cloner le repository
git clone https://github.com/moreau66/Bluetooth2Mqtt.git
cd Bluetooth2Mqtt

# Lancer le service MCP
docker-compose up -d

Installation Manuelle

# Installer les dépendances MCP
pip install -r requirements.txt

# Lancer le service MCP
python src/main.py

📡 API MCP Disponible
🔧 Outils MCP (Tools)
Outil 	Description 	Permissions 	Paramètres
trigger_scan 	Déclenche un scan Bluetooth manuel 	bluetooth:read 	-
update_scan_config 	Met à jour la configuration du scanner 	bluetooth:config 	scan_duration, scan_interval
add_managed_device 	Ajoute un nouveau périphérique géré 	bluetooth:admin 	mac_address, name, device_type, etc.
update_managed_device 	Met à jour un périphérique géré 	bluetooth:admin 	mac_address, name, device_type, etc.
remove_managed_device 	Supprime un périphérique géré 	bluetooth:admin 	mac_address
list_managed_devices 	Liste tous les périphériques gérés 	bluetooth:read 	-
get_managed_devices_summary 	Résumé des périphériques gérés 	bluetooth:read 	-
pair_device 	Appaire un périphérique Bluetooth 	bluetooth:admin 	mac_address, pin
unpair_device 	Supprime l'appairage d'un périphérique 	bluetooth:admin 	mac_address
connect_device 	Connecte un périphérique appairé 	bluetooth:admin 	mac_address
disconnect_device 	Déconnecte un périphérique 	bluetooth:admin 	mac_address
get_device_info 	Informations détaillées d'un périphérique 	bluetooth:read 	mac_address
start_discovery 	Démarre la découverte pour l'appairage 	bluetooth:admin 	duration
get_paired_devices 	Liste des périphériques appairés 	bluetooth:read 	-
get_service_status 	Statut complet du service 	bluetooth:read 	-
📊 Ressources MCP (Resources)
Ressource 	Type 	Description
bluetooth_dynamic_page 	Page 	Page de gestion complète Bluetooth
bluetooth_widget_template 	Widget 	Template de widget pour périphériques gérés
🔐 Permissions Granulaires

Le système implémente trois niveaux de permissions :

    bluetooth:read : Lecture des données et statuts (neurhomia, test_client, monitoring)
    bluetooth:config : Modification de la configuration (neurhomia, admin)
    bluetooth:admin : Administration complète (neurhomia, admin)

🔄 Exemples d'Utilisation MCP
Requête JSON-RPC : Ajouter un périphérique géré

{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "add_managed_device",
    "arguments": {
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "name": "Mon iPhone",
      "device_type": "smartphone",
      "presence_timeout": 300
    }
  },
  "id": "req_001",
  "auth": {
    "api_key": "mcp_bluetooth2mqtt_api_key_123456",
    "service_id": "neurhomia"
  }
}

Réponse JSON-RPC

{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "message": "Périphérique Mon iPhone ajouté avec succès",
    "device": {
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "name": "Mon iPhone",
      "device_type": "smartphone",
      "present": false,
      "paired": false,
      "connected": false,
      "presence_timeout": 300
    }
  },
  "id": "req_001"
}

📋 Topics MQTT MCP
Structure des Topics

mcp/bluetooth2mqtt/
├── jsonrpc/
│   ├── request          # Requêtes JSON-RPC vers le service
│   └── response         # Réponses JSON-RPC du service
├── discovery            # Auto-découverte du service
├── heartbeat           # Battement de cœur du service
├── events              # Événements Bluetooth en temps réel
└── logs                # Logs structurés JSON

Topics de Données par Périphérique

Chaque périphérique géré génère ses propres topics :

bluetooth/device/AABBCCDDEEFF/presence     # home/not_home
bluetooth/device/AABBCCDDEEFF/rssi         # -45 dBm
bluetooth/device/AABBCCDDEEFF/paired       # true/false
bluetooth/device/AABBCCDDEEFF/connected    # true/false
bluetooth/device/AABBCCDDEEFF/last_seen    # 2025-01-27T10:30:00Z
bluetooth/device/AABBCCDDEEFF              # Données JSON complètes

🔧 Configuration MCP
Fichier config/mqtt_config.yaml

mcp:
  service_id: "bluetooth2mqtt"
  name: "Bluetooth2MQTT MCP Service"
  version: "1.0.0"
  api_key: "mcp_bluetooth2mqtt_api_key_123456"
  allowed_clients: ["neurhomia", "test_client"]
  heartbeat_interval: 30
  discovery_enabled: true
  events_enabled: true

mqtt:
  broker: "mosquitto"
  port: 1883
  topic: "mcp"
  username: null
  password: null
  client_id: "mcp_bluetooth2mqtt"
  qos: 1
  retain: false
  keepalive: 60

bluetooth:
  scan_duration: 10
  scan_interval: 30
  filter_mode: "disabled"
  filter_mac_addresses: []
  filter_names: []
  filter_addr_types: []
  log_level: "INFO"
  managed_devices: []

discovery:
  enabled: true
  device_name: "Bluetooth MQTT Bridge"
  manufacturer: "Microservices Suite"
  prefix: "homeassistant"
  node_id: "bluetooth2mqtt"
  update_interval: 60

Variables d'Environnement MCP

# Configuration MCP
MCP_SERVICE_ID=bluetooth2mqtt
MCP_VERSION=1.0.0
MCP_API_KEY=mcp_bluetooth2mqtt_api_key_123456
MCP_ALLOWED_CLIENTS=neurhomia,test_client

# Configuration MQTT MCP
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USER=mcp_user
MQTT_PASS=mcp_password

# Configuration Bluetooth
BLUETOOTH_SCAN_DURATION=10
BLUETOOTH_SCAN_INTERVAL=30
BLUETOOTH_FILTER_MODE=disabled

# Configuration des fonctionnalités MCP
MCP_HEARTBEAT_INTERVAL=30
MCP_DISCOVERY_ENABLED=true
MCP_EVENTS_ENABLED=true
DISCOVERY_ENABLED=true

🧪 Tests et Développement
Client de Test MCP

# Lancer le client de test
python src/examples/mcp_client_test.py

Le client de test démontre :

    ✅ Connexion MCP via MQTT
    ✅ Authentification avec API key
    ✅ Appel de tous les outils Bluetooth disponibles
    ✅ Récupération des ressources (page dynamique, widgets)
    ✅ Écoute des événements Bluetooth en temps réel
    ✅ Gestion des périphériques gérés
    ✅ Appairage et connexion de périphériques

🔍 Monitoring et Debugging
Health Check MCP

{
  "jsonrpc": "2.0",
  "method": "mcp.health_check",
  "params": {},
  "id": "health_001",
  "auth": {
    "api_key": "mcp_bluetooth2mqtt_api_key_123456",
    "service_id": "neurhomia"
  }
}

Heartbeat Automatique

Le service publie automatiquement un heartbeat toutes les 30 secondes :

{
  "service_id": "bluetooth2mqtt",
  "status": "alive",
  "uptime": 3600,
  "active_connections": 2,
  "managed_devices": {
    "total": 3,
    "present": 2,
    "paired": 2,
    "connected": 1
  },
  "last_activity": "2025-01-27T10:35:00Z",
  "timestamp": "2025-01-27T10:35:30Z"
}

Logs Structurés JSON

{
  "timestamp": "2025-01-27T10:30:00.123456Z",
  "level": "INFO",
  "service": "bluetooth2mqtt",
  "message": "Périphérique découvert : iPhone de Jean (AA:BB:CC:DD:EE:FF)",
  "module": "bluetooth_scanner",
  "function": "on_device_discovered",
  "line": 142,
  "mcp_context": {
    "action": "device_discovery",
    "device_mac": "AA:BB:CC:DD:EE:FF",
    "rssi": -45
  }
}

🔐 Sécurité MCP
Authentification

Chaque requête MCP doit inclure une section auth :

{
  "auth": {
    "api_key": "mcp_bluetooth2mqtt_api_key_123456",
    "service_id": "neurhomia",
    "timestamp": "2025-01-27T10:30:00Z"
  }
}

Codes d'Erreur Standardisés
Code 	Message 	Description
-32001 	Unauthorized 	Authentification requise
-32002 	Forbidden 	Permissions insuffisantes
-32602 	Invalid params 	Paramètres invalides
-32603 	Internal error 	Erreur interne
🚀 Déploiement Production
Docker Compose Production

version: '3.8'

services:
  bluetooth2mqtt-mcp:
    build: .
    container_name: bluetooth2mqtt-mcp
    restart: unless-stopped
    
    # Accès au Bluetooth de l'hôte
    privileged: true
    network_mode: host
    
    environment:
      - MCP_API_KEY=${MCP_API_KEY}
      - MQTT_BROKER=${MQTT_BROKER}
      - MQTT_USER=${MQTT_USER}
      - MQTT_PASS=${MQTT_PASS}
      - BLUETOOTH_SCAN_DURATION=15
      - BLUETOOTH_SCAN_INTERVAL=60
      - DISCOVERY_ENABLED=true
    
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
      - ./data:/app/data
    
    # Accès aux périphériques Bluetooth
    devices:
      - /dev/bus/usb:/dev/bus/usb
    
    # Capacités nécessaires pour Bluetooth
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
    
    labels:
      - "com.bluetooth2mqtt.mcp.service=true"

📚 Documentation détaillée

    📖 Guide d'installation complet
    ⚙️ Configuration détaillée
    📡 API MQTT
    🎨 Widgets
    🔌 Intégrations

🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre guide de contribution.
📄 Licence

MIT - Libre d'utilisation, modification et partage.

Bluetooth2MQTT MCP 1.0 - La passerelle Bluetooth nouvelle génération pour NeurHomIA ! 🚀
✨ Auteur

Créé par cce66 pour l'écosystème NeurHomIA 🏠
