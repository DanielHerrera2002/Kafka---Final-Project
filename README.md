# 🚀 Kafka Final Project: Real-time User Behavior Analysis

**Estudiantes:** Daniel Herrera, Alan Mendoza, Emmanuel Carmona  
**Curso:** Kafka - Unit III  
**Fecha:** Diciembre 2025

---

## 📋 Descripción del Proyecto

Este proyecto implementa una arquitectura de **streaming de datos distribuida** utilizando Apache Kafka. El sistema simula el ecosistema de un E-commerce en tiempo real, generando eventos de interacción de usuarios (vistas, carritos, compras), procesándolos para obtener métricas analíticas y visualizando el flujo de datos.

El objetivo principal es demostrar la capacidad de **ingesta, procesamiento y visualización** de volúmenes de datos concurrentes, cumpliendo con los estándares de modelado de información y escalabilidad.

---

## 🏗️ Arquitectura del Pipeline

El flujo de información sigue el patrón **Producer-Broker-Consumer**:

* **Data Source (JSON):** Catálogos estáticos de `products.json` y `users.json` simulan la base de datos maestra.
* **Producers (Python + Threading):** Scripts que generan eventos sintéticos. Soportan concurrencia mediante hilos para simular múltiples usuarios activos simultáneamente.
* **Message Broker (Kafka):** Cluster gestionado vía Docker, encargado de recibir y distribuir los mensajes en el topic `product-events`.
* **Consumers (Analytics):** Procesamiento en tiempo real que calcula KPIs (Key Performance Indicators) como "Top Productos" y segmentación de usuarios.
* **Visualización (Kafka UI):** Interfaz gráfica para monitoreo de offsets, particiones y flujo de mensajes.

---

## 📂 Estructura del Proyecto

La organización del código sigue principios de modularidad y buenas prácticas:

```text
KafkaFinalProject/
├── data/                   # Fuentes de datos estáticas
│   ├── products.json       # Catálogo de productos (ID, Categoría, Precio)
│   └── users.json          # Usuarios con segmentación (Región, Tipo)
├── src/
│   ├── producers/          # Lógica de generación de eventos
│   │   └── main_producer.py
│   ├── consumers/          # Lógica de procesamiento y analítica
│   │   └── analytics_consumer.py
│   └── utils/              # Configuraciones compartidas
├── docker-compose.yml      # Orquestación de Zookeeper, Kafka y Kafka UI
├── .env                    # Variables de entorno (Configuración)
├── requirements.txt        # Dependencias de Python
└── README.md               # Documentación
```
---
## ⚙️ Requisitos Previos
Docker Desktop (con Docker Compose instalado).

Python 3.8 o superior (Probado en Python 3.12+).

Git (Opcional, para control de versiones).

## 🚀 Guía de Instalación y Ejecución
Sigue estos pasos para levantar el entorno completo en tu máquina local.

1. Configuración del Entorno Virtual
Es necesario aislar las dependencias para evitar conflictos, especialmente con versiones modernas de Python.

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt
2. Configuración de Variables (.env)
El proyecto utiliza variables de entorno para facilitar la configuración. El archivo .env incluye:

Properties

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_PRODUCTS=product-events
KAFKA_TOPIC_USERS=user-events
KAFKA_TOPIC_PURCHASES=purchases
3. Despliegue de Infraestructura (Docker)
Levanta los contenedores de Zookeeper, Kafka Broker y Kafka UI.

docker-compose up -d
Nota: Espere unos 30 segundos hasta que los servicios estén completamente iniciados.

## ▶️ Ejecución de la Simulación
Para ver el sistema en acción, se recomienda usar dos terminales separadas.

Terminal 1: Consumer (Analítica)
Inicie primero el consumidor para que esté listo para procesar los mensajes entrantes.


# Asegúrese de tener el venv activado
python -m src.consumers.analytics_consumer
Se mostrará un dashboard en consola esperando eventos.

Terminal 2: Producer (Generador de Tráfico)
Inicie el simulador de tráfico. Este script lanzará 3 hilos concurrentes simulando usuarios distintos enviando datos al mismo tiempo.

# En una nueva terminal con venv activado
python -m src.producers.main_producer

## 📊 Monitoreo y Verificación
Dashboard en Consola
En la Terminal 1, verá actualizaciones en tiempo real con las siguientes métricas:

Total de eventos procesados.

Conteo por tipo de evento (view, add_to_cart, remove_from_cart).

Actividad por segmento de usuario (Premium, Standard).

Producto más visto/interactuado.

Kafka UI (Visualización Web)
Acceda a la interfaz gráfica para verificar la creación de topics y la persistencia de mensajes:

## 🔗 URL: http://localhost:8080

Navegue a la sección Topics.

Seleccione product-events.

Vaya a la pestaña Messages para ver el payload JSON crudo ingresando en tiempo real.

## 🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.13

Streaming: Apache Kafka (Confluent Image 7.4.0)

Orquestación: Docker Compose

Librerías Clave:

kafka-python-ng: Cliente Kafka compatible con versiones recientes de Python.

python-dotenv: Gestión de configuración.

## 📝 Notas Técnicas
Compatibilidad Python: Se utiliza kafka-python-ng en lugar de la librería estándar antigua para garantizar compatibilidad con Python 3.12+.

Serialización: Todos los mensajes se serializan en JSON UTF-8.

Concurrencia: El Producer implementa threading para simular carga real, cumpliendo con el requerimiento de la rúbrica sobre múltiples productores simultáneos.

Proyecto desarrollado para la evaluación final de la Unidad III.
