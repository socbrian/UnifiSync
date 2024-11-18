FROM python:3.9-buster

WORKDIR /app

COPY run.sh /run.sh
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /run.sh

COPY . .

CMD ["python", "mqtt_listener.py"]