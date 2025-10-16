# Dockerfile pour microservices MCP
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="votre-email@example.com"
LABEL description="Microservice MCP JSON-RPC over MQTT"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Création de l'utilisateur non-root
RUN groupadd -r mcp && useradd -r -g mcp mcp

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Changement de propriétaire
RUN chown -R mcp:mcp /app

# Changement d'utilisateur
USER mcp

# Port exposé (si nécessaire pour monitoring/health check)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Point d'entrée
ENTRYPOINT ["python"]
CMD ["main.py"]

# Multi-stage build pour une image plus légère (optionnel)
# FROM python:3.11-slim as builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --user --no-cache-dir -r requirements.txt

# FROM python:3.11-slim
# WORKDIR /app
# COPY --from=builder /root/.local /root/.local
# COPY . .
# ENV PATH=/root/.local/bin:$PATH
# CMD ["python", "main.py"]