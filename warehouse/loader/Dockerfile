FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY loader.py inspect_bronze.py ./

CMD ["python", "loader.py"]
