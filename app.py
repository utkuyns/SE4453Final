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
PGPASSWORD = client.get_secret("PASSWORD").value
PGDATABASE = client.get_secret("PGDATABASE").value
PGPORT = client.get_secret("PGPORT").value
PGUSER = client.get_secret("userNew").value


# PostgreSQL bağlantı fonksiyonu
def connect_db():
    conn = psycopg2.connect(
    host=PGHOST,
    dbname=PGDATABASE,
    user=PGUSER,
    password=PGPASSWORD,
    port=PGPORT,
    sslmode="require"
)

    return conn

@app.route("/")
def index():
    return "<h1>Welcome to Midterm Project App</h1><p>Visit <a href='/hello'>/hello</a> to view student records.</p>"   

@app.route("/hello")
def hello():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ogrenciler;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Sonuçları string'e çevir
        result = "<h2>Öğrenciler:</h2><ul>"
        for row in rows:
            result += f"<li>ID: {row[0]}, Ad: {row[1]}, Soyad: {row[2]}, No: {row[3]}, Ders: {row[4]}, Midterm: {row[5]}</li>"
        result += "</ul>"
        return result
    except Exception as e:
        return f"Database connection failed: {str(e)}"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

