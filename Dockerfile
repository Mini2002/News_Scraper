FROM python:3.13.3-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt  

CMD ["python","bbc_new.py"]