#!/usr/bin/env python3
"""
Client de test pour microservices MCP
"""

import json
import time
import uuid
import argparse
import paho.mqtt.client as mqtt
from typing import Dict, Any

class MCPTestClient:
    def __init__(self, mqtt_host: str = "localhost", mqtt_port: int = 1883):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.responses = {}
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connecté au broker MQTT: {rc}")
    
    def on_message(self, client, userdata, msg):
        try:
            response = json.loads(msg.payload.decode())
            if "id" in response:
                self.responses[response["id"]] = response
        except Exception as e:
            print(f"Erreur parsing message: {e}")
    
    def connect(self):
        self.client.connect(self.mqtt_host, self.mqtt_port, 60)
        self.client.loop_start()
    
    def call_tool(self, service_id: str, method: str, params: Dict = None) -> Dict[str, Any]:
        request_id = str(uuid.uuid4())
        
        # S'abonner à la réponse
        response_topic = f"mcp/services/{service_id}/jsonrpc/response"
        self.client.subscribe(response_topic)
        
        # Construire la requête
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": request_id
        }
        
        # Envoyer la requête
        request_topic = f"mcp/services/{service_id}/jsonrpc/request"
        self.client.publish(request_topic, json.dumps(request))
        
        # Attendre la réponse
        timeout = 10
        start_time = time.time()
        while request_id not in self.responses:
            if time.time() - start_time > timeout:
                return {"error": "Timeout"}
            time.sleep(0.1)
        
        return self.responses[request_id]
    
    def test_health_check(self, service_id: str):
        print(f"Test health check pour {service_id}")
        response = self.call_tool(service_id, "mcp.health_check")
        print(f"Réponse: {json.dumps(response, indent=2)}")
        return response

def main():
    parser = argparse.ArgumentParser(description="Client de test MCP")
    parser.add_argument("--service-id", required=True, help="ID du microservice")
    parser.add_argument("--method", default="mcp.health_check", help="Méthode à appeler")
    parser.add_argument("--params", help="Paramètres JSON")
    parser.add_argument("--mqtt-host", default="localhost", help="Host MQTT")
    
    args = parser.parse_args()
    
    client = MCPTestClient(args.mqtt_host)
    client.connect()
    
    params = json.loads(args.params) if args.params else None
    response = client.call_tool(args.service_id, args.method, params)
    
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()