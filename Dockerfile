FROM ubuntu

WORKDIR /

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y git python3 python3-pip avahi-daemon cups cups-pdf samba ufw

RUN ufw allow 631/tcp && ufw allow 5353/udp

RUN sed -i 's/Listen localhost:631/#Listen localhost:631/g' /etc/cups/cupsd.conf
RUN \
cat >> /etc/cups/cupsd.conf <<'EOF'
Port 631
Browsing On
BrowseLocalProtocols dnssd
EOF

RUN lpadmin -p cups-pdf -v cups-pdf:/ -E -P /usr/share/ppd/cups-pdf/CUPS-PDF.ppd

RUN git clone https://github.com/foreverpositive/New-Phystech-Printers-Bot.git cloned

WORKDIR /cloned/

RUN pip install -r requirements.txt

CMD python3 main.py