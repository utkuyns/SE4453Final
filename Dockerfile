FROM python:3.10-slim

# SSH kurulumu ve key üretimi
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    ssh-keygen -A

# SSH kullanıcı tanımı ve config ayarları
RUN useradd -m admin && echo "admin:admin123" | chpasswd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Uygulama dosyaları ve Python bağımlılıkları
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Başlatma scripti
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Web (5000) ve SSH (2222) portları dışa açılıyor
EXPOSE 5000 2222

# Başlangıç komutu
CMD ["/init.sh"]
