
FROM python:3.11 

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["sh", "-c", "python app.py && flask run --host=0.0.0.0 --port=4000"]

