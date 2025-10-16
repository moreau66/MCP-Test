# 🎛️ Découverte de Widgets pour Gestionnaire

Astral2Mqtt prend en charge la **découverte de widgets** pour NeurHomIA via le protocole **MCP JSON-RPC over MQTT**, permettant la création automatique d'interfaces utilisateur pour les données astronomiques.

> ✅ **Implémenté** : Cette fonctionnalité est entièrement implémentée dans le code et activée par défaut.

---

## 🏷️ Nom du Widget

Le widget est identifié comme **"Astral2MQTT Astronomy Widget"** dans l'écosystème MCP.

---

## 📡 Découverte de la Ressource Widget

Le schéma du widget est exposé en tant que **ressource MCP** et peut être récupéré par NeurHomIA via un appel JSON-RPC.

#### Requête JSON-RPC pour récupérer le schéma de widget
```json
{
  "jsonrpc": "2.0",
  "method": "mcp.get_resource",
  "params": {
    "resource_id": "astral_widget_schema"
  },
  "id": "req_get_widget_schema",
  "auth": {
    "api_key": "votre_api_key",
    "service_id": "astral2mqtt"
  }
}
```

---

## 📋 Structure du Schéma de Widget (Ressource MCP)

Le schéma de widget est défini dans `src/astral2mqtt/mcp_service.py` et contient toutes les informations nécessaires pour créer dynamiquement le widget.

#### Extrait du schéma de widget (pour illustration)
```json
{
  "resource_type": "widget",
  "resource_id": "astral_widget_schema",
  "name": "Astral2MQTT Astronomy Widget",
  "version": "2.0.0",
  "config": {
    "id": "astral2mqtt-astronomy-v2",
    "name": "Données Astronomiques",
    "description": "Widget d'affichage des données astronomiques complètes",
    "display": {
      "icon": "🌙",
      "primaryColor": "hsl(240, 100%, 50%)",
      "size": "large"
    },
    "sections": [
      {
        "id": "solar_position",
        "title": "Position Solaire",
        "fields": [
          { "key": "current_elevation", "label": "Élévation", "type": "number", "unit": "°" },
          { "key": "current_azimuth", "label": "Azimut", "type": "number", "unit": "°" }
        ]
      },
      {
        "id": "daily_events",
        "title": "Événements Quotidiens",
        "fields": [
          { "key": "sunrise", "label": "Lever du soleil", "type": "text" },
          { "key": "sunset", "label": "Coucher du soleil", "type": "text" }
        ]
      }
    ],
    "dataMapping": {
      "current_elevation": { "tool_name": "get_astronomical_data", "path": "current_elevation", "fallback": 0 },
      "sunrise": { "tool_name": "get_astronomical_data", "path": "sunrise", "fallback": "N/A" }
    },
    "interactions": [
      { "type": "refresh", "label": "Actualiser", "icon": "🔄" },
      { "type": "command", "label": "Recalculer", "action": "call_tool", "tool_name": "refresh_all_data" }
    ]
  }
}
```

---

## 🎨 Éléments du Widget

Le widget affiche une gamme complète de données astronomiques via les outils MCP :

#### ☀️ Données Solaires en Temps Réel
- **Position actuelle** : Élévation et azimut du soleil
- **Événements quotidiens** : Lever du soleil, coucher du soleil, midi solaire
- **Périodes spéciales** : Aube/crépuscule, heures dorées/bleues

#### 🌙 Données Lunaires
- **Phase lunaire** : Valeur numérique et représentation visuelle
- **Position lunaire** : Élévation et azimut actuels
- **Lever/coucher de lune** : Heures de lever et coucher de la lune

#### 📈 Visualisations Avancées (Dépendant du Gestionnaire)
- **Trajectoire solaire** : Graphique du parcours du soleil tout au long de la journée
- **Boussole solaire** : Représentation visuelle de la position actuelle du soleil sur une boussole.
- **Timeline** : Une chronologie des événements astronomiques de la journée.

---

## 🔧 Intégration Gestionnaire (NeurHomIA)

NeurHomIA peut exploiter ce mécanisme de découverte pour :

1.  **Découvrir le service** : Via le topic `mcp/astral2mqtt/discovery`
2.  **Récupérer les ressources** : Via l'outil `mcp.get_resource`
3.  **Créer l'interface utilisateur** : Basée sur le schéma de widget
4.  **Récupérer les données** : Via l'outil `get_astronomical_data` ou les événements
5.  **Afficher les données** : Dans le tableau de bord

### 🎯 Exemple de Code Gestionnaire (Pseudo-code)

```javascript
// Exemple de code gestionnaire NeurHomIA (pseudo-code)
async function loadAstralWidget(locationName) {
  // Récupérer le schéma de widget
  const widgetSchemaResponse = await mcpClient.callTool(
    "astral2mqtt",
    "mcp.get_resource",
    { resource_id: "astral2mqtt_astronomy_widget" }
  );
  const widgetSchema = widgetSchemaResponse.config;

  // Créer le widget UI
  const widget = createUIWidget(widgetSchema);

  // Charger les données initiales
  const initialData = await mcpClient.callTool(
    "astral2mqtt",
    "get_astronomical_data",
    { location_name: locationName }
  );
  widget.updateData(initialData);

  // S'abonner aux événements
  mcpClient.subscribeEvent("astral2mqtt", "astronomical_data", (event) => {
    if (event.data.location_name === locationName) {
      widget.updateData(event.data);
    }
  });

  dashboard.addWidget(widget);
}
```

---

## 🛠️ Activation de la Découverte de Widgets

La découverte de widgets est **activée par défaut** avec la découverte générale.

**Via variable d'environnement (priorité maximale) :**
```bash
export DISCOVERY_ENABLED=true
```

**Via fichier YAML (`config/mqtt_config.yaml`) :**
```yaml
discovery:
  enabled: true
```

---

## 🔄 Publication Automatique
