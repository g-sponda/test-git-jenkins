FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 9213
CMD ["python","exporter.py", "--file", "example.yml"]