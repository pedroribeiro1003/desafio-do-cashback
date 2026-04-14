from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("cashback.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    tipo_cliente TEXT,
    valor REAL,
    desconto REAL,
    cashback REAL,
    criado_em TEXT
)
''')
conn.commit()

class Consulta(BaseModel):
    valor: float
    desconto: float
    vip: bool

def calcular_cashback(valor_produto, desconto_percentual, vip=False):
    valor_final = valor_produto * (1 - desconto_percentual / 100)
    cashback_base = valor_final * 0.05
    if valor_final > 500:
        cashback_base *= 2
    bonus_vip = cashback_base * 0.10 if vip else 0
    return round(cashback_base + bonus_vip, 2)

@app.post("/calcular")
def calcular(data: Consulta, request: Request):
    ip = request.client.host
    cashback = calcular_cashback(data.valor, data.desconto, data.vip)
    tipo = "VIP" if data.vip else "Normal"
    cursor.execute(
        "INSERT INTO consultas (ip, tipo_cliente, valor, desconto, cashback, criado_em) VALUES (?, ?, ?, ?, ?, ?)",
        (ip, tipo, data.valor, data.desconto, cashback, datetime.now().isoformat())
    )
    conn.commit()
    return {"cashback": cashback}

@app.get("/historico")
def historico(request: Request):
    ip = request.client.host
    cursor.execute("SELECT tipo_cliente, valor, desconto, cashback, criado_em FROM consultas WHERE ip = ? ORDER BY id DESC", (ip,))
    return cursor.fetchall()
