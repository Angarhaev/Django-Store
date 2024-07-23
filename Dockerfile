FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY mysite .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
