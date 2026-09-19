FROM python:3.14-slim-bookworm

WORKDIR /usr/src/app

COPY requirments.txt ./ 

RUN pip install --no-cache-dir -r requirments.txt

COPY . .

CMD ["uvicorn" , "app.main:app", "--host" , "0.0.0.0" , "--port" , "8000" , "--reload"]


