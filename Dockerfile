FROM python:3.6

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY server server

EXPOSE 8000
CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0"]
