FROM python:3.11.1

WORKDIR /app

COPY . .

RUN pip install -r my_reqs.txt

CMD flask run -h 0.0.0.0 -p 5000