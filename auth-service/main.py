import os
import logging
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger

os.makedirs("/app/logs", exist_ok=True)

logger = logging.getLogger("auth-service")
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler("/app/logs/auth-service.log")
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={"levelname": "log_level", "asctime": "@timestamp", "name": "service"}
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    event_chance = random.random()
    
    # Генерація події ERROR
    if event_chance < 0.2:
        logger.error(
            "Database connection failed during authentication",
            extra={"client_ip": "192.168.1.15", "user": req.username, "error_code": "DB_CONN_TIMEOUT"}
        )
        raise HTTPException(status_code=500, detail="Internal Auth DB Error")
    
    # Генерація події WARN
    elif event_chance < 0.5 or req.password != "secret":
        logger.warning(
            "Failed login attempt: invalid credentials",
            extra={"client_ip": "192.168.1.20", "user": req.username, "attempt": 3}
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Генерація події INFO
    logger.info(
        "User authenticated successfully",
        extra={"client_ip": "192.168.1.10", "user": req.username, "token_issued": True}
    )
    return {"status": "SUCCESS", "token": "jwt-mock-token"}