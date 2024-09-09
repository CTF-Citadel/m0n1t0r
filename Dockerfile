FROM docker.io/library/python:latest

WORKDIR /app

COPY /app /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "9999"]