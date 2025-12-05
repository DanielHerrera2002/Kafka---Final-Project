import json
import os
import time
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

# Configuración
TOPIC_PRODUCTS = os.getenv('KAFKA_TOPIC_PRODUCTS', 'product-events')
BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def analytics_consumer():
    # Configuración del consumidor con group_id para monitoreo
    consumer = KafkaConsumer(
        TOPIC_PRODUCTS,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='analytics_dashboard'  # <--- ESTO ES LO QUE FALTABA
    )

    # Métricas en memoria
    metrics = {
        "total_events": 0,
        "by_type": {"view": 0, "add_to_cart": 0, "remove_from_cart": 0},
        "by_segment": {"Premium": 0, "Standard": 0, "New": 0},
        "top_products": {}
    }

    print("Iniciando Consumer de Analíticas... Esperando eventos...")
    print("-" * 50)

    try:
        for message in consumer:
            event = message.value
            
            # Actualizar métricas
            metrics["total_events"] += 1
            
            # Conteo por tipo
            e_type = event.get('event_type')
            if e_type in metrics["by_type"]:
                metrics["by_type"][e_type] += 1
            
            # Segmentación de usuarios
            segment = event.get('user_segment', 'Unknown')
            if segment in metrics["by_segment"]:
                metrics["by_segment"][segment] = metrics["by_segment"].get(segment, 0) + 1
            else:
                 metrics["by_segment"][segment] = 1

            # Top productos (simple)
            p_name = f"{event['product_id']}"
            metrics["top_products"][p_name] = metrics["top_products"].get(p_name, 0) + 1

            # Visualización Clara (dashboard simple en consola)
            # Solo imprimimos cada 5 eventos para no saturar la consola
            if metrics["total_events"] % 5 == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"=== KAFKA REAL-TIME ANALYTICS DASHBOARD ===")
                print(f"Total Eventos Procesados: {metrics['total_events']}")
                print("\n--- Eventos por Tipo ---")
                for k, v in metrics["by_type"].items():
                    print(f"{k}: {v}")
                
                print("\n--- Actividad por Segmento de Usuario ---")
                for k, v in metrics["by_segment"].items():
                    print(f"{k}: {v}")
                
                print("\n--- Último Evento Recibido ---")
                print(f"Usuario {event['user_id']} ({event['user_segment']}) -> {event['event_type']} -> {event['product_id']}")
                print("===========================================")

    except KeyboardInterrupt:
        print("Consumer detenido.")
    finally:
        consumer.close()

if __name__ == "__main__":
    analytics_consumer()