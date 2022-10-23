FROM python:3.10.5-buster

COPY ./requirements.txt /CostcoTW_API_Parser/requirements.txt

RUN pip install --no-cache-dir -r /CostcoTW_API_Parser/requirements.txt && \
    apt-get update && \
    apt-get install net-tools

COPY ./app /CostcoTW_API_Parser/app

WORKDIR /CostcoTW_API_Parser
EXPOSE 8000

CMD [ "uvicorn" ,"app:asgi_app" ,"--host=0.0.0.0" ,"--port=8000" ]