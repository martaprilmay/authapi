FROM python:3.9-alpine

RUN mkdir -p /usr/scr/authapi
WORKDIR /usr/scr/authapi

COPY ./requirements.txt /usr/scr/requirements.txt
RUN pip install -r /usr/scr/requirements.txt

COPY . /usr/scr/authapi

EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]