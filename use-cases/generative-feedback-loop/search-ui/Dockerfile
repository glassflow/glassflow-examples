FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "search_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
