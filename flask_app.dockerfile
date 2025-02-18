FROM python:3.10-alpine

WORKDIR /flask_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /flask_app/

CMD [ "python", "main.py" ]

EXPOSE 5000