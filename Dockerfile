FROM python:3.11

COPY . .

RUN pip install -r requirements.txt


# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
