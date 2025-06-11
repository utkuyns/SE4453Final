FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    ssh-keygen -A  

RUN useradd -m admin && echo "admin:admin123" | chpasswd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY init.sh /init.sh
RUN chmod +x /init.sh

EXPOSE 22 5000

CMD ["/init.sh"]
