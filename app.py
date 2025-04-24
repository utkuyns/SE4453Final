import os
import psycopg2
from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Flask uygulamasını başlat
app = Flask(__name__)

# Key Vault bilgileri
KEY_VAULT_NAME = "yazilimmidtermkv"
KVUri = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

# Azure Managed Identity ile giriş
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Secret'ları çek
PGHOST = client.get_secret("PGHOST").value
PGUSER = client.get_secret("PGUSER").value
PGPASSWORD = client.get_secret("PGPASSWORD").value
PGDATABASE = client.get_secret("PGDATABASE").value
PGPORT = client.get_secret("PGPORT").value

# PostgreSQL bağlantı fonksiyonu
def connect_db():
    conn = psycopg2.connect(
        host=PGHOST,
        dbname=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        port=PGPORT
    )
    return conn

@app.route("/")
def index():
    return "Welcome to Azure App!"

@app.route("/hello")
def hello():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return f"DB Connected! Query Result: {result[0]}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

if __name__ == '__main__':
    app.run()
