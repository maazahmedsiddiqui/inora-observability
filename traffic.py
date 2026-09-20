import requests
import time
import random

while True:
    requests.get('http://127.0.0.1:5000/catalog')
    
    if random.random() < 0.3:
        requests.post('http://127.0.0.1:5000/order')
        
    time.sleep(random.uniform(0.5, 2.0))