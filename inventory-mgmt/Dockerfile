FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nginx \
    build-essential \
    libmariadb-dev \
    libmariadb-dev-compat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
