# Python 3.10 bazlı küçük imaj
FROM python:3.10-slim

# SSH server kurulumu
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# SSH kullanıcı oluşturma (kullanıcı: admin / şifre: admin123)
RUN useradd -m admin && echo "admin:admin123" | chpasswd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# Uygulama klasörüne geç
WORKDIR /app

# Proje dosyalarını kopyala
COPY . /app

# Gerekli Python paketlerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Başlatma scriptini kopyala ve çalıştırılabilir yap
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Portları aç (22: SSH, 5000: Flask app)
EXPOSE 22 5000

# Container başlarken çalışacak komut
CMD ["/init.sh"]
