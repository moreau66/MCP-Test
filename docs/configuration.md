# ⚙️ Guide de Configuration

Ce document fournit un guide détaillé pour configurer Astral2Mqtt avec l'architecture **MCP JSON-RPC over MQTT**.

---

## 📝 Configuration Hiérarchique

Le système de configuration suit une **hiérarchie de priorité** :

1. **Valeurs par défaut** (codées dans l'application) - Ces valeurs sont la base.
2. **Fichier YAML** (`config/mqtt_config.yaml`) - Les valeurs de ce fichier surchargent les valeurs par défaut.
3. **Variables d'environnement** (priorité maximale) - Les variables d'environnement surchargent toutes les configurations précédentes.
 
Cette approche permet une grande flexibilité selon votre environnement de déploiement.

---

## 📁 Fichier de Configuration YAML (Recommandé)

Le fichier `config/mqtt_config.yaml` est la méthode principale recommandée pour la configuration statique. Il doit être placé dans le répertoire `config/` relatif à la racine de l'application.

```yaml
# Configuration MQTT pour Astral2Mqtt
# Ce fichier peut être surchargé par les variables d'environnement

mqtt:
  broker: "mosquitto"
  port: 1883
  topic: "astral/data"
  username: null
  password: null
  client_id: "astral2mqtt"
  keepalive: 60
  qos: 0
  retain: false

astral:
  interval: 3600  # Intervalle de mise à jour en secondes
  heartbeat_interval: 300  # Intervalle du heartbeat en secondes (5 minutes)
  locations:
    default:
      latitude: 48.8566
      longitude: 2.3522
    paris:
      latitude: 48.8566
      longitude: 2.3522
    toulouse:
      latitude: 43.6047
      longitude: 1.4442
    montreal:
      latitude: 45.5019
      longitude: -73.5674

discovery:
  enabled: true
  device_name: "Astral MQTT Bridge" # Nom du périphérique pour la découverte
  manufacturer: "Microservices Suite"
  model: "Astral2Mqtt"
  sw_version: "1.0.0"
```

---

## 🌍 Variables d'Environnement (Priorité Maximale)

Les variables d'environnement ont la **priorité maximale** et sont recommandées pour :
- Les environnements conteneurisés (Docker, Kubernetes)
- La configuration sensible (mots de passe)
- Les déploiements automatisés

Vous pouvez définir les variables d'environnement directement dans votre shell avant d'exécuter l'application, ou dans votre fichier `docker-compose.yml`.

```bash
# Exemple : Définition des variables d'environnement dans le shell
export MQTT_BROKER="192.168.1.100"
export MQTT_PORT=1883
export MQTT_USER="admin"
export MQTT_PASS="password"
export MQTT_CLIENT_ID="astral2mqtt"

export ASTRAL_INTERVAL=1800
export ASTRAL_HEARTBEAT_INTERVAL=300

export DISCOVERY_ENABLED=true
export DISCOVERY_DEVICE_NAME="Astral Production"
```

### 📊 Tableau des Variables d'Environnement

| Variable | Description | Exemple | Section |
|----------|-------------|---------|---------|
| `MQTT_BROKER` | Adresse du broker MQTT | `"192.168.1.100"` | mqtt |
| `MQTT_PORT` | Port du broker MQTT | `1883` | mqtt |
| `MQTT_TOPIC` | Topic de base pour toutes les données publiées | `"astral/data"` | mqtt |
| `MQTT_USER` | Nom d'utilisateur MQTT pour l'authentification | `"admin"` | mqtt |
| `MQTT_PASS` | Mot de passe MQTT pour l'authentification | `"password"` | mqtt |
| `MQTT_CLIENT_ID` | ID client MQTT | `"astral2mqtt"` | mqtt |
| `MQTT_KEEPALIVE` | Intervalle keepalive MQTT (secondes) | `60` | mqtt |
| `MQTT_QOS` | Qualité de Service MQTT | `0` | mqtt |
| `MQTT_RETAIN` | Flag des messages retenus | `false` | mqtt |
| `ASTRAL_INTERVAL` | Intervalle de mise à jour des données (secondes) | `3600` | astral |
| `ASTRAL_HEARTBEAT_INTERVAL` | Intervalle de publication du heartbeat (secondes) | `300` | astral |
| `DISCOVERY_ENABLED` | Activer la découverte automatique | `true` | discovery |
| `LOG_LEVEL` | Niveau de log (DEBUG, INFO, WARNING, ERROR) | `"INFO"` | logging |
| `DISCOVERY_DEVICE_NAME` | Nom du périphérique pour la découverte | `"Astral MQTT Bridge"` | discovery |
| `DISCOVERY_MANUFACTURER` | Fabricant pour la découverte | `"Microservices Suite"` | discovery |
| `DISCOVERY_MODEL` | Modèle pour la découverte | `"Astral2Mqtt"` | discovery |
| `DISCOVERY_SW_VERSION` | Version logicielle pour la découverte | `"1.0.0"` | discovery |

---

## 🎯 Exemples de Configuration Complète

### Configuration pour Environnement de Production
```bash
# Configuration MQTT sécurisée
export MQTT_BROKER="192.168.1.100"
export MQTT_PORT=1883
export MQTT_USER="astral_service"
export MQTT_PASS="mot_de_passe_securise" # Utilisez la gestion des secrets en production
export MQTT_CLIENT_ID="astral2mqtt_prod"

# Configuration du service
export ASTRAL_INTERVAL=1800  # Mise à jour toutes les 30 minutes
export ASTRAL_HEARTBEAT_INTERVAL=300  # Heartbeat toutes les 5 minutes

# Découverte activée pour Home Assistant et NeurHome-IA
export DISCOVERY_ENABLED=true
export DISCOVERY_DEVICE_NAME="Astral Production"
```

### Configuration pour Développement/Test
```bash
# Configuration MQTT locale
export MQTT_BROKER="localhost"
export MQTT_PORT=1883
export MQTT_CLIENT_ID="astral2mqtt_dev"

# Mises à jour plus fréquentes pour les tests
export ASTRAL_INTERVAL=300  # Toutes les 5 minutes
export ASTRAL_HEARTBEAT_INTERVAL=60  # Heartbeat toutes les minutes

# Découverte désactivée pour éviter les conflits en développement
export DISCOVERY_ENABLED=false
```

---

## 📋 Fichier `config.json` (Hérité et Obsolète)

Le fichier `config.json` est obsolète. Utilisez le système YAML + variables d'environnement pour une meilleure flexibilité et sécurité.

```json
{
  "auth": {
    "username": "admin",
    "password": "admin"
  },
  "settings": {
    "interval": 60,
    "heartbeat_interval": 300
  },
  "mqtt": {
    "host": "mqtt.local",
    "port": 1883,
    "base_topic": "suncalc"
  },
  "locations": {
    "default": {
      "latitude": 48.8566,
      "longitude": 2.3522
    },
    "paris": {
      "latitude": 48.8566,
      "longitude": 2.3522
    },
    "toulouse": {
      "latitude": 43.6047,
      "longitude": 1.4442
    },
    "montreal": {
      "latitude": 45.5019,
      "longitude": -73.5674
    }
  },
  "homeassistant_discovery": {
    "enabled": true,
    "node_id": "astral2mqtt"
  }
}
```

---

## 🔧 Paramètres de Connexion MQTT

Ces paramètres définissent comment Astral2Mqtt se connecte à votre broker MQTT.

| Paramètre | Section | Description | Exemple | Notes |
|-----------|---------|-------------|---------|-------|
| `broker` | `mqtt` | Adresse IP ou nom d'hôte du broker MQTT | `"mosquitto"` ou `"192.168.1.100"` | Peut être surchargé par `MQTT_BROKER` |
| `port` | `mqtt` | Port de connexion du broker MQTT | `1883` (standard) ou `8883` (SSL) | Peut être surchargé par `MQTT_PORT` |
| `username` | `mqtt` | Nom d'utilisateur pour l'authentification MQTT | `"astral_user"` | Peut être surchargé par `MQTT_USERNAME` |
| `password` | `mqtt` | Mot de passe pour l'authentification MQTT | `"astral_password"` | Peut être surchargé par `MQTT_PASSWORD` |
| `client_id` | `mqtt` | ID client MQTT | `"astral2mqtt"` | Peut être surchargé par `MQTT_CLIENT_ID` |

---

## 🔍 Débogage de la Configuration

Le système de configuration enregistre son processus de chargement :
- Les sources de configuration chargées (défaut, YAML, variables d'environnement)
- Les surcharges appliquées par les variables d'environnement
- La configuration finale effective (avec masquage des données sensibles)

Les logs sont au format JSON structuré pour faciliter le débogage.

```bash
# Exemple de logs de configuration
INFO - Loading configuration with priority hierarchy:
INFO - 1. Default values (hardcoded)
INFO - 2. YAML configuration file
INFO - 3. Environment variables (highest priority)
INFO - Environment override: MQTT_BROKER -> mqtt.broker = 192.168.1.100
INFO - Final configuration: {'mqtt': {'broker': '192.168.1.100', 'password': '***MASKED***'}}
```

**Notes importantes :**
- 🔒 **Sécurité** : Changez toujours les identifiants par défaut (`admin`/`admin`) avant le déploiement en production.
- 🌐 **Réseau** : Assurez-vous que le broker MQTT est accessible depuis le conteneur Docker.
- 🔌 **Port** : Le port 1883 est standard pour MQTT non chiffré, 8883 pour MQTT sur SSL/TLS.

---

## 🌍 Gestion des Localisations

Astral2Mqtt prend en charge la gestion de **plusieurs localisations** avec deux approches complémentaires : configuration statique et mises à jour dynamiques via les outils MCP.
### 📍 Localisations Statiques (Fichier de Configuration)

Définies dans le fichier `config/mqtt_config.yaml` ou via les variables d'environnement, ces localisations sont chargées au démarrage du service. Elles sont idéales pour les localisations fixes et permanentes.

```yaml
astral:
  locations:
    paris:
      latitude: 48.8566
      longitude: 2.3522
    toulouse:
      latitude: 43.6047
      longitude: 1.4442
    montreal:
      latitude: 45.5019
      longitude: -73.5674
    ma_maison:
      latitude: 46.2276
      longitude: 2.2137
```

### ⚡ Localisations Dynamiques (MQTT)
Les localisations peuvent être ajoutées ou modifiées en temps réel via l'outil MCP `add_location` sans redémarrage du service.

Pour ajouter une localisation, envoyez une requête JSON-RPC :

```bash
# Ajouter une nouvelle localisation
mosquitto_pub -h <MQTT_BROKER_IP> -t "mcp/astral2mqtt/jsonrpc/request" -m '{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "add_location",
    "arguments": {
      "location_name": "bureau",
      "latitude": 45.764,
      "longitude": 4.8357
    }
  },
  "id": "req_add_bureau",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}'
```

### 🎛️ Interface Graphique (NeurHome-IA)

NeurHomIA découvre automatiquement le service et offre une interface graphique pour gérer les localisations :
- **Formulaire d'ajout** : Interface pour ajouter de nouvelles localisations.
- **Validation automatique** : Les contrôles de saisie pour la latitude (-90 à +90) et la longitude (-180 à +180) garantissent l'intégrité des données.
- **Gestion centralisée** : Vue d'ensemble de toutes les localisations configurées.

### 📊 Publication des Données par Localisation

Chaque localisation génère ses propres données astronomiques publiées en tant qu'événements MCP :

```json
{
  "event_type": "astronomical_data",
  "data": {
    "location_name": "paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "timestamp": "2025-01-12T10:30:00Z",
    "current_elevation": 25.3,
    "sunrise": "2025-01-12T07:30:00Z",
    ...
  }
}
```



