FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "9300"]