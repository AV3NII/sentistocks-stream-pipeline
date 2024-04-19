FROM python:3.10

WORKDIR /app/dashboard

COPY dashboard .

COPY secrets/gcp-sentistocks-credentials.json /app/secrets/gcp-sentistocks-credentials.json

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8501

RUN pip install -r req.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/gcp-sentistocks-credentials.json

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit" , "run", "/app/dashboard/app.py", "--server.port", "8501", "--server.headless", "True", "--server.address", "0.0.0.0" ]