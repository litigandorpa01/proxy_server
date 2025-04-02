FROM python:3.12-slim

WORKDIR /home/app
COPY . /home/app

RUN apt-get update && apt-get install -y curl

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
