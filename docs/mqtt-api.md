# 📡 Guide API MQTT

Ce document détaille l'API **MCP JSON-RPC over MQTT** d'Astral2Mqtt pour la configuration, le contrôle, la surveillance et la publication des données.

---

## 📊 Données et Événements MCP Publiés

Les données astronomiques sont publiées en tant qu'événements MCP sur le topic `mcp/astral2mqtt/events`.

### Événements Astronomiques

Chaque localisation génère des événements contenant toutes les données astronomiques :

### Exemple d'Événement Astronomique
```json
{
  "event_type": "astronomical_data",
  "data": {
    "location_name": "paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "timestamp": "2025-01-12T10:30:00Z",
    "current_elevation": 25.3,
    "current_azimuth": 134.2,
    "sunrise": "2025-01-12T07:30:00Z",
    "sunset": "2025-01-12T17:30:00Z",
    "solar_noon": "2025-01-12T12:30:00Z",
    "moon_phase": 0.75,
    "sun_trajectory": [
      {"time": "2025-01-12T07:30:00Z", "elevation": 0.5, "azimuth": 90.1},
      {"time": "2025-01-12T07:35:00Z", "elevation": 1.2, "azimuth": 90.8}
    ]
  }
}
```

---

## 🔐 API MCP JSON-RPC - Outils et Contrôle

Astral2Mqtt expose une API MCP JSON-RPC complète. Les requêtes sont envoyées sur `mcp/astral2mqtt/jsonrpc/request` et les réponses reçues sur `mcp/astral2mqtt/jsonrpc/response`.

### 🔧 Outil : `add_location` (Gestion des Localisations Dynamiques)

Permet d'ajouter ou modifier des localisations en temps réel.

#### Requête JSON-RPC pour `add_location`
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "add_location",
    "arguments": {
      "location_name": "maison",
      "latitude": 43.6047,
      "longitude": 1.4442
    }
  },
  "id": "req_add_location",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Réponse JSON-RPC pour `add_location`
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "message": "Localisation 'maison' ajoutée avec succès",
    "location_name": "maison",
    "latitude": 43.6047,
    "longitude": 1.4442
  },
  "id": "req_add_location"
}
```

### 🔧 Outil : `list_locations` (Lister les Localisations)

Récupère la liste de toutes les localisations configurées.

#### Requête JSON-RPC pour `list_locations`
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "list_locations",
    "arguments": {}
  },
  "id": "req_list_locations",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Réponse JSON-RPC pour `list_locations`
```json
{
  "jsonrpc": "2.0",
  "result": {
    "static_locations": {
      "default": { "latitude": 48.8566, "longitude": 2.3522, "type": "static" },
      "paris": { "latitude": 48.8566, "longitude": 2.3522, "type": "static" }
    },
    "dynamic_locations": {
      "maison": { "latitude": 43.6047, "longitude": 1.4442, "type": "dynamic" }
    },
    "total_count": 3
  },
  "id": "req_list_locations"
}
```

### 🔧 Outil : `get_astronomical_data` (Récupérer les Données Astronomiques)

Récupère les données astronomiques complètes pour une localisation.

#### Requête JSON-RPC pour `get_astronomical_data`
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
  "id": "req_get_data",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Réponse JSON-RPC pour `get_astronomical_data`
```json
{
  "jsonrpc": "2.0",
  "result": {
    "current_elevation": 25.3,
    "current_azimuth": 134.2,
    "sunrise": "2025-01-12T07:30:00Z",
    "sunset": "2025-01-12T17:30:00Z",
    "location_name": "paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "timestamp": "2025-01-12T10:30:00Z",
    ... (toutes les données astronomiques)
  },
  "id": "req_get_data"
}
```

### 🔧 Outil : `refresh_all_data` (Actualiser toutes les Données)

Déclenche un recalcul immédiat des données pour toutes les localisations.

#### Requête JSON-RPC pour `refresh_all_data`
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "refresh_all_data",
    "arguments": {}
  },
  "id": "req_refresh_data",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Réponse JSON-RPC pour `refresh_all_data`
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "message": "Données rafraîchies pour X localisations",
    "timestamp": "2025-01-12T10:30:00Z"
  },
  "id": "req_refresh_data"
}
```

### 🔧 Outil : `health_check` (Vérification de Santé MCP)

Vérifie l'état de santé du microservice selon les standards MCP.

#### Requête JSON-RPC pour `health_check`
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "health_check",
    "arguments": {}
  },
  "id": "req_health_check",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Réponse JSON-RPC pour `health_check`
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "healthy",
    "uptime": 3600,
    "version": "2.0.0",
    "static_locations_count": 2,
    "dynamic_locations_count": 1,
    "total_locations": 3,
    "dependencies": {
      "astral_library": "connected",
      "mqtt_broker": "connected"
    },
    "timestamp": "2025-01-12T10:30:00Z"
  },
  "id": "req_health_check"
}
```

### 🔧 Outil : `get_service_status` (Statut du Service)

Récupère le statut détaillé du service (alias pour compatibilité).

#### Requête JSON-RPC pour `get_service_status`
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "get_service_status",
    "arguments": {}
  },
  "id": "req_service_status",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Réponse JSON-RPC pour `get_service_status`
```json
{
  "jsonrpc": "2.0",
  "result": {
    "service_id": "astral2mqtt",
    "name": "Astral2MQTT Service",
    "version": "2.0.0",
    "status": "running",
    "static_locations_count": 2,
    "dynamic_locations_count": 1,
    "total_locations": 3,
    "update_interval": 3600,
    "heartbeat_interval": 300,
    "timestamp": "2025-01-12T10:30:00Z"
  },
  "id": "req_service_status"
}
```

### 📊 Surveillance du Service (Heartbeat MCP)

Le service publie automatiquement son heartbeat sur `mcp/astral2mqtt/heartbeat` pour la surveillance en temps réel.

```json
{
  "service_id": "astral2mqtt",
  "status": "alive",
  "uptime": 3600,
  "active_connections": 1,
  "last_activity": "2025-01-12T10:35:00Z",
  "timestamp": "2025-01-12T10:35:30Z"
}
```

---

## 🔐 Sécurité MCP JSON-RPC

Une sécurité appropriée est cruciale pour l'exposition des outils de commande.

### Authentification MCP

Chaque requête JSON-RPC doit inclure une section `auth` avec une `api_key` et le `service_id`.

```json
{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": { ... },
  "id": "req_001",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

### Configuration Recommandée du Broker MQTT (ACLs)

Configurez votre broker MQTT avec :

1.  **Authentification obligatoire** : Désactivez les connexions anonymes.
2.  **ACL (Access Control Lists)** : Contrôlez l'accès aux topics pour différents utilisateurs.

#### Exemple de Configuration ACL Mosquitto

```
# mosquitto.conf
allow_anonymous false
password_file /mosquitto/config/passwd # Chemin vers votre fichier de mots de passe
acl_file /mosquitto/config/acl         # Chemin vers votre fichier ACL
```

```
# /etc/mosquitto/acl
# Utilisateur admin - accès complet
user admin
topic readwrite mcp/astral2mqtt/#

# Utilisateur NeurHomIA
user neurhomia
topic readwrite mcp/astral2mqtt/jsonrpc/request
topic read mcp/astral2mqtt/jsonrpc/response
topic read mcp/astral2mqtt/events
topic read mcp/astral2mqtt/heartbeat
topic read mcp/astral2mqtt/discovery

# Utilisateur Home Assistant
user homeassistant
topic read mcp/astral2mqtt/events
topic read mcp/astral2mqtt/heartbeat
topic readwrite homeassistant/+/+/config
```

---

## 📋 Résumé des Topics et Outils MCP

| Type | Nom/Topic | Description | Accès Recommandé |
|------|-----------|-------------|------------------|
| **Outil** | `add_location` | Ajoute ou modifie une localisation dynamique | Admin/NeurHomIA |
| **Outil** | `list_locations` | Liste toutes les localisations configurées | Admin/NeurHomIA |
| **Outil** | `get_astronomical_data` | Récupère les données astronomiques pour une localisation | Tous |
| **Outil** | `refresh_all_data` | Recalcul forcé des données et republication des événements | Admin/NeurHomIA |
| **Outil** | `health_check` | Vérification de santé du microservice (standard MCP) | Tous |
| **Outil** | `get_service_status` | Récupère le statut détaillé du service | Tous |
| **Topic** | `mcp/astral2mqtt/jsonrpc/request` | Requêtes JSON-RPC vers le service | Dépend de l'outil appelé |
| **Topic** | `mcp/astral2mqtt/jsonrpc/response` | Réponses JSON-RPC du service | Dépend de la requête |
| **Topic** | `mcp/astral2mqtt/events` | Événements de données astronomiques | Tous |
| **Topic** | `mcp/astral2mqtt/heartbeat` | Statut du service (heartbeat) | Tous |
| **Topic** | `mcp/astral2mqtt/discovery` | Message de découverte du service | Tous |