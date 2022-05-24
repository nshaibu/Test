FROM python:3.8
WORKDIR .
ENV PATH=$PATH:.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8070
COPY . .
RUN chmod +x entrypoint.sh
RUN chmod +x run_app.sh
RUN chmod +x run_celery.sh