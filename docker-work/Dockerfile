# this is to pull python image. # this is command
FROM python:latest

WORKDIR /app 

COPY code/requirements.txt .

RUN pip install -r requirements.txt

COPY code/app.py .

EXPOSE  5000

CMD python app.py