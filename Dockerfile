FROM python:3.9-buster

WORKDIR /app


COPY run.sh /
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod a+x /run.sh

COPY . .

CMD [ "/run.sh" ]