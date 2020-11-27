FROM python:3.8.6-slim
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app
ENV FLASK_APP="fraud_detection/flask_app/app.py"
ENV FLASK_ENV=development
ENV FLASK_DEBUG=true
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
