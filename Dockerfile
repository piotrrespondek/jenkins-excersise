FROM python:3.12-slim

WORKDIR /usr/app

COPY script.py .

CMD ["python", "script.py"]