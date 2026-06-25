from fastapi import FastAPI
import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

app = FastAPI(title="Marmit'IA API")

@app.get("/")
def accueil():
    return {"app": "Marmit'IA", "etat": "squelette DevOps"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/redis-check")
def redis_check():
    """Vérifie que l'api arrive à joindre Redis (démo du réseau Docker)."""
    try:
        cache.ping()
        return {"redis": "connecté", "host": REDIS_HOST}
    except redis.exceptions.RedisError as err:
        return {"redis": "injoignable", "host": REDIS_HOST, "erreur": str(err)}