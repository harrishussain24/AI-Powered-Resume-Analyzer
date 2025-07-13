FROM python:3.11-slim

# System dependencies (slimmed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
# Install torch first with the extra index
RUN pip install --no-cache-dir torch==2.2.0 --extra-index-url https://download.pytorch.org/whl/cpu
# Then install the rest of the requirements (excluding torch)
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
