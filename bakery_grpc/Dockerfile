FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/bakery
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r /home/bakery/requirements.txt
COPY . .

EXPOSE 50051
CMD [ "python", "main.py" ]