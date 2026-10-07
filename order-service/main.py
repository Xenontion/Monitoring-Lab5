import os
import logging
import random
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger

os.makedirs("/app/logs", exist_ok=True)

class EventIdFilter(logging.Filter):
    def filter(self, record):
        record.event_id = str(uuid.uuid4())
        return True


logger = logging.getLogger("order-service")
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler("/app/logs/order-service.log")
log_handler.addFilter(EventIdFilter())
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(event_id)s %(message)s",
    rename_fields={"levelname": "log_level", "asctime": "@timestamp", "name": "service"}
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

app = FastAPI()

class OrderRequest(BaseModel):
    order_id: str
    user_id: str
    amount: float

@app.post("/orders")
def create_order(req: OrderRequest):
    event_chance = random.random()

    # Генерація події ERROR із записом стек-трейсу винятку
    if event_chance < 0.2:
        try:
            raise ConnectionResetError("Remote payment gateway timeout after 5000ms")
        except Exception:
            logger.error(
                "Payment gateway call terminated with exception",
                exc_info=True,
                extra={"order_id": req.order_id, "amount": req.amount, "user_id": req.user_id}
            )
        raise HTTPException(status_code=502, detail="Payment gateway failure")

    # Генерація події WARN
    elif event_chance < 0.4:
        logger.warning(
            "Stock quantity is low for requested item",
            extra={"order_id": req.order_id, "available_items": 1}
        )

    # Генерація події INFO
    logger.info(
        "Order created and registered",
        extra={"order_id": req.order_id, "user_id": req.user_id, "amount": req.amount, "status": "CONFIRMED"}
    )
    return {"status": "CONFIRMED", "order_id": req.order_id}