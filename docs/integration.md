# 🏠 Guide d'Intégration

Ce document fournit des informations détaillées sur l'intégration d'Astral2Mqtt avec NeurHomIA via l'architecture **MCP JSON-RPC over MQTT** et offre des exemples d'utilisation pratiques.

---

## 🏠 Intégration Home Assistant (Découverte MQTT)

Astral2Mqtt prend en charge la **découverte automatique MQTT de Home Assistant** pour une intégration transparente.

### 🔧 Configuration de la Découverte

La découverte est activée par défaut et peut être contrôlée via les variables d'environnement ou le fichier de configuration.

**Via variable d'environnement (recommandé) :**
```bash
export DISCOVERY_ENABLED=true
```

**Via fichier YAML (`config/mqtt_config.yaml`) :**
```yaml
discovery:
  enabled: true
```

| Paramètre | Description | Valeur par Défaut |
|-----------|-------------|-------------------|
| `enabled` | Active/désactive la découverte MQTT | `true` |

### 📊 Entités Créées Automatiquement

Pour chaque localisation configurée, les capteurs suivants sont automatiquement découverts dans Home Assistant :

#### ☀️ Capteurs Solaires
- **Élévation Solaire** : Position verticale du soleil (en degrés).
- **Azimut Solaire** : Position horizontale du soleil (en degrés).
- **Lever du Soleil** : Heure du lever du soleil.
- **Coucher du Soleil** : Heure du coucher du soleil.
- **Midi Solaire** : Heure du midi solaire.
- **Aube Civile** : Début de l'aube civile.
- **Crépuscule Civil** : Fin du crépuscule civil.

#### 🌙 Capteurs Lunaires
- **Phase Lunaire** : Phase actuelle de la lune (valeur numérique).
- **Élévation Lunaire** : Position verticale de la lune (en degrés).
- **Azimut Lunaire** : Position horizontale de la lune (en degrés).

### 🎯 Attributs Détaillés

Chaque capteur dans Home Assistant aura des **attributs étendus** contenant toutes les données astronomiques pour la localisation respective. Cela inclut :
- Trajectoire solaire complète (toutes les 5 minutes)
- Heures dorées et bleues
- Périodes de crépuscule (civil, nautique, astronomique)
- Lever/coucher de lune
- Rahukaalam
- Et bien plus...

### 🔍 Exemple d'Utilisation dans Home Assistant

Une fois découvertes, vous pouvez utiliser ces entités dans vos automatisations, tableaux de bord et scripts Home Assistant.

```yaml
automation:
  - alias: "Éclairage automatique au coucher du soleil"
    trigger:
      - platform: state
        entity_id: sensor.paris_solar_elevation # Exemple pour la localisation Paris
        to: "0" # Déclencher quand l'élévation du soleil atteint 0 degré (coucher du soleil)
    action:
      - service: light.turn_on
        target:
          entity_id: light.garden # Remplacez par votre entité lumière
```

### 🛠️ Désactiver la Découverte

Pour désactiver la découverte MQTT :

**Via variable d'environnement (recommandé) :**
```bash
export DISCOVERY_ENABLED=false
```

**Via fichier YAML (`config/mqtt_config.yaml`) :**
```yaml
discovery:
  enabled: false
```

---

## 🖥️ Intégration NeurHomIA (Pages Dynamiques)
Astral2Mqtt prend en charge la **découverte automatique** pour NeurHomIA via le protocole **MCP JSON-RPC over MQTT**, créant automatiquement une interface de gestion complète.

### 🔧 Configuration de Page Dynamique

La découverte est activée par défaut :

**Via variable d'environnement :**
```bash
export DISCOVERY_ENABLED=true
```

**Via fichier YAML (`config/mqtt_config.yaml`) :**
```yaml
discovery:
  enabled: true
```

### 📡 Topic de Découverte

Les messages de découverte sont publiés sur les topics MCP standardisés :

*   **Découverte de service** : `mcp/astral2mqtt/discovery`
*   **Heartbeat** : `mcp/astral2mqtt/heartbeat`
*   **Événements** : `mcp/astral2mqtt/events`

### 📋 Structure des Ressources MCP

Astral2Mqtt expose ses interfaces de gestion et ses widgets en tant que **ressources MCP** récupérables via des appels JSON-RPC.

#### Exemple de Récupération de la Page de Gestion (Requête JSON-RPC)

```json
{
  "jsonrpc": "2.0",
  "method": "mcp.get_resource",
  "params": {
    "resource_id": "astral2mqtt_management"
  },
  "id": "req_get_page",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

#### Exemple de Récupération du Schéma de Widget (Requête JSON-RPC)

```json
{
  "jsonrpc": "2.0",
  "method": "mcp.get_resource",
  "params": {
    "resource_id": "astral2mqtt_astronomy_widget"
  },
  "id": "req_get_widget_schema",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

Pour la structure détaillée de ces ressources (page de gestion et widget), veuillez consulter les méthodes `astral_management_page` et `astral_widget_schema` dans `src/astral2mqtt/mcp_service.py`.

### 🎛️ Interface Générée Automatiquement par NeurHomIA

NeurHomIA utilise ces ressources pour créer automatiquement :

*   **Une page de gestion complète** : Configuration des localisations, visualisation du statut
*   **Un widget astronomique** : Affichage des données astronomiques en temps réel

### 🔄 Publication des Événements

Les données astronomiques sont publiées en tant qu'événements MCP sur `mcp/astral2mqtt/events` pour les mises à jour en temps réel.

---

## 🛠️ Exemples d'Utilisation Pratiques

Ces exemples démontrent comment interagir avec Astral2Mqtt via les automatisations Home Assistant et les appels à l'API MCP JSON-RPC.

### 📱 Exemples d'Intégration Home Assistant

Vous pouvez utiliser les entités découvertes dans vos automatisations :

```yaml
# Éclairage automatique du jardin au coucher du soleil
automation:
  - alias: "Éclairage jardin au coucher du soleil"
    trigger:
      - platform: numeric_state
        entity_id: sensor.paris_solar_elevation # Exemple pour la localisation Paris
        below: 0
    action:
      - service: light.turn_on
        target:
          entity_id: light.garden
        data:
          brightness: 128

# Fermeture des volets basée sur l'azimut pour se protéger du soleil d'été
automation:
  - alias: "Protection soleil d'été"
    trigger:
      - platform: numeric_state
  - alias: "Éclairage jardin au coucher du soleil"
    trigger:
      - platform: numeric_state
        entity_id: sensor.paris_solar_elevation # Exemple pour la localisation Paris
        below: 0
    action:
      - service: light.turn_on
        target:
          entity_id: light.garden # Remplacez par votre entité lumière
```

### 🎛️ Exemples de Contrôle via l'API MCP JSON-RPC

Vous pouvez interagir directement avec Astral2Mqtt via des requêtes JSON-RPC :

```bash
# Ajouter une localisation
mosquitto_pub -h <MQTT_BROKER_IP> -t "mcp/astral2mqtt/jsonrpc/request" -m '{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "add_location",
    "arguments": {
      "location_name": "chalet",
      "latitude": 46.0207,
      "longitude": 7.7491
    }
  },
  "id": "req_add_chalet",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}'

# Actualiser les données
mosquitto_pub -h <MQTT_BROKER_IP> -t "mcp/astral2mqtt/jsonrpc/request" -m '{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "refresh_all_data",
    "arguments": {}
  },
  "id": "req_refresh",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}'

# Récupérer le statut du service
mosquitto_pub -h <MQTT_BROKER_IP> -t "mcp/astral2mqtt/jsonrpc/request" -m '{
  "jsonrpc": "2.0",
  "method": "mcp.call_tool",
  "params": {
    "tool_name": "health_check",
    "arguments": {}
  },
  "id": "req_health",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}'
```

### 📊 Exemple de Surveillance et Monitoring

Surveillez la santé du service via le heartbeat MCP :

```bash
# Surveillance du heartbeat
mosquitto_sub -h <MQTT_BROKER_IP> -t "mcp/astral2mqtt/heartbeat" -v

# Script Python pour surveillance automatique
import asyncio
from mcp_mqtt_sdk import MCPClient

async def monitor_astral_service():
    client = MCPClient(client_id="astral_monitor")
    await client.connect()

    async def heartbeat_handler(payload):
        print(f"Heartbeat reçu: {payload}")
        # Ici, vous pouvez ajouter votre logique d'alerte ou de traitement

    client.subscribe_heartbeat("astral2mqtt", heartbeat_handler)
    print("Abonné au heartbeat d'astral2mqtt. En attente de messages...")

    # Garder le client en vie
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(monitor_astral_service())
```