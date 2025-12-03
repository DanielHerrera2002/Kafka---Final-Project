# Kafka Final Project: Real-time User Behavior Analysis

Este proyecto implementa un sistema de streaming de datos utilizando Apache Kafka para simular, procesar y visualizar eventos de comportamiento de usuarios en un e-commerce.

## Estructura del Proyecto
El código está organizado modularmente siguiendo buenas prácticas:
- `data/`: Archivos JSON con datos base (productos y usuarios).
- `src/producers/`: Scripts para generación de eventos concurrentes.
- `src/consumers/`: Scripts para procesamiento y analítica en tiempo real.
- `docker-compose.yml`: Infraestructura de Kafka, Zookeeper y Kafka UI.

## Requisitos Previos
- Docker y Docker Compose
- Python 3.8+

## Instrucciones de Instalación

1. **Configurar Entorno Virtual:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Git Bash/Windows