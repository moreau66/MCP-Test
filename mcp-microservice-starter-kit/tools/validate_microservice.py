#!/usr/bin/env python3
"""
Validateur de microservice MCP
Vérifie la conformité d'un microservice avec les standards MCP
"""

import json
import sys
import argparse
import jsonschema
from pathlib import Path
from typing import Dict, List, Any
import importlib.util

class MCPValidator:
    """Validateur pour microservices MCP."""
    
    def __init__(self, schemas_path: str = "schemas"):
        """
        Initialise le validateur.
        
        Args:
            schemas_path: Chemin vers les schémas JSON
        """
        self.schemas_path = Path(schemas_path)
        self.schemas = self._load_schemas()
        self.errors = []
        self.warnings = []
    
    def _load_schemas(self) -> Dict[str, Any]:
        """Charge tous les schémas JSON."""
        schemas = {}
        schema_files = [
            "mcp-schema.json",
            "jsonrpc-schema.json",
            "mcp-tool-schema.json",
            "mcp-resource-schema.json"
        ]
        
        for schema_file in schema_files:
            schema_path = self.schemas_path / schema_file
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schemas[schema_file] = json.load(f)
        
        return schemas
    
    def validate_microservice_file(self, microservice_path: str) -> bool:
        """
        Valide un fichier de microservice Python.
        
        Args:
            microservice_path: Chemin vers le fichier Python
            
        Returns:
            True si valide, False sinon
        """
        print(f"🔍 Validation du microservice: {microservice_path}")
        
        # Vérification de l'existence du fichier
        if not Path(microservice_path).exists():
            self.errors.append(f"Fichier non trouvé: {microservice_path}")
            return False
        
        try:
            # Import dynamique du microservice
            spec = importlib.util.spec_from_file_location("microservice", microservice_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Recherche de la classe de microservice
            microservice_class = self._find_microservice_class(module)
            if not microservice_class:
                self.errors.append("Aucune classe héritant de MCPMicroservice trouvée")
                return False
            
            # Validation de la classe
            return self._validate_microservice_class(microservice_class)
            
        except Exception as e:
            self.errors.append(f"Erreur lors de l'import: {str(e)}")
            return False
    
    def _find_microservice_class(self, module) -> Any:
        """Trouve la classe de microservice dans le module."""
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and 
                hasattr(obj, '__bases__') and 
                any('MCPMicroservice' in str(base) for base in obj.__bases__)):
                return obj
        return None
    
    def _validate_microservice_class(self, microservice_class) -> bool:
        """Valide une classe de microservice."""
        is_valid = True
        
        # Validation des méthodes MCP obligatoires
        required_methods = ['health_check']
        for method in required_methods:
            if not hasattr(microservice_class, method):
                self.errors.append(f"Méthode obligatoire manquante: {method}")
                is_valid = False
        
        # Validation des outils MCP
        tools = self._extract_mcp_tools(microservice_class)
        if not tools:
            self.warnings.append("Aucun outil MCP défini (@mcp_tool)")
        else:
            for tool_name, tool_info in tools.items():
                if not self._validate_tool(tool_name, tool_info):
                    is_valid = False
        
        # Validation des ressources MCP
        resources = self._extract_mcp_resources(microservice_class)
        for resource_name, resource_info in resources.items():
            if not self._validate_resource(resource_name, resource_info):
                is_valid = False
        
        # Validation des métadonnées de service
        if hasattr(microservice_class, 'get_service_metadata'):
            metadata = microservice_class().get_service_metadata()
            if not self._validate_service_metadata(metadata):
                is_valid = False
        else:
            self.warnings.append("Méthode get_service_metadata() recommandée")
        
        return is_valid
    
    def _extract_mcp_tools(self, microservice_class) -> Dict[str, Any]:
        """Extrait les outils MCP de la classe."""
        tools = {}
        for name in dir(microservice_class):
            method = getattr(microservice_class, name)
            if hasattr(method, '_mcp_tool_config'):
                tools[name] = method._mcp_tool_config
        return tools
    
    def _extract_mcp_resources(self, microservice_class) -> Dict[str, Any]:
        """Extrait les ressources MCP de la classe."""
        resources = {}
        for name in dir(microservice_class):
            method = getattr(microservice_class, name)
            if hasattr(method, '_mcp_resource_config'):
                resources[name] = method._mcp_resource_config
        return resources
    
    def _validate_tool(self, tool_name: str, tool_info: Dict) -> bool:
        """Valide un outil MCP."""
        required_fields = ['name', 'description', 'category']
        for field in required_fields:
            if field not in tool_info:
                self.errors.append(f"Outil {tool_name}: champ obligatoire manquant '{field}'")
                return False
        
        # Validation du nom
        if '.' not in tool_info['name']:
            self.errors.append(f"Outil {tool_name}: le nom doit contenir un point (namespace.method)")
            return False
        
        # Validation de la catégorie
        valid_categories = ["utility", "data", "automation", "monitoring", "config", "ai", "iot"]
        if tool_info['category'] not in valid_categories:
            self.errors.append(f"Outil {tool_name}: catégorie invalide '{tool_info['category']}'")
            return False
        
        return True
    
    def _validate_resource(self, resource_name: str, resource_info: Dict) -> bool:
        """Valide une ressource MCP."""
        required_fields = ['uri', 'name', 'mimeType', 'resourceType']
        for field in required_fields:
            if field not in resource_info:
                self.errors.append(f"Ressource {resource_name}: champ obligatoire manquant '{field}'")
                return False
        
        # Validation du type MIME
        valid_mime_types = ["application/json", "text/plain", "text/html", "image/png", "image/jpeg"]
        if resource_info['mimeType'] not in valid_mime_types:
            self.errors.append(f"Ressource {resource_name}: type MIME invalide '{resource_info['mimeType']}'")
            return False
        
        return True
    
    def _validate_service_metadata(self, metadata: Dict) -> bool:
        """Valide les métadonnées du service."""
        required_fields = ['service_id', 'name', 'description', 'version']
        for field in required_fields:
            if field not in metadata:
                self.errors.append(f"Métadonnées: champ obligatoire manquant '{field}'")
                return False
        
        # Validation du service_id
        service_id = metadata['service_id']
        if not service_id.replace('-', '').replace('_', '').isalnum():
            self.errors.append(f"service_id invalide: '{service_id}' (lettres, chiffres, tirets et underscores uniquement)")
            return False
        
        return True
    
    def validate_json_config(self, config_path: str) -> bool:
        """
        Valide un fichier de configuration JSON.
        
        Args:
            config_path: Chemin vers le fichier JSON
            
        Returns:
            True si valide, False sinon
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validation avec le schéma approprié
            if 'mcp-schema.json' in self.schemas:
                jsonschema.validate(config, self.schemas['mcp-schema.json'])
                print(f"✅ Configuration JSON valide: {config_path}")
                return True
            else:
                self.warnings.append("Schéma MCP non trouvé pour la validation JSON")
                return True
                
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON invalide dans {config_path}: {str(e)}")
            return False
        except jsonschema.ValidationError as e:
            self.errors.append(f"Validation échouée pour {config_path}: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Erreur lors de la validation de {config_path}: {str(e)}")
            return False
    
    def print_results(self):
        """Affiche les résultats de validation."""
        print("\n" + "="*50)
        print("RÉSULTATS DE VALIDATION")
        print("="*50)
        
        if self.errors:
            print(f"\n❌ ERREURS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️ AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ VALIDATION RÉUSSIE - Aucun problème détecté")
        elif not self.errors:
            print(f"\n✅ VALIDATION RÉUSSIE - {len(self.warnings)} avertissement(s)")
        else:
            print(f"\n❌ VALIDATION ÉCHOUÉE - {len(self.errors)} erreur(s)")
        
        print("="*50)

def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Validateur de microservice MCP")
    parser.add_argument("path", help="Chemin vers le microservice Python ou config JSON")
    parser.add_argument("--schemas", default="schemas", help="Chemin vers les schémas")
    parser.add_argument("--type", choices=["python", "json", "auto"], default="auto",
                       help="Type de fichier à valider")
    
    args = parser.parse_args()
    
    validator = MCPValidator(args.schemas)
    
    # Détection automatique du type
    if args.type == "auto":
        if args.path.endswith('.py'):
            file_type = "python"
        elif args.path.endswith('.json'):
            file_type = "json"
        else:
            print("❌ Type de fichier non reconnu. Utilisez --type pour spécifier.")
            sys.exit(1)
    else:
        file_type = args.type
    
    # Validation selon le type
    if file_type == "python":
        is_valid = validator.validate_microservice_file(args.path)
    elif file_type == "json":
        is_valid = validator.validate_json_config(args.path)
    
    # Affichage des résultats
    validator.print_results()
    
    # Code de sortie
    sys.exit(0 if is_valid and not validator.errors else 1)

if __name__ == "__main__":
    main()