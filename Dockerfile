# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./bitespeed/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./bitespeed .

EXPOSE 8000
# CMD ["gunicorn", "bitespeed.wsgi", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]