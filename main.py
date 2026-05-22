from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

class Transaksi(BaseModel):
    tanggal: str
    keterangan: str
    jenis: str
    jumlah: float

@app.get("/")
def root():
    return {"message": "Kas RW Backend Running"}

@app.get("/transaksi")
def get_transaksi():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transaksi")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

@app.post("/transaksi")
def add_transaksi(t: Transaksi):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = """
    INSERT INTO transaksi
    (tanggal, keterangan, jenis, jumlah)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        t.tanggal,
        t.keterangan,
        t.jenis,
        t.jumlah
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Transaksi berhasil ditambahkan"}
