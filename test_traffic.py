import time
import random
import uuid
import requests

AUTH_URL = "http://localhost:8001/login"
ORDER_URL = "http://localhost:8002/orders"

users = ["admin", "alex", "john_doe", "support", "guest"]

print(">>> Початок надсилання запитів для створення логів...")

for i in range(1, 61):
    user = random.choice(users)
    
    # 1. Запит до Auth-Service
    auth_body = {
        "username": user,
        "password": "secret" if random.random() > 0.35 else "wrong_pass"
    }
    try:
        requests.post(AUTH_URL, json=auth_body, timeout=2)
    except Exception:
        pass

    # 2. Запит до Order-Service
    order_body = {
        "order_id": f"ord-{uuid.uuid4().hex[:6]}",
        "user_id": user,
        "amount": round(random.uniform(25.0, 1500.0), 2)
    }
    try:
        requests.post(ORDER_URL, json=order_body, timeout=2)
    except Exception:
        pass

    print(f"[{i}/60] Згенеровано події для сервісів auth та order...")
    time.sleep(0.1)

print("\n>>> Генерацію завершено! Відкрийте Kibana: http://localhost:5601")