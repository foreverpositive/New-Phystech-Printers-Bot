FROM ubuntu

WORKDIR /

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y git python3 python3-pip

RUN git clone https://github.com/foreverpositive/New-Phystech-Printers-Bot.git cloned

RUN mv cloned/* .. && rm -rf cloned

RUN pip install -r requirements.txt

CMD python main.py
