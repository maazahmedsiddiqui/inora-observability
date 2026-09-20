from flask import Flask
import random
import time

app = Flask(__name__)

@app.route('/catalog')
def catalog():
    time.sleep(random.uniform(0.1, 0.3))
    return {"items": ["clover pendant", "minimalist ring", "pearl bracelet"]}

@app.route('/order', methods=['POST'])
def order():
    if random.random() < 0.2:
        return {"error": "payment_failed"}, 500
    time.sleep(random.uniform(0.2, 0.6))
    return {"status": "success", "order_id": random.randint(1000, 9999)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)