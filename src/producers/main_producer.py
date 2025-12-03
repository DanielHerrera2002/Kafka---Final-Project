import json
import time
import random
import os
import threading
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC_PRODUCTS = os.getenv('KAFKA_TOPIC_PRODUCTS', 'product-events')

def load_data(filename):
    """Carga datos desde archivos JSON."""
    filepath = os.path.join('data', filename)
    with open(filepath, 'r') as f:
        return json.load(f)

class ProductEventProducer:
    def __init__(self, producer_id):
        self.producer_id = producer_id
        self.producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.products = load_data('products.json')
        self.users = load_data('users.json')
        self.event_types = ['view', 'add_to_cart', 'remove_from_cart']

    def generate_event(self):
        """Genera un evento simulado."""
        user = random.choice(self.users)
        product = random.choice(self.products)
        event_type = random.choices(self.event_types, weights=[0.7, 0.2, 0.1], k=1)[0]
        
        event = {
            'event_id': str(random.randint(10000, 99999)),
            'timestamp': datetime.now().isoformat(),
            'user_id': user['user_id'],
            'user_segment': user['segment'], # Datos enriquecidos para analisis
            'user_region': user['region'],
            'product_id': product['product_id'],
            'category': product['category'],
            'event_type': event_type,
            'producer_source': self.producer_id
        }
        return event

    def run(self):
        print(f"Producer {self.producer_id} iniciado...")
        try:
            while True:
                event = self.generate_event()
                self.producer.send(TOPIC_PRODUCTS, event)
                print(f"[{self.producer_id}] Enviado: {event['event_type']} por {event['user_id']}")
                time.sleep(random.uniform(1, 3)) # Simular tiempo entre acciones
        except KeyboardInterrupt:
            self.producer.close()

def start_producer_thread(pid):
    p = ProductEventProducer(pid)
    p.run()

if __name__ == "__main__":
    # Cumplimiento: Script para ejecutar múltiples producers simultáneamente
    num_producers = 3
    threads = []
    
    print(f"Iniciando {num_producers} producers concurrentes...")
    
    for i in range(num_producers):
        t = threading.Thread(target=start_producer_thread, args=(f"P-{i+1}",))
        t.daemon = True
        t.start()
        threads.append(t)
        
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo producers...")