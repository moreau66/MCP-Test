#!/usr/bin/env python3
"""
Exemple de microservice calculatrice simple
Démontre les fonctionnalités de base d'un microservice MCP
"""

import logging
import math
from typing import Dict, Any
from mcp_mqtt_sdk import MCPMicroservice, mcp_tool, mcp_resource

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalculatorService(MCPMicroservice):
    """
    Microservice calculatrice avec opérations mathématiques de base.
    
    Ce service démontre l'implémentation d'outils MCP simples
    pour des opérations mathématiques courantes.
    """
    
    def __init__(self):
        super().__init__(
            service_id="calculator-service",
            mqtt_host="localhost",
            mqtt_port=1883,
            api_key="calculator-api-key"
        )
        
        self.calculation_history = []
        logger.info("Service calculatrice initialisé")
    
    def get_service_metadata(self) -> Dict[str, Any]:
        """Métadonnées du service calculatrice."""
        return {
            "service_id": "calculator-service",
            "name": "Service Calculatrice",
            "description": "Microservice pour opérations mathématiques de base",
            "version": "1.0.0",
            "protocol_version": "1.0",
            "author": "Équipe MCP",
            "category": "utility",
            "tags": ["math", "calculator", "utility"]
        }
    
    @mcp_tool(
        name="math.add",
        description="Additionne deux nombres",
        category="utility",
        permissions=["math:basic"]
    )
    def add(self, a: float, b: float) -> Dict[str, Any]:
        """
        Additionne deux nombres.
        
        Args:
            a: Premier nombre
            b: Deuxième nombre
            
        Returns:
            Résultat de l'addition avec métadonnées
        """
        result = a + b
        calculation = {
            "operation": "addition",
            "operands": [a, b],
            "result": result,
            "formula": f"{a} + {b} = {result}"
        }
        
        self.calculation_history.append(calculation)
        logger.info(f"Addition: {a} + {b} = {result}")
        
        return calculation
    
    @mcp_tool(
        name="math.subtract",
        description="Soustrait deux nombres",
        category="utility",
        permissions=["math:basic"]
    )
    def subtract(self, a: float, b: float) -> Dict[str, Any]:
        """Soustrait b de a."""
        result = a - b
        calculation = {
            "operation": "subtraction",
            "operands": [a, b],
            "result": result,
            "formula": f"{a} - {b} = {result}"
        }
        
        self.calculation_history.append(calculation)
        logger.info(f"Soustraction: {a} - {b} = {result}")
        
        return calculation
    
    @mcp_tool(
        name="math.multiply",
        description="Multiplie deux nombres",
        category="utility",
        permissions=["math:basic"]
    )
    def multiply(self, a: float, b: float) -> Dict[str, Any]:
        """Multiplie deux nombres."""
        result = a * b
        calculation = {
            "operation": "multiplication",
            "operands": [a, b],
            "result": result,
            "formula": f"{a} × {b} = {result}"
        }
        
        self.calculation_history.append(calculation)
        logger.info(f"Multiplication: {a} × {b} = {result}")
        
        return calculation
    
    @mcp_tool(
        name="math.divide",
        description="Divise deux nombres",
        category="utility",
        permissions=["math:basic"]
    )
    def divide(self, a: float, b: float) -> Dict[str, Any]:
        """
        Divise a par b.
        
        Args:
            a: Dividende
            b: Diviseur
            
        Returns:
            Résultat de la division
            
        Raises:
            ValueError: Si b est zéro
        """
        if b == 0:
            raise ValueError("Division par zéro impossible")
        
        result = a / b
        calculation = {
            "operation": "division",
            "operands": [a, b],
            "result": result,
            "formula": f"{a} ÷ {b} = {result}"
        }
        
        self.calculation_history.append(calculation)
        logger.info(f"Division: {a} ÷ {b} = {result}")
        
        return calculation
    
    @mcp_tool(
        name="math.power",
        description="Élève un nombre à une puissance",
        category="utility",
        permissions=["math:advanced"]
    )
    def power(self, base: float, exponent: float) -> Dict[str, Any]:
        """Calcule base^exponent."""
        result = math.pow(base, exponent)
        calculation = {
            "operation": "power",
            "operands": [base, exponent],
            "result": result,
            "formula": f"{base}^{exponent} = {result}"
        }
        
        self.calculation_history.append(calculation)
        logger.info(f"Puissance: {base}^{exponent} = {result}")
        
        return calculation
    
    @mcp_tool(
        name="math.sqrt",
        description="Calcule la racine carrée d'un nombre",
        category="utility",
        permissions=["math:advanced"]
    )
    def sqrt(self, number: float) -> Dict[str, Any]:
        """
        Calcule la racine carrée.
        
        Args:
            number: Nombre positif
            
        Returns:
            Racine carrée du nombre
            
        Raises:
            ValueError: Si le nombre est négatif
        """
        if number < 0:
            raise ValueError("Impossible de calculer la racine carrée d'un nombre négatif")
        
        result = math.sqrt(number)
        calculation = {
            "operation": "square_root",
            "operands": [number],
            "result": result,
            "formula": f"√{number} = {result}"
        }
        
        self.calculation_history.append(calculation)
        logger.info(f"Racine carrée: √{number} = {result}")
        
        return calculation
    
    @mcp_tool(
        name="calculator.clear_history",
        description="Efface l'historique des calculs",
        category="utility",
        permissions=["calculator:admin"]
    )
    def clear_history(self) -> Dict[str, Any]:
        """Efface l'historique des calculs."""
        count = len(self.calculation_history)
        self.calculation_history.clear()
        
        logger.info(f"Historique effacé: {count} calculs supprimés")
        
        return {
            "status": "success",
            "message": f"Historique effacé ({count} calculs supprimés)",
            "cleared_count": count
        }
    
    @mcp_resource(
        uri="calculator/history",
        name="Historique des calculs",
        description="Liste de tous les calculs effectués",
        mimeType="application/json",
        resourceType="data"
    )
    def get_calculation_history(self) -> Dict[str, Any]:
        """Retourne l'historique complet des calculs."""
        return {
            "total_calculations": len(self.calculation_history),
            "history": self.calculation_history,
            "statistics": self._get_calculation_statistics()
        }
    
    @mcp_resource(
        uri="calculator/widget",
        name="Widget Calculatrice",
        description="Interface de calculatrice pour NeurHomIA",
        mimeType="application/json",
        resourceType="widget"
    )
    def get_calculator_widget(self) -> Dict[str, Any]:
        """Retourne la configuration du widget calculatrice."""
        return {
            "id": "calculator-widget",
            "name": "Calculatrice",
            "version": "1.0.0",
            "display": {
                "title": "Calculatrice",
                "icon": "calculator",
                "color": "hsl(210, 100%, 50%)",
                "size": {"width": 300, "height": 400}
            },
            "sections": [
                {
                    "id": "display",
                    "title": "Affichage",
                    "type": "display",
                    "fields": [
                        {
                            "id": "result",
                            "label": "Résultat",
                            "type": "number",
                            "readonly": True
                        }
                    ]
                },
                {
                    "id": "operations",
                    "title": "Opérations",
                    "type": "controls",
                    "fields": [
                        {
                            "id": "operand_a",
                            "label": "Nombre A",
                            "type": "number"
                        },
                        {
                            "id": "operand_b",
                            "label": "Nombre B",
                            "type": "number"
                        }
                    ]
                }
            ],
            "interactions": [
                {
                    "type": "button",
                    "label": "Addition",
                    "action": "math.add",
                    "params": ["operand_a", "operand_b"]
                },
                {
                    "type": "button",
                    "label": "Soustraction",
                    "action": "math.subtract",
                    "params": ["operand_a", "operand_b"]
                },
                {
                    "type": "button",
                    "label": "Multiplication",
                    "action": "math.multiply",
                    "params": ["operand_a", "operand_b"]
                },
                {
                    "type": "button",
                    "label": "Division",
                    "action": "math.divide",
                    "params": ["operand_a", "operand_b"]
                }
            ]
        }
    
    def _get_calculation_statistics(self) -> Dict[str, Any]:
        """Calcule des statistiques sur l'historique."""
        if not self.calculation_history:
            return {"total": 0}
        
        operations = {}
        for calc in self.calculation_history:
            op = calc["operation"]
            operations[op] = operations.get(op, 0) + 1
        
        return {
            "total": len(self.calculation_history),
            "operations_count": operations,
            "most_used_operation": max(operations.items(), key=lambda x: x[1])[0] if operations else None
        }

if __name__ == "__main__":
    service = CalculatorService()
    
    try:
        logger.info("Démarrage du service calculatrice")
        service.run()
    except KeyboardInterrupt:
        logger.info("Arrêt du service calculatrice")
    except Exception as e:
        logger.error(f"Erreur: {e}")