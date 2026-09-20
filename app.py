from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest
import random
import time
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint', 'http_status'])
ACTIVE_REQUESTS = Gauge('app_active_requests', 'Active requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')
ORDER_PROCESSING = Summary('app_order_processing_seconds', 'Time spent processing orders')
BUSINESS_ORDERS = Counter('business_orders_total', 'Total orders placed', ['status'])

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4'}

@app.route('/catalog')
@ACTIVE_REQUESTS.track_inprogress()
@REQUEST_LATENCY.time()
def catalog():
    time.sleep(random.uniform(0.1, 0.3))
    REQUEST_COUNT.labels('GET', '/catalog', '200').inc()
    logging.info("Catalog endpoint accessed by user")
    return {"items": ["clover pendant", "minimalist ring", "pearl bracelet"]}

@app.route('/order', methods=['POST'])
@ACTIVE_REQUESTS.track_inprogress()
def order():
    start_time = time.time()
    if random.random() < 0.2:
        REQUEST_COUNT.labels('POST', '/order', '500').inc()
        BUSINESS_ORDERS.labels('failed').inc()
        logging.error("Payment transaction failed for order attempt")
        return {"error": "payment_failed"}, 500
    
    time.sleep(random.uniform(0.2, 0.6))
    REQUEST_COUNT.labels('POST', '/order', '200').inc()
    BUSINESS_ORDERS.labels('success').inc()
    ORDER_PROCESSING.observe(time.time() - start_time)
    
    order_id = random.randint(1000, 9999)
    logging.info(f"Order {order_id} processed successfully")
    return {"status": "success", "order_id": order_id}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)